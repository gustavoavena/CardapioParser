from app import app
from parser import *

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/date/<string:date>')
def cardapio(date):
    print(date)
    cardapio = cardapio_por_data(date)
    return json.dumps(cardapio, indent=4, ensure_ascii=False)