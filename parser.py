from bs4 import BeautifulSoup
import requests
from BandecoClasses import *
import date_services

# from unicamp_webservices import limpa_especificos

from app import cache
import re


URL_TEMPLATE = "http://catedral.prefeitura.unicamp.br/cardapio.php?d="

# TODO: error handling in case the menu doesn' follow the pattern, or there is no menu for that day (weekends).

# TODO: colcoar funcoes de limpeza num modulo separado.

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



def pega_salada_sobremesa_suco(items):
    """ Funcao auxiliar que popula os atributos salada, sobremesa e suco do cardapio da refeicao fornecida."""
    alimentos = ["salada", "suco", "sobremesa"]
    cardapio = {}

    for alim in alimentos:
        tag = alim.upper() + ":" # tag para procurar o cardapio dos alimentos acima dentro do vetor items
        valor = [s.replace(tag, "") for s in items if tag in s][0] # pega o valor do alimento e ja tira a tag (e.g. "SOBREMESA:")
        cardapio[alim] = valor.capitalize() # lowercase eh melhor para exibir.
        items = [s for s in items if tag not in s]


    return cardapio, items



def get_refeicao(tipo, soup):
    """
    Faz o parsing do cardapio de uma refeicao (e.g. almoco, jantar), dado o elemento em HTML contendo as informacoes.

    :param tipo: string que representa qual refeicao é (e.g. "Almoço", "Jantar")
    :param soup: objeto do BeatifulSoup que contem o HTML e sera utilizado para fazer o parsing.
    :return: dict com cardapio de uma refeicao.
    """
    items = [s for s in soup.get_text().split("\n") if s] # retira todas as tags de HTML, e armazena todos os elementos (strings nao vazias) em uma lista.
    cardapio, items = pega_salada_sobremesa_suco(items)

    cardapio["arroz_feijao"] = items.pop(0).capitalize()

    obs = items.pop() # o ultimo item eh a observacao, que pode ter um ou dois elementos.
    if "Observações:  " not in obs:
        cardapio["observacoes"] = (items.pop().replace("Observações:  ", "Obs: ").capitalize() + obs.capitalize())
    else:
        cardapio["observacoes"] = obs.replace("Observações:  ", "Obs: ").capitalize()

    ACRONIMOS = ["pts", " ru ", " ra ", " rs "]

    for sig in ACRONIMOS: # procura siglas e deixa elas em maiusculo.
        cardapio["observacoes"].replace(sig, sig.upper())


    # o primeiro item nesse ponto eh sempre o prato principal.
    cardapio["prato_principal"] = items.pop(0).replace("PRATO PRINCIPAL:  ", "").capitalize()


    # TODO: organizar isso da guarnicao e do PTS.
    # o que sobra eh a guarnicao e o pts.
    cardapio["guarnicao"] = items[0].capitalize().replace("pts", "PTS")

    if len(items) == 2:
        cardapio["pts"] = items[1].capitalize().replace("pts", "PTS")
    else:
        cardapio["pts"] = "-"

    limpa_especificos(cardapio)


    return Refeicao(tipo=tipo, **cardapio) # retorna objeto da classe Refeicao utilizando dando "unwrap" no dictionario.



def cardapio_por_data(data_string):
    """
    Dada a string de uma data, fornece o objeto da classe Cardapio correspondente ao cardapio dessa data.

    :param data_string: string da data do cardapio desejado.
    :return: objeto da classe Cardapio que contem o cardapio requisitado.
    """
    res = requests.get(URL_TEMPLATE+data_string) # faz o request para a pagina da prefeitura

    html_doc = res.content # pega a pagina HTML
    soup = BeautifulSoup(html_doc, 'html.parser')
    meals = soup.find_all(class_="fundo_cardapio") # pega todos os elementos da classe fundo_cardapio. Dos 5 encontrados, 4 sao os cardapios das 4 refeicoes.

    tipos_refeicoes = list(TipoRefeicao) # lista os tipos de refeicao para iterarmos sobre eles.

    refeicoes = {}

    for i, m in enumerate(meals[1:]):
        refeicoes[tipos_refeicoes[i]] = get_refeicao(tipos_refeicoes[i].value, m)


    return Cardapio.fromRefeicoesDict(data=data_string, refeicoes=refeicoes) # instacia um objeto Cardapio






def cardapio_para_datas(data_strings):
    """
    Dada uma lista com strings das datas, essa funcao retorna os objetos Cardapio desses cardapios em uma lista.

    :param data_strings: lista com strings das datas dos cardapios desejados.
    :return: lista com objetos da classe Cardapio que contem os cardapios das datas fornecidas.
    """
    cardapios = []

    for data in data_strings:
        c = cardapio_por_data(data)
        cardapios.append(c)

    return cardapios


@cache.memoize(timeout=60 * 5) # cache com timeout de 5min
def get_next_cardapios(date_string, next):
    """
    Fornece os cardapios dos *next* dias a partir da data fornecida em *date_string*.

    Ponto de entrada principal. A view que sera chamada no app sera essa.


    :param date_string: data inicial.
    :param next: inteiro que representa a quantidade de cardapios desejados a partir da data inicial.
    :return: lista com os objetos Cardapio contendo os cardapios das datas requisitadas.
    """

    date_strings = date_services.next_weekdays(next, start_date=date_string)
    print("EXECUTOU get_next_cardapio")
    return cardapio_para_datas(date_strings)


