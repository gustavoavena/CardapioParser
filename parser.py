from bs4 import BeautifulSoup
import requests
import pprint
from enum import Enum
import json

class Refeicao(Enum):
    ALMOCO = "Almoço"
    ALMOCO_VEGETARIANO = "Almoço Vegetariano"
    JANTAR = "Jantar"
    JANTAR_VEGETARIANO = "Jantar Vegetariano"

class ItemCardapio(Enum):
    ARROZ_FEIJAO = "arroz_feijao"
    PRATO_PRINCIPAL = "prato_principal"
    SALADA = "salada"
    SOBREMESA = "sobremesa"
    SUCO = "suco"
    OBSERVACOES = "observacoes"


URL_TEMPLATE = "http://catedral.prefeitura.unicamp.br/cardapio.php?d="

# TODO: use enumeration to improve code organization.
# TODO: change the menu strings to lowercase.
# TODO: error handling in case the menu doesn' follow the pattern, or there is no menu for that day (weekends).
# TODO: listar strings que nao podem ir pra lowercase (e.g. PTS, RU, RA)

def main():
    cardapio = cardapio_por_data("2017-05-22")

    # pprint.pprint(cardapio)
    string = json.dumps(cardapio, indent=4, ensure_ascii=False)
    # pprint.pprint(string)

# recebe data no formato "AAAA-MM-DD" e retorna um dicionario com o cardapio daquele dia, caso tenha um.


def cardapio_por_data(data):
    res = requests.get(URL_TEMPLATE+data)

    html_doc = res.content

    soup = BeautifulSoup(html_doc, 'html.parser')

    meals = soup.find_all(class_="fundo_cardapio")

    cardapio = {}
    refeicoes = ["Almoço", "Almoço Vegetariano", "Jantar", "Jantar Vegetariano"]

    for i, m in enumerate(meals[1:]):
        preenche_refeicao(cardapio, refeicoes[i], m)

    return cardapio

def pega_salada_sobremesa_suco(items):
    alimentos = ["salada", "suco", "sobremesa"]
    cardapio = {}

    for alim in alimentos:
        tag = alim.upper() + ":" # tag para procurar o cardapio dos alimentos acima dentro do vetor items
        valor = [s.replace(tag, "") for s in items if tag in s][0] # pega o valor do alimento e ja tira a tag (e.g. "SOBREMESA:")
        cardapio[alim] = valor.capitalize() # lowercase eh melhor para exibir.
        items = [s for s in items if tag not in s]


    return cardapio, items


def preenche_refeicao(cardapio_do_dia, refeicao, soup):
    cardapio = {}

    items = [s for s in soup.get_text().split("\n") if s]

    # print(items)

    cardapio, items = pega_salada_sobremesa_suco(items)

    # pega tipo de arroz:
    cardapio["arroz_feijao"] = items.pop(0).capitalize()

    # observacoes
    cardapio["observacoes"] = items.pop().replace("Observações:  ", "").title()

    # prato principal
    cardapio["prato_principal"] = [items.pop(0).replace("PRATO PRINCIPAL:  ", "").capitalize(), *[i.capitalize() for i in items]] # o que sobrar faz parte do prato principal

    cardapio_do_dia[refeicao] = cardapio


    return cardapio_do_dia


# retorna um dict com o cardapio completo do dia para cada data.
def cardapio_para_datas(datas):
    cardapios= {}

    for data in datas:
        c = cardapio_por_data(data)
        cardapios[data] = c

    return cardapios




if __name__ == '__main__':
    main()
