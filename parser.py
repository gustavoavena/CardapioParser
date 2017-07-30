from functools import reduce

from bs4 import BeautifulSoup
import requests
from BandecoClasses import *
import date_services

from limpa_informacoes import *
from app import cache


URL_TEMPLATE = "http://catedral.prefeitura.unicamp.br/cardapio.php?d="

# TODO: error handling in case the menu doesn' follow the pattern, or there is no menu for that day (weekends).






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

    cardapio = {}

    print(items)
    observacoes = []

    obs = items.pop()
    print(obs)
    while("Observações:" not in obs):
        observacoes.append(obs)
        obs = items.pop()

    observacoes.append(obs)

    observacoes.reverse()



    observacao_final = reduce(lambda x, y: x+y, observacoes)
    cardapio["observacoes"] = observacao_final.replace("Observações: ", "Obs: ").capitalize()

    print(cardapio["observacoes"])

    suco = items.pop()
    cardapio["suco"] = suco.replace("SUCO:", "").capitalize()

    sobremesa = items.pop()
    cardapio["sobremesa"] = sobremesa.replace("SOBREMESA:", "").capitalize()

    salada = items.pop()
    cardapio["salada"] = salada.replace("SALADA:", "").capitalize()

    prato_principal_list = []

    pp = items.pop()

    if "PTS" in pp:
        cardapio["pts"] = pp.capitalize()
        pp = items.pop()
    else:
        cardapio["pts"] = "-"

    if "PRATO PRINCIPAL:" not in pp:
        cardapio["guarnicao"] = pp.replace("GUARNIÇÃO: ", "").capitalize()
        pp = items.pop()
    else:
        cardapio["guarnicao"] = "-"


    prato_principal = pp.replace("PRATO PRINCIPAL:  ", "").replace("PRATO PRINCIPAL: ", "").capitalize()

    # while ("PRATO PRINCIPAL:" not in pp):
    #     prato_principal_list.append(pp)
    #     obs = items.pop()

    # prato_principal_list.append(pp)

    # prato_principal_list = prato_principal_list.reverse()

    # prato_principal = reduce(lambda x, y: x+y, prato_principal_list)

    cardapio["prato_principal"] = prato_principal

    print(prato_principal)

    print(cardapio)



    # TODO: organizar isso da guarnicao e do PTS.
    # o que sobra eh a guarnicao e o pts.
    # cardapio["guarnicao"] = items[0].capitalize().replace("pts", "PTS")

    # if len(items) == 2:
    #     cardapio["pts"] = items[1].capitalize().replace("pts", "PTS")
    # else:
    #     cardapio["pts"] = "-"

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


# @cache.memoize(timeout=60 * 5) # cache com timeout de 5min
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


