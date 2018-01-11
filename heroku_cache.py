from models.bandex_classes import MyJsonEncoder
import json
from unicamp_webservices import get_all_cardapios, request_data_from_unicamp
from persistence.firebase import setup_firebase


"""

Esse modulo é responsavel por atualizar os cardapios no Firebase. Ele será executado por um scheduler no heroku em tempos pre-determinados, para tentar
manter os cardapios atualizados sem utilizar muitos requests do nosso proxy.
Eu modifiquei o unicamp_webservices para tambem armazenar o JSON original do API da unicamp, para facilitar a implementacao de notificacoes mais customizaveis.

Agora, a funcao request_data_from_unicamp pega os dados da unicamp e armazena no firebase. Entao esse metodo so eh executado aqui, para nao gastarmos muitos requests do Fixie.

A funcao get_all_cardapios chama a request cardapio, que pega os dados do JSON do firebase, nao diretamente com a unicamp, como era anteriormente.

Assim, eu posso chamar a funcao get_all_cardapios de qualquer lugar da aplicacao sem me preocupar com requests do Fixie. Eu terei que fazer isso muitas vezes, por causa dos horarios de notificacao (que vao ser muitos).

OBS: nao alterei o nome desse arquivo ainda porque tenho que copiar e colar ele no scheduler.

"""

def main():

    db = setup_firebase()

    try:
        # request para unicamp que atualiza o firebase.
        raw_json = request_data_from_unicamp()

        cardapios = get_all_cardapios(raw_json)

        # atualiza os cardapios no firebase.
        if cardapios != None and len(cardapios) > 0:
            json_data = json.dumps(cardapios, cls=MyJsonEncoder)

            # tambem salva os raw_json no firebase para que o modulo de notificacoes nao precise pega-lo da unicamp toda vez.
            db.child("cardapios").set(json_data)
        else:
            print("Nenhum cardapio retornado ao tentar atualizar o Firebase.")
            raise Exception

    except Exception as e:
        print("Exception at heroku_cache: ", e)
        # print(e.__traceback__.__annotations__)
        return None
    else:
        print("Firebase atualizado com sucesso pelo script heroku_cache.")
        return cardapios


    return None






if __name__ == '__main__':
    main()