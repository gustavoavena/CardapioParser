from app import app
from parser import *
from flask import request
import collections


@app.route('/')
@app.route('/index')
def index():
    return "Esse app ira fazer o parsing do cardapio da unicamp e retornar um JSON."

@app.route('/date/<string:date>')
def cardapio(date):

    cardapio = cardapio_por_data(date)
    print(cardapio)
    # print(json.dumps(cardapio, ensure_ascii=True))
    return json.dumps(cardapio.__dict__, ensure_ascii=True)



# TODO: implementar metodo aqui que busca os cardapios dos proximos next dias uteis!!!!
#

# TODO: talvez seja melhor retornar um array de tuplas, onde o primeiro elemento é a data e o sgundo eh um dict
# com o cardapio daquela data...
# recebe um array de datas (em strings) e retorna um json onde as chaves sao as datas e os valores
# os cardapios completos para aquela data.
@app.route('/dates', methods=['POST'])
def cardapios_datas():

    if(request.method == 'POST'):
        data_dict = json.loads(request.data)
        print(data_dict.get('datas'))
        array_cardapios = cardapio_para_datas(data_dict.get('datas'))
        pprint.pprint(array_cardapios)

        json_response = json.dumps(array_cardapios)
        return json_response


    return "Empty"


@app.route('/cardapios/date/<string:date_string>/next/<int:next>', methods=['GET'])
def next_cardapios(date_string, next):
    cardapios = get_next_cardapios(date_string, next)

    json_response = json.dumps(cardapios)
    return json_response




# jsonData = {"datas":["2017-06-06","2017-06-07","2017-06-08","2017-06-09","2017-06-12","2017-06-13","2017-06-14"]}


# curl -H "Content-Type: application/json" -X POST -d '{"datas":["2017-06-06","2017-06-07","2017-06-08","2017-06-09","2017-06-12","2017-06-13","2017-06-14"]}' http://127.0.0.1:5000/dates



"""
Quais metodos eu preciso:


- cardapio_por_data(data_string: string) -> Cardapio
    - OBS: Ele precisa de outros metodos, mas quando mudarmos o API, mudaremos a interface. O que importa
    eh que as rotas tenham acesso a ESSES metodos, com esses parametros e esses retornos.
    
- next_cardapios(date_string: string, next: int) -> [Cardapio]
    - next_weekdays(next: int, start_date: datetime.date = date.today()) -> [String]
    - cardapio_para_datas(data_strings: [string]) -> [Cardapio]


"""