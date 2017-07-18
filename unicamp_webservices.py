import os, requests
from BandecoClasses import *

UNICAMP_WEBSERVICES_URL = "https://webservices.prefeitura.unicamp.br/cardapio_json.php"
from app import cache
import pprint


def limpa_especificos(ref):
    """
    Faz modificacoes especificas, como remover tags HTML e transformar siglas em maiusculo.
    :param ref: dicionario da refeicao a ser "limpada"
    """
    ref['observacoes'] = ref['observacoes'].replace('<font color = "red">', '')
    ref['observacoes'] = ref['observacoes'].replace('</font>', '')
    ref['pts'] = ref['pts'].replace('pts', 'PTS')  # TODO



def limpa_chaves(refeicoes_list):
    """
    Faz a "limpeza" dos cardapios. Transforma letras em minusculas ou titulos, remove tags HTML, etc.
    Tambem altera o nome de algumas chaves para ficarem iguais aos atributos das classes definidas em BandecoClasses.
    :param refeicoes_list: lista com dicionarios contendo as informacoes das refeicoes.
    :return: lista atualizada apos a "limpeza"
    """
    for ref in refeicoes_list:
        try:
            for key in list(ref.keys()):
                ref[key] = ref[key].capitalize()
                ref[key.lower()] = ref.pop(key)

            # modificar chaves para ficarem de acordo com os atributos da classe que eu defini.
            ref['prato_principal'] = ref.pop('prato principal')
            ref['arroz_feijao'] = ref.pop('acompanhamento')
            ref['observacoes'] = ref.pop('obs')
            limpa_especificos(ref)

            # TODO: consertar essa gambiarra depois.

        except AttributeError as e:
            print("Refeicoes nao sao dicionarios")









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
    r = requests.get("https://webservices.prefeitura.unicamp.br/cardapio_json.php", proxies=proxyDict)

    raw_json = r.content


    try:
        cardapios = json.loads(raw_json)
        refeicoes_list = cardapios['CARDAPIO']
    except KeyError as e:
        print('KeyError tentando pegar array de refeicoes.')
        refeicoes_list = []
    except:
        print("erro deserializando conteudo do JSON.")
        refeicoes_list = []


    return refeicoes_list, None



# cache com timeout de 60min para limitar requests ao API da UNICAMP.
@cache.cached(timeout=(60*60), key_prefix='get_all_cardapios')
def get_all_cardapios():
    """
    Entrypoint que fornece uma lista de objetos Cardapio realizando um request para o webservices da Unicamp.
    :return: lista com os cardapios disponiveis ja em objetos da classe Cardapio e um status code para informar sucesso ou erro.
    """
    refeicoes_list = request_cardapio() # faz o request e recebe uma lista contendo as refeicoes em dicionarios.


    limpa_chaves(refeicoes_list) # faz a limpeza das informacoes.

    cardapios_por_data = cria_refeicoes(refeicoes_list)


    cardapios = cria_cardapios(cardapios_por_data)




    print("request para UNICAMP esta completo.")
    # print(cardapios)
    return cardapios


def main():
    get_all_cardapios()


if __name__ == '__main__':
    main()



'''
Error handling:

- Nao funcionar com esse modulo, usar o outro. Informar isso ao app.
- Definir custom Exceptions para cada etapa (metodo chamado pra obters os objetos Cardapio).
- 


'''