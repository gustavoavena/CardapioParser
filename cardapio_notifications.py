
from datetime import date
import os
import pyrebase
from apns2.client import APNsClient
from apns2.payload import Payload
from unicamp_webservices import get_all_cardapios



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


# TODO: diferenciar normal de vegetarianos!


# TODO: meotodos em date_services, para saber se deve mandar notificacao ou nao e qual refeicao deve ser enviada.


def push_next_notification(mensagem="Hoje teremos ***** para almoçar no bandeco."):

    db = setup_firebase()
    tokens = db.child('tokens').get().val()

    # TODO: separar tradicional de vegetariano



    payload = Payload(alert=mensagem, sound="default", badge=1)
    # TODO: pegar refeicao apropriada.

    topic = 'com.Gustavo.Avena.BandecoUnicamp'

    file_path = ""

    key_file_content = os.environ.get('APNS_PROD_KEY_CONTENT')

    if key_file_content != None:
        f = open("key.pem", "w")
        f.write(key_file_content)

        file_path =  "key.pem"
    else:
        file_path = './../Certificates/bandex_push_notifications_dev_key.pem'

    client = APNsClient(file_path, use_sandbox=True, use_alternative_port=False)

    client.send_notification_batch(tokens, payload, topic)



def cardapio_valido():
    """
    Pega o proximo cardapio disponivel e confere se é do dia de hoje. Retorna None quando nao há cardapio disponivel e
    quando for fim de semana ou feriado.

    :return: o proximo cardapio, se for valido, e None caso contrário.
    """
    cardapios = get_all_cardapios()

    if len(cardapios) == 0:
        return None

    prox = cardapios[0]

    if(prox.data == date.today()):
        return prox
    else:
        return None


def mandar_proxima_refeicao(refeicao):

    cardapio = cardapio_valido()

    template = "O bandeco terá {} hoje no {}."

    if cardapio != None:
        if refeicao == "almoço":
            push_next_notification(template.format(cardapio.almoco.p))






"""
- Armazenar tokens dos devices em um BD.
    - Qual BD?
        - Firebase!!!
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



- Fluxo para mandar notificacao.

- Criar trigger para executar 11am e 17h.
    - Confere se é segunda a sexta.
        - Se for, pega o primeiro cardapio.
        - Confere se é o cardapio do mesmo dia (porque pode ser feriado).

    - Ele chama um metodo que recebe almoco ou jantar como parametro (o trigger da manha passa almoco e o da tarde passa jantar).
        - Esse metodo pega a refeicao, cria uma string e chama o metodo push_next_notification(mensagem).



curl -X PUT -H "Content-Type: application/json" -d '{"token":"e77c39f01e46911ae21bc93a57dc55ca29d9a81325a22cc4fee340c75a2957d9","vegetariano" : false }' 127.0.0.1:5000/tokens



"""
