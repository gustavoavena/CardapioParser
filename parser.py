from bs4 import BeautifulSoup


file = open("cardapio.html", "r")
html_doc = file.read()

soup = BeautifulSoup(html_doc, 'html.parser')

meals = soup.find_all(class_="fundo_cardapio")

# print(meals)
for i,m in enumerate(meals):
    print("i = ", i)
    print(m)
