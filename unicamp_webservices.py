import os, requests

from BandecoClasses import *
from app import app

from cache_scheduler import CardapioCache

UNICAMP_WEBSERVICES_URL = "https://webservices.prefeitura.unicamp.br/cardapio_json.php"

import re






@app.before_first_request
def setup_webservices():
    print("Setting up unicamp_webservices...")
    CardapioCache.cardapios = get_all_cardapios()
    print(CardapioCache.cardapios)
    write_to_cardapio_cache(CardapioCache.cardapios)





def update_cache():
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





def uppercase(matchobj):
    return matchobj.group(0).upper()

def capitalize(s):
    return re.sub('^([a-z])|'
                  '[\.|\?|\!]\s*([a-z])|'
                  '\s+([a-z])(?=\.)|'
                  '[\s,\.]+(ru|rs|ra)[\s,\.]+', uppercase, s)

def clean_spaces(s):
    s = re.sub('\s{2,}|\n', ' ', s)
    s = re.sub('\s\:\s*', ': ', s)
    return s


def limpa_especificos(ref):
    """
    Faz modificacoes especificas, como remover tags HTML e transformar siglas em maiusculo.
    :param ref: dicionario da refeicao a ser "limpada"
    """
    ref['observacoes'] = ref['observacoes'].replace('<font color = "red">', '')
    ref['observacoes'] = ref['observacoes'].replace('</font>', '')
    ref['observacoes'] = capitalize(capitalize(ref['observacoes'])) # chamar duas vezes pra resovler o problema do RA, que nao era alterado porque o RU dava match com a virgula primeiro.
    ref['observacoes'] = clean_spaces(ref['observacoes'])


    for key in ['pts', 'prato_principal']:
        ref[key] = ref[key].replace('pts', 'PTS').replace('Pts', 'PTS')  # vergonhoso, mas dps conserto



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



# TODO: melhorar isso depois. Muito zona e ruim...
def limpa_nao_informado(cardapio):
    attributes = ['guarnicao', 'pts']
    NAO_INF = 'Não informado'
    DASH = '-'

    try:
        cardapio.almoco.guarnicao = cardapio.almoco.guarnicao.replace(NAO_INF, DASH)
        cardapio.jantar.guarnicao = cardapio.jantar.guarnicao.replace(NAO_INF, DASH)

        cardapio.almoco.pts = cardapio.almoco.pts.replace(NAO_INF, DASH)
        cardapio.jantar.pts = cardapio.jantar.pts.replace(NAO_INF, DASH)
    except AttributeError:
        print("AttributeError limpando nao informado.")
    except:
        print("Erro desconhecido limpando nao informado.")


    for at in attributes:
        try:

            value = getattr(cardapio.almoco_vegetariano, at)
            value = value.replace('Não informado', getattr(cardapio.almoco, at))
            setattr(cardapio.almoco_vegetariano, at, value)

            value = getattr(cardapio.jantar_vegetariano, at)
            value = value.replace('Não informado', getattr(cardapio.jantar, at))
            setattr(cardapio.jantar_vegetariano, at, value)
        except AttributeError as e:
            print("Attribute error!")
        except:
            print("Erro desconhecido limpando nao informados.")

    return cardapio






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
        return []



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

def write_to_cardapio_cache(cardapios):
    try:
        f = open('cardapio_cache', 'w')
        f.write(json.dumps(cardapios, cls=MyJsonEncoder))
        f.close()
    except Exception as e:
        print("Exception: ", e)

    else:
        print("cardapio_cache updated successfully inside unicamp_webservices.")

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
        # date_string = date.today().strftime("%y-%m-%d")
        # return get_next_cardapios(date_string, 5)

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