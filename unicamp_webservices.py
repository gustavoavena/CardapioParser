import os, requests
from BandecoClasses import *
from app import app
from limpa_informacoes import *

class CardapioCache:
    cardapios = []

UNICAMP_WEBSERVICES_URL = "https://webservices.prefeitura.unicamp.br/cardapio_json.php"



@app.before_first_request
def setup_webservices():
    print("Setting up unicamp_webservices...")
    update_cache()
    print(CardapioCache.cardapios)



def update_cache():
    """
    Responsavel por ler o arquivo cardapio_cache, que sera atualizado pelo script heroku_cache.py, e atualizar o CardapioCache.cardapios (o "singleton" que sera usado para retornar os cardapios para o usuario).
    """
    try:
        print("Reading from cardapio_cache...")
        f = open('cardapio_cache', 'r')
        cardapio_list = eval(f.read())
        cardapios = []
        for v in cardapio_list:
            cardapios.append(Cardapio(**v))

        CardapioCache.cardapios = cardapios
    except Exception as e:
        print("Erro lendo cardapio_cache", type(e), e)
    else:
        print("CardapioCache singleton updated!")










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

    cardapios = [limpa_nao_informado(c) for c in cardapios]

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




def request_cardapio():
    """"
    Responsavel por fazer o request ao webservices da UNICAMP.

    Esse metodo configurao add-on do Heroku que garante que todos os outbounds requests utilizando esse proxy sao feitos a partir de um IP fixo.
    """
    proxyDict = {
        "http": os.environ.get('FIXIE_URL', ''),
        "https": os.environ.get('FIXIE_URL', '')
    }
    try:
        r = requests.get("https://webservices.prefeitura.unicamp.br/cardapio_json.php", proxies=proxyDict)
        raw_json = r.content
    except:
        print("Erro no primeiro request para UNICAMP.")
        raw_json = b''
    else:
        print("Request para UNICAMP terminou ")



    try: # coloquei o try por fora so para casos de erro no len(raw_json) ou outro erro que nao pensei.
        if raw_json == b'' or len(raw_json) == 0:
            print("Usando servidor backup...")
            r = requests.get("https://backup-unicamp-server.herokuapp.com")
            raw_json = r.content
    except Exception as e:
        print("Exception no backup request: ", e)
    else:
        print("Request backup terminou sem exceptions.")


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
        print("Request para a UNICAMP feito com sucesso.")


    return refeicoes_list





# cache com timeout de 60min para limitar requests ao API da UNICAMP.
def get_all_cardapios():
    """
    Entrypoint que fornece uma lista de objetos Cardapio realizando um request para o webservices da Unicamp.
    :return: lista com os cardapios disponiveis ja em objetos da classe Cardapio.
    """
    refeicoes_list = request_cardapio() # faz o request e recebe uma lista contendo as refeicoes em dicionarios.

    limpa_chaves(refeicoes_list) # faz a limpeza das informacoes.

    cardapios_por_data = cria_refeicoes(refeicoes_list)


    cardapios = cria_cardapios(cardapios_por_data)

    if len(cardapios) > 0:
        print("request para UNICAMP esta completo.")
    else:
        print("unicamp_server falhou!")

    return cardapios



def main():
    update_cache()


if __name__ == '__main__':
    main()



'''
Error handling:

- Nao funcionar com esse modulo, usar o outro. Informar isso ao app.
- Definir custom Exceptions para cada etapa (metodo chamado pra obters os objetos Cardapio).
- 


'''