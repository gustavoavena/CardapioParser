from bs4 import BeautifulSoup
import requests


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



# Exemplo:
# ['ARROZ E FEIJÃO']  = ['NavigableString']
# [<strong>PRATO PRINCIPAL:</strong>, ' ', <br/>, ' STEAK']  = ['Tag', 'NavigableString', 'Tag', 'NavigableString']
# ['CREME DE ESPINAFRE']  = ['NavigableString']
# [' PTS COM ABOBRINHA']  = ['NavigableString']
# [<strong>SALADA:</strong>, 'CENOURA RALADA']  = ['Tag', 'NavigableString']
# [<strong>SOBREMESA:</strong>, 'MAÇÃ']  = ['Tag', 'NavigableString']
# [<strong>SUCO:</strong>, 'MARACUJÁ']  = ['Tag', 'NavigableString']
# [<br/>, <strong>Observações:</strong>, ' ', <br/>, ' O CARDÁPIO CONTÉM GLÚTEN NO PÃO E NO CREME DE ESPINAFRE. CONTÉM LACTOSE NO CREME DE ESPINAFRE. NÃO CONTÉM OVOS.']  = ['Tag', 'Tag', 'NavigableString', 'Tag', 'NavigableString']


def pega_salada_sobremsa_suco(items):
    alimentos = ["salada", "suco", "sobremesa"]
    cardapio = {}

    print(cardapio)
    print(items)
    print("\n")
    for i, alim in enumerate(alimentos):
        tag = alimentos[i].upper() + ":"

        valor = [s.replace(tag, "") for s in items if tag in s][0]

        cardapio[alimentos[i]] = valor
        items = [s for s in items if tag not in s]

    print(cardapio)
    print(items)


def preenche_refeicao(cardapio_do_dia, refeicao, soup):
    cardapio = {}

    # items = soup.find_all('td')
    # print("items.size = ", len(items))
    items = [s for s in soup.get_text().split("\n") if s]
    # print(items)
    # for item in items:
    #     # help(item)
    #     print([i for i in item.children], " = ", end="")
    #     print([type(i).__name__ for i in item.children])

    # pega tipo de arroz:
    cardapio["arroz_feijao"] = items.pop(0)
    # print(items)

    # salada
    salada = [s.replace("SALADA:", "") for s in items if "SALADA:" in s][0]
    # print(salada)
    cardapio["salada"] = salada
    items = [s for s in items if "SALADA:" not in s]

    # sobremesa
    sobremesa = [s.replace("SOBREMESA:", "") for s in items if "SOBREMESA:" in s][0]
    # print(sobremesa)
    cardapio["sobremesa"] = sobremesa

    items = [s for s in items if "SOBREMESA:" not in s]

    # suco
    suco = [s.replace("SUCO:", "") for s in items if "SUCO:" in s][0]
    # print(suco)
    cardapio["suco"] = suco

    items = [s for s in items if "SUCO:" not in s]


    # observacoes
    observacoes = items.pop().replace("Observações:  ", "")
    # print(observacoes)
    cardapio["observacoes"] = observacoes

    cardapio["prato_principal"] = [items.pop(0).replace("PRATO PRINCIPAL:  ", ""), *items]

    print(items)
    print(cardapio)

    print("\n\n")

    cardapio_do_dia[refeicao] = cardapio
    return cardapio_do_dia


if __name__ == '__main__':
    main()





