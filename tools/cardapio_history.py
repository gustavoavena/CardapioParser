import parser
from models.bandex_classes import MyJsonEncoder
import json


try:

    # date_string = date.today().strftime("%y-%m-%d")
    # start_date
    cardapios = parser.get_next_cardapios("2016-09-02", 400)
except Exception as e:
    print("Uso do parser falhou: {}".format(e))
    print(e.with_traceback())
    cardapios = []
else:
    print("Parser executado com sucesso.")





if cardapios != None and len(cardapios) > 0:
    json_data = json.dumps(cardapios, cls=MyJsonEncoder)

    f = open('history.txt', 'w')
    f.write(json_data)
    f.close()
else:
    print("Nenhum cardapio retornado.")
    raise Exception




