import os
import pyrebase


"""
Responsavel pela configuracao do firebase.


"""


def setup_firebase():
    """
    Instancia objeto de acesso do BD Firebase.

    :return: o objeto do BD Firebase instanciado.
    """
    config = {
        "apiKey": os.environ.get('FIREBASE_API_KEY'),
        "authDomain": os.environ.get('FIREBASE_PROJECT_ID') + ".firebaseapp.com",
        "databaseURL": os.environ.get('FIREBASE_DB_URL'),
        "storageBucket": os.environ.get('FIREBASE_PROJECT_ID') + ".appspot.com",
        "serviceAccount": "./bandex_services_account.json"
    }

    firebase = pyrebase.initialize_app(config)

    db = firebase.database()
    return db