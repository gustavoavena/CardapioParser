
from datetime import date
import os
import pyrebase
from apns2.client import APNsClient
from apns2.payload import Payload

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
            
            
            

curl -X PUT -H "Content-Type: application/json" -d '{"token":"e77c39f01e46911ae21bc93a57dc55ca29d9a81325a22cc4fee340c75a2957d9","vegetariano" : false }' 127.0.0.1:5000/tokens
        


"""

# Metodos relacionados ao armazenamento dos iOS Device Tokens, fornecidos pelos devices ao se registrarem para Push Notifications.


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

    return True




def delete_token(token):
    db = setup_firebase()
    db.child('tokens').child(token).remove()

    print("Device token {} removido com sucesso.".format(token))

    return True


# Metodos relacionados ao envio de push notifications.





def push_next_notification():

    db = setup_firebase()
    tokens = db.child('tokens').get().val()



    # token_hex = 'e77c39f01e46911ae21bc93a57dc55ca29d9a81325a22cc4fee340c75a2957d9'

    payload = Payload(alert="Hello World!", sound="default", badge=1)
    # TODO: pegar refeicao apropriada.


    topic = 'com.Gustavo.Avena.BandecoUnicamp'
    client = APNsClient('./../Certificates/bandex_push_notifications_dev_key.pem', use_sandbox=True, use_alternative_port=False)

    client.send_notification_batch(tokens, payload, topic)

