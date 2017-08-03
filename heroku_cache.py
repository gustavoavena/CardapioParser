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
        "storageBucket": os.environ.get('FIREBASE_PROJECT_ID') + ".appspot.com"
    }



    firebase = pyrebase.initialize_app(config)


    db = firebase.database()

    try:
        f = open('cardapio_cache', 'w')
        cardapios = get_all_cardapios()
        json_data = json.dumps(cardapios, cls=MyJsonEncoder)
        f.write(json_data)
        db.child("cardapios").set(json_data)
        f.close()
    except Exception as e:
        print()
        print("Exception at heroku_cache: ", e)
    else:
        print("cardapio_cache and firebase updated successfully by the heroku_cache script.")






if __name__ == '__main__':
    main()