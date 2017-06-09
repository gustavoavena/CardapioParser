from bs4 import BeautifulSoup
import requests
import pprint
from BandecoClasses import *
import date_services


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



def pega_salada_sobremesa_suco(items):
    alimentos = ["salada", "suco", "sobremesa"]
    cardapio = {}

    for alim in alimentos:
        tag = alim.upper() + ":" # tag para procurar o cardapio dos alimentos acima dentro do vetor items
        valor = [s.replace(tag, "") for s in items if tag in s][0] # pega o valor do alimento e ja tira a tag (e.g. "SOBREMESA:")
        cardapio[alim] = valor.capitalize() # lowercase eh melhor para exibir.
        items = [s for s in items if tag not in s]


    return cardapio, items



def get_refeicao(tipo, soup):
    cardapio = {}

    items = [s for s in soup.get_text().split("\n") if s]

    print(items)

    cardapio, items = pega_salada_sobremesa_suco(items)

    cardapio["arroz_feijao"] = items.pop(0).capitalize()

    cardapio["observacoes"] = items.pop().replace("Observações:  ", "").title()

    cardapio["prato_principal"] = items.pop(0).replace("PRATO PRINCIPAL:  ", "").capitalize()
    cardapio["guarnicao"] = items[0].capitalize()
    cardapio["pts"] = items[1].capitalize()

    return Refeicao(tipo=tipo, **cardapio)

def cardapio_por_data(data_string):
    res = requests.get(URL_TEMPLATE+data_string)

    html_doc = res.content
    soup = BeautifulSoup(html_doc, 'html.parser')
    meals = soup.find_all(class_="fundo_cardapio")

    tipos_refeicoes = list(TipoRefeicao)
    # print(refeicoes[0].value)

    refeicoes = {}

    for i, m in enumerate(meals[1:]):
        refeicoes[tipos_refeicoes[i]] = get_refeicao(tipos_refeicoes[i].value, m)

    # print("refs = ", refeicoes)

    cardapio = Cardapio.fromRefeicoesDict(data=data_string, refeicoes=refeicoes)
    print("cardapio = ", cardapio)

    return cardapio





# retorna um dict com o cardapio completo do dia para cada data.
def cardapio_para_datas(data_strings):
    cardapios = []

    for data in data_strings:
        c = cardapio_por_data(data)
        cardapios.append(c)

    return cardapios


def get_next_cardapios(date_string, next):
    date_strings = date_services.next_weekdays(next, start_date=date_string)
    return cardapio_para_datas(date_strings)



if __name__ == '__main__':
    main()
