from app import app
from parser import *
from flask import request

@app.route('/')
@app.route('/index')
def index():
    return "Esse app ira fazer o parsing do cardapio da unicamp e retornar um JSON."

@app.route('/date/<string:date>')
def cardapio(date):

    cardapio = cardapio_por_data(date)
    pprint.pprint(cardapio)
    # print(json.dumps(cardapio, ensure_ascii=True))
    return json.dumps(cardapio, ensure_ascii=True)



# TODO: implementar metodo aqui que busca os cardapios dos proximos next dias uteis.
#

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




# jsonData = {"datas":["2017-06-06","2017-06-07","2017-06-08","2017-06-09","2017-06-12","2017-06-13","2017-06-14"]}


# curl -H "Content-Type: application/json" -X POST -d '{"datas":["2017-06-06","2017-06-07","2017-06-08","2017-06-09","2017-06-12","2017-06-13","2017-06-14"]}' http://127.0.0.1:5000/dates
