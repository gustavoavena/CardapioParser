
from datetime import date
import os
import pyrebase


"""


- Armazenar tokens dos devices em um BD.
    - Qual BD?
    - Armazenar com o que?
        - Last used: Date.
        - Vegetariano: Bool.
        - (Futuramente) Horarios.
        - (Futuramente) Pratos favoritos.
    - Operacoes:
        - UPDATE:
            - Last used
            - Vegetariano
        - CREATE:
            - DeviceNotificationToken
        - DELETE:
            - By HTTP request.
            - By expiration.
        


"""

def setup_firebase():
    config = {
        "apiKey": os.environ.get('FIREBASE_API_KEY'),
        "authDomain": os.environ.get('FIREBASE_PROJECT_ID') + ".firebaseapp.com",
        "databaseURL": os.environ.get('FIREBASE_DB_URL'),
        "storageBucket": os.environ.get('FIREBASE_PROJECT_ID') + ".appspot.com",
        "serviceAccount": "./bandex-c2f82-firebase-adminsdk-msdgz-b90f16f4a6.json"
    }

    firebase = pyrebase.initialize_app(config)

    db = firebase.database()
    return db





def update_or_create_token(token, vegetariano):
    new_dict = {"last_used": date.today().strftime("%y-%m-%d"), "vegetariano": vegetariano }

    db = setup_firebase()
    db.child('tokens').child(token).set(new_dict)


    print("Device token {} registrado com sucesso.".format(token))



def delete_token(token):
    db = setup_firebase()
    db.child('tokens').child(token).remove()

    print("Device token {} removido com sucesso.".format(token))