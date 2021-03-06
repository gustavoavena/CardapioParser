import requests
from models.bandex_classes import *
from parsing.limpa_informacoes import *
import parser
from datetime import date
from persistence.firebase import setup_firebase
from persistence import environment_vars


class CardapioCache:
    cardapios = []

UNICAMP_WEBSERVICES_URL = "https://webservices.prefeitura.unicamp.br/cardapio_json.php"






def cria_cardapios(cardapios_por_data):
    """
    Recebe objetos de Refeicao agrupados por data em um dicionario e retorna uma lista de objetos Cardapios a partir desse dicionario.

    :param cardapios_por_data: dicionario do tipo {String: [Refeicao]}, onde a string eh uma data.
    :return: lista com os objetos Cardapio instanciados.
    """
    cardapios = []

    chaves_para_tipos = {
        'Almoço':'almoco',
        'Almoço vegetariano': 'almoco_vegetariano',
        'Jantar': 'jantar',
        'Jantar vegetariano': 'jantar_vegetariano'
    }

    for data in list(cardapios_por_data.keys()):
        refeicoes = {chaves_para_tipos[r.tipo] : r for r in cardapios_por_data[data]}
        cardapios.append(Cardapio(data=data, **refeicoes))

    # cardapios = [limpa_nao_informado(c) for c in cardapios]

    return cardapios





def cria_refeicoes(refeicoes_list):
    """
    Cria um dicionario que agrupas objetos da classe Refeicao por data a partir de uma lista de dicionarios contendo informacoes das refeicoes.


    :param refeicoes_list: Lista com refeicoes em dicionarios.
    :return: Dicionario que mapeia datas a uma lista com objetos Refeicao contendo o cardapios daquela data.
    """

    cardapios_por_data = {}

    for ref in refeicoes_list:
        try:
            d = ref['data']
        except KeyError as e:
            print("KeyError nas datas.")
            print(e, end="\n\n")
            break
        except TypeError as e:
            print("TypeError nas datas.")
            print(e, end="\n\n")
            break

        try:
            cardapios_por_data[d].append(Refeicao(**ref))
        except KeyError as e: # cria lista para aquela data e armazena a primeira refeicao.
            # print("criando list para data: {}".format(d))
            # print(e)
            cardapios_por_data[d] = [Refeicao(**ref)]
        except TypeError as e:
            print(e)
            print("provavelmente argumento a mais no construtor de Refeicao")


    return cardapios_por_data


def request_data_from_unicamp():
    """"
        Responsavel por fazer o request ao webservices da UNICAMP e armazenar a resposta no firebase.

        Esse metodo configura o add-on do Heroku que garante que todos os outbounds requests utilizando esse proxy sao feitos a partir de um IP fixo.
        """
    proxyDict = {
        "http": environment_vars.FIXIE_URL,
        "https": environment_vars.FIXIE_URL
    }
    try:
        print("Opcao 1: Executando request para o API da UNICAMP utilizando o proxy.")
        r = requests.get("https://webservices.prefeitura.unicamp.br/cardapio_json.php", proxies=proxyDict)
        raw_json = r.content
    except:
        print("Erro no primeiro request para UNICAMP.")
        raw_json = b''
    else:
        print("Request para API da UNICAMP terminou com sucesso.")

    # usar o backup server se o limite do add-on fixie foi atingido
    if raw_json == b'' or len(raw_json) == 0:
        try:
            print("Opcao 2: Request para servidor backup...")
            r = requests.get("https://backup-unicamp-server.herokuapp.com")
            raw_json = r.content
        except Exception as e:
            print("Exception no request para o PRIMEIRO servidor backup: ", e)
            raw_json = b''
        else:
            print("Request para o primeiro servidor backup terminou com sucesso.")

    # usar o SEGUNDO backup server se o limite do fixie do primeiro foi atingido
    if raw_json == b'' or len(raw_json) == 0:
        try:
            print("Opcao 3: Request para o SEGUNDO servidor backup...")
            r = requests.get("https://backup-unicamp-server2.herokuapp.com")
            raw_json = r.content
        except Exception as e:
            print("Exception no request para o SEGUNDO servidor backup: ", e)
            raw_json = b''
        else:
            print("Request para o segundo servidor backup terminou com sucesso.")




    # # Decode UTF-8 bytes to Unicode, and convert single quotes
    # # to double quotes to make it valid JSON
    raw_json = raw_json.decode('utf8').replace("'", '"')
    #
    # print("raw_json = ", raw_json)


    if raw_json == b'' or len(raw_json) == 0:
        print("Erro ao tentar armazenar JSON original no Firebase.")
        return None
    else:
        db = setup_firebase()
        db.child("cardapio_raw_json").set(raw_json)
        print("Firebase atualizado com o JSON original da UNICAMP.")
        return raw_json





