from app import app
from parser import *
import unicamp_webservices
from datetime import date



@app.route('/')
@app.route('/index')
def index():
    return "Esse app ira fazer o parsing do cardapio da unicamp e retornar um JSON."


@app.route('/cardapios', methods=['GET'])
def get_all_cardapios():
    cardapios = unicamp_webservices.get_all_cardapios()

    print("buscando todos os cardapios disponiveis...")
    # print(cardapios)

    if len(cardapios) == 0: # o unicamp webservices nao retornou nada.
        date_string = date.today().strftime("%y-%m-%d")
        cardapios = get_cardapios_date_next(date_string, 5)

    cardapios = [c for c in cardapios if type(c) is Cardapio]


    if len(cardapios) == 0:
        return None, 500

    json_response = json.dumps(cardapios, cls=MyJsonEncoder)

    # print(json_response)
    return json_response, 200



@app.route('/cardapios/date/<string:date_string>', methods=['GET'])
def get_cardapios_date(date_string):
    cardapio = cardapio_por_data(date_string)
    json_response = json.dumps(cardapio, cls=MyJsonEncoder)
    return json_response


@app.route('/cardapios/date/<string:date_string>/next/<int:next>', methods=['GET'])
def get_cardapios_date_next(date_string, next):
    cardapios = get_next_cardapios(date_string, next)

    # json_response = json.dumps(cardapios, cls=MyJsonEncoder)
    return cardapios




"""
Quais metodos eu preciso AQUI:


- cardapio_por_data(data_string: string) -> Cardapio
    - OBS: Ele precisa de outros metodos, mas quando mudarmos o API, mudaremos a interface. O que importa
    eh que as rotas tenham acesso a ESSES metodos, com esses parametros e esses retornos.

- next_cardapios(date_string: string, next: int) -> [Cardapio]
    - next_weekdays(next: int, start_date: datetime.date = date.today()) -> [String]
    - cardapio_para_datas(data_strings: [string]) -> [Cardapio]


"""





# jsonData = {"datas":["2017-06-06","2017-06-07","2017-06-08","2017-06-09","2017-06-12","2017-06-13","2017-06-14"]}


# curl -H "Content-Type: application/json" -X POST -d '{"datas":["2017-06-06","2017-06-07","2017-06-08","2017-06-09","2017-06-12","2017-06-13","2017-06-14"]}' http://127.0.0.1:5000/dates


