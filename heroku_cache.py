from BandecoClasses import MyJsonEncoder
import json
import os
from unicamp_webservices import get_all_cardapios
import pyrebase

def main():

    config = {
        "apiKey": os.environ.get('FIREBASE_API_KEY'),
        "authDomain": os.environ.get('FIREBASE_PROJECT_ID') + ".firebaseapp.com",
        "databaseURL": os.environ.get('FIREBASE_DB_URL'),
        "storageBucket": os.environ.get('FIREBASE_PROJECT_ID') + ".appspot.com",
        "serviceAccount": "./bandex_services_account.json"
    }



    firebase = pyrebase.initialize_app(config)


    db = firebase.database()

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