def request_cardapio(raw_json):
    """
    Obtem o JSON original contendo todas as informacoes dos proximos cardapios e retorna uma lista com as refeicoes em dicionarios, para comecar o processo de criacao dos objetos de tipo Refeicao e Cardapio.


    :param raw_json: parametro opcional que contem as informacoes obtidas com o API da Unicamp em formato de JSON. Caso nao seja passado (acontece no envio das push notifications), essas informacoes sao obtidas pelo firebase.
    :return: lista contendo as refeicoes em dicionarios.
    """


    # so faz request pro firebase se nao tiver o json.
    if raw_json == None:
        db = setup_firebase()
        raw_json = db.child("cardapio_raw_json").get().val()

    try:
        cardapios = json.loads(raw_json)
        refeicoes_list = cardapios['CARDAPIO']
    except KeyError as e:
        print('KeyError tentando pegar array de refeicoes.')
        refeicoes_list = []
    except:
        print("erro deserializando conteudo do JSON.")
        refeicoes_list = []
    else:
        print("Unloading do JSON feito com sucesso.")


    return refeicoes_list







def use_parser():
    try:
        print("Opcao 4: Usando parser para obter cardapios...")
        date_string = date.today().strftime("%y-%m-%d")
        cardapios = parser.get_next_cardapios(date_string, 10)
    except:
        print("Uso do parser falhou.")
        cardapios = []
    else:
        print("Parser executado com sucesso.")

    return cardapios



# cache com timeout de 60min para limitar requests ao API da UNICAMP.
def get_all_cardapios(raw_json=None):
    """
    Fornece uma lista de objetos Cardapio (contendo todos os cardapios disponiveis). O JSON com as informacoes e obtido pelo firebase e passa por um processo de "limpeza". Esse JSON e obtido pelo API da Unicamp e salvo no firebase utilizando a funcao `request_data_from_unicamp` (mais informacoes la).
    Como o modulo `heroku_cache.py` faz o request pra Unicamp e serializa os objetos logo depois, eu coloquei um parametro opcional `raw_json` que pode ser passado para que um request para o firebase nao precise ser feito desnecessariamente.

    :param raw_json:
    :return: lista com os cardapios disponiveis ja em objetos da classe Cardapio.
    """
    refeicoes_list = request_cardapio(raw_json) # faz o request e recebe uma lista contendo as refeicoes em dicionarios.

    limpa_chaves(refeicoes_list) # faz a limpeza das informacoes.

    cardapios_por_data = cria_refeicoes(refeicoes_list)


    cardapios = cria_cardapios(cardapios_por_data)

    if len(cardapios) > 0:
        print("Cardápios obtidos com sucesso.")
        return cardapios
    else: # usar o parser se os requests para os APIs todos falharam.
        print("ERRO: não foi possível obter os cardápios com nenhum dos requests!")
        return use_parser()




#
# def main():
#     print("unicamp_webservices main() has no purpose.")
#     # update_cache()
#
#
# if __name__ == '__main__':
#     main()
#


'''
Error handling:

- Nao funcionar com esse modulo, usar o outro. Informar isso ao app.
- Definir custom Exceptions para cada etapa (metodo chamado pra obters os objetos Cardapio).
- 


'''