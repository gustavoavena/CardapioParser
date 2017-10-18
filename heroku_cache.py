from BandecoClasses import MyJsonEncoder
import json
from unicamp_webservices import get_all_cardapios
from firebase import setup_firebase


"""

Esse modulo é responsavel por atualizar os cardapios no Firebase. Ele será executado por um scheduler no heroku em tempos pre-determinados, para tentar
manter os cardapios atualizados sem utilizar muitos requests do nosso proxy.

OBS: nao alterei seu nome ainda porque tenho que copiar e colar ele no scheduler.

"""

def main():

    db = setup_firebase()

    try:
        cardapios = get_all_cardapios()

        if cardapios != None and len(cardapios) > 0:
            json_data = json.dumps(cardapios, cls=MyJsonEncoder)
            db.child("cardapios").set(json_data)
        else:
            print("Nenhum cardapio retornado ao tentar atualizar o Firebase.")
            raise Exception

    except Exception as e:
        print("Exception at heroku_cache: ", e)
        return None
    else:
        print("Firebase atualizado com sucesso pelo script heroku_cache.")
        return cardapios


    return None






if __name__ == '__main__':
    main()