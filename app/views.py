from app import app
import parser
from BandecoClasses import *
import unicamp_webservices
from datetime import date


@app.route('/')
@app.route('/index')
def index():
    return "Esse app ira fazer o parsing do cardapio da unicamp e retornar um JSON."


@app.route('/cardapios_test', methods=['GET'])
def get_all_cardapios():
    cardapios = unicamp_webservices.get_all_cardapios()



    cardapios = [c for c in cardapios if type(c) is Cardapio]


    if len(cardapios) == 0:
        return None, 500

    if len(cardapios) > 10:
        cardapios = cardapios[:10] # limita o retorno a 10 cardapios

    json_response = json.dumps(cardapios, cls=MyJsonEncoder)

    # print("json_response: ", json_response)
    return json_response, 200


@app.route('/parser', methods=['GET'])
def parser_test():
    date_string = date.today().strftime("%y-%m-%d")
    cardapios = parser.get_next_cardapios(date_string, 10)
    print(cardapios)
    return json.dumps(cardapios, cls=MyJsonEncoder)


@app.route('/cardapios/date/<string:date_string>/next/<int:next>', methods=['GET'])
def get_cardapios_date_next(date_string):
    cardapios = parser.get_next_cardapios(date_string, 10)

    # json_response = json.dumps(cardapios, cls=MyJsonEncoder)
    return cardapios









# jsonData = {"datas":["2017-06-06","2017-06-07","2017-06-08","2017-06-09","2017-06-12","2017-06-13","2017-06-14"]}


# curl -H "Content-Type: application/json" -X POST -d '{"datas":["2017-06-06","2017-06-07","2017-06-08","2017-06-09","2017-06-12","2017-06-13","2017-06-14"]}' http://127.0.0.1:5000/dates


