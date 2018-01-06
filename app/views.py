from app import app
import parser
from flask import request
from models.bandex_classes import *
import cardapio_notifications
import unicamp_webservices
from datetime import date


@app.route('/')
@app.route('/index')
def index():
    return "Bem vindo ao servidor do Bandex. Esse app ira se comunicar com o API da UNICAMP e vai instanciar objetos para serem utilizados no app para iOS. Além disso, ele é responsável pelo registro dos device tokens e pelas notificações push."


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



@app.route('/tokens', methods=['PUT', 'POST'])
def create_update_token():
    """
    Recebe JSON no formato: {"token": <token_id: string>, "vegetariano": <bool>, "almoco": <string>, "jantar": <string> }

    Obs: almoco e jantar sao strings que representam o horario da notificacao (e.g. "13:00", "18:00"). Caso seja None, o usuario nao quer receber notificacao daquela refeicao.


    :return:
    """
    data = json.loads(request.data)
    print(data)

    ok = cardapio_notifications.update_or_create_token(**data)

    return "Device token registrado com sucesso" if ok else ("ERRO ao registrar device token", 500)



@app.route('/tokens/<string:token>', methods=['DELETE'])
def delete_token(token):

    ok = cardapio_notifications.delete_token(token)

    return "Device token removido com sucesso" if ok else ("ERRO ao removed device token", 500)








# jsonData = {"datas":["2017-06-06","2017-06-07","2017-06-08","2017-06-09","2017-06-12","2017-06-13","2017-06-14"]}


# curl -H "Content-Type: application/json" -X POST -d '{"datas":["2017-06-06","2017-06-07","2017-06-08","2017-06-09","2017-06-12","2017-06-13","2017-06-14"]}' http://127.0.0.1:5000/dates


