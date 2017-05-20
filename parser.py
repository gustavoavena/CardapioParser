from bs4 import BeautifulSoup
import requests
import pprint


# file = open("cardapio.html", "r")

def main():
    res = requests.get("http://catedral.prefeitura.unicamp.br/cardapio.php?d=2017-05-22")
    # html_doc = file.read()
    html_doc = res.content
    # print(html_doc)

    soup = BeautifulSoup(html_doc, 'html.parser')

    meals = soup.find_all(class_="fundo_cardapio")

    # print(meals)
    # for i,m in enumerate(meals[1:]):
    #     print("\n\ni = ", i)
    #     print(m)

    cardapio = {}
    refeicoes = ["Almoço", "Almoço Vegetariano", "Jantar", "Jantar Vegetariano"]

    for i,m in enumerate(meals[1:]):
        # print("\n\ni = ", i)
        preenche_refeicao(cardapio, refeicoes[i], m)


    # pprint.pprint(cardapio)



# Exemplo:
# ['ARROZ E FEIJÃO']  = ['NavigableString']
# [<strong>PRATO PRINCIPAL:</strong>, ' ', <br/>, ' STEAK']  = ['Tag', 'NavigableString', 'Tag', 'NavigableString']
# ['CREME DE ESPINAFRE']  = ['NavigableString']
# [' PTS COM ABOBRINHA']  = ['NavigableString']
# [<strong>SALADA:</strong>, 'CENOURA RALADA']  = ['Tag', 'NavigableString']
# [<strong>SOBREMESA:</strong>, 'MAÇÃ']  = ['Tag', 'NavigableString']
# [<strong>SUCO:</strong>, 'MARACUJÁ']  = ['Tag', 'NavigableString']
# [<br/>, <strong>Observações:</strong>, ' ', <br/>, ' O CARDÁPIO CONTÉM GLÚTEN NO PÃO E NO CREME DE ESPINAFRE. CONTÉM LACTOSE NO CREME DE ESPINAFRE. NÃO CONTÉM OVOS.']  = ['Tag', 'Tag', 'NavigableString', 'Tag', 'NavigableString']


def pega_salada_sobremesa_suco(items):
    alimentos = ["salada", "suco", "sobremesa"]
    cardapio = {}

    for i, alim in enumerate(alimentos):
        tag = alimentos[i].upper() + ":"
        valor = [s.replace(tag, "") for s in items if tag in s][0]
        cardapio[alimentos[i]] = valor
        items = [s for s in items if tag not in s]


    return cardapio, items


def preenche_refeicao(cardapio_do_dia, refeicao, soup):
    cardapio = {}

    items = [s for s in soup.get_text().split("\n") if s]
    print(items)

    cardapio, items = pega_salada_sobremesa_suco(items)

    # pega tipo de arroz:
    cardapio["arroz_feijao"] = items.pop(0)

    # observacoes
    cardapio["observacoes"] = items.pop().replace("Observações:  ", "")

    # prato principal
    cardapio["prato_principal"] = [items.pop(0).replace("PRATO PRINCIPAL:  ", ""), *items] # o que sobrar faz parte do prato principal


    print(cardapio)
    print("\n\n")

    cardapio_do_dia[refeicao] = cardapio
    return cardapio_do_dia


if __name__ == '__main__':
    main()





