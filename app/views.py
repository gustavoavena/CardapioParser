from app import app
from parser import *

@app.route('/')
@app.route('/index')
def index():
    return "Esse app ira fazer o parsing do cardapio da unicamp e retornar um JSON."

@app.route('/date/<string:date>')
def cardapio(date):
    print(date)
    cardapio = cardapio_por_data(date)
    return json.dumps(cardapio, ensure_ascii=True)