
from datetime import date, datetime
import os
import pyrebase
from apns2.client import APNsClient, Notification
from apns2.payload import Payload
from unicamp_webservices import get_all_cardapios

from date_services import segunda_a_sexta
import heroku_cache
from firebase import setup_firebase



# Metodos relacionados ao armazenamento dos iOS Device Tokens, fornecidos pelos devices ao se registrarem para Push Notifications.


def update_or_create_token(token, vegetariano):
    """
    Registra device token ou atualiza os seus parametros "last_used" e/ou "vegetariano".

    :param token: token a ser registrado ou atualizado.
    :param vegetariano: preferencia de cardapio do usuario.
    :return: True caso nao haja erros durante o processo.
    """
    new_dict = {"last_used": date.today().strftime("%y-%m-%d"), "vegetariano": vegetariano }

    db = setup_firebase()
    db.child('tokens').child(token).set(new_dict)


    print("Device token {} registrado com sucesso.".format(token))

    return True




def delete_token(token):
    """
    Remove device token do BD (firebase).

    :param token: token a ser removido.
    :return: True caso nao haja erros durante o processo.
    """
    db = setup_firebase()
    db.child('tokens').child(token).remove()

    print("Device token {} removido com sucesso.".format(token))

    return True




# Metodos relacionados ao envio de push notifications.


def get_device_tokens():
    """
    Pega os device tokens no firebase e separa os tradicionais dos vegetarianos.

    :return: uma tupla (toks_trad, toks_veg) contendo os tokens tradicionais e vegetarianos.
    """

    # obtems device tokens dos usuarios registrados
    db = setup_firebase()
    tokens = db.child('tokens').get().val()

    # separa usuarios vegetarianos
    tokens_tradicional = [t for t, d in tokens.items() if d["vegetariano"] == False]
    tokens_vegetariano = [t for t, d in tokens.items() if d["vegetariano"]]

    # print("Tokens tradicionais: ", tokens_tradicional)
    # print("Tokens vegetarianos: ", tokens_vegetariano)

    return tokens_tradicional, tokens_vegetariano



def get_notification_objects(msg_tradicional, msg_vegetariano):
    """

    :param msg_tradicional: mensagem da notificacao do cardapio tradicional.
    :param msg_vegetariano: mensagem da notificacao do cardapio vegetariano.
    :return: objetos de notificacao a serem enviados.
    """
    tokens_tradicional, tokens_vegetariano = get_device_tokens()


    # cria 2 payloads diferentes para tradicional e vegetariano
    payload_tradicional = Payload(alert=msg_tradicional, sound="default", badge=1)
    payload_vegetariano = Payload(alert=msg_vegetariano, sound="default", badge=1)

    # adiciona os objetos Notification (olhar codigo do apns2) para serem enviados em batch.
    notifications = []

    for t in tokens_tradicional:
        notifications.append(Notification(t, payload_tradicional))

    for t in tokens_vegetariano:
        notifications.append(Notification(t, payload_vegetariano))

    return notifications



def push_next_notification(msg_tradicional, msg_vegetariano):
    """
    Utiliza a biblioteca apns2 para enviar push notifications para os usuarios registrados.


    :param msg_tradicional: string de notificacao para o cardapio tradicional.
    :param msg_vegetariano: string de notificacao para o cardapio vegetariano.
    :return: None
    """

    notifications = get_notification_objects(msg_tradicional, msg_vegetariano)


    topic = 'com.Gustavo.Avena.BandecoUnicamp'


    # separa o heroku de production do de teste
    use_sandbox = False if os.environ.get('PRODUCTION_ENVIRONMENT') != None else True


    if os.path.exists('./apns_key.pem'):
        print("Executando no heroku")
        file_path = "./apns_key.pem"
    else: # local development. Usar o certificado armazenado localmente para development.
        print("Usando chave de development localmente...")
        file_path = './../Certificates/bandex_push_notifications_dev_key.pem'

    client = APNsClient(file_path, use_sandbox=use_sandbox, use_alternative_port=False)

    client.send_notification_batch(notifications, topic)

    today = datetime.utcnow()
    print("Push notifications sent on {} UTC.".format(today.strftime("%A, %b %d, %H:%M:%S")))




def cardapio_valido():
    """
    Pega o proximo cardapio disponivel e confere se é do dia de hoje. Retorna None quando nao há cardapio disponivel e
    quando for fim de semana ou feriado.

    :return: o proximo cardapio, se for valido, ou None caso contrário.
    """


    # atualiza o firebase e pega os cardapios ao mesmo tempo. Gastando somente um request do proxy.
    cardapios = heroku_cache.main()

    if cardapios == None:
        cardapios = get_all_cardapios()



    if len(cardapios) == 0:
        return None

    prox = cardapios[0]
    today = date.today().strftime("%Y-%m-%d")

    if prox.data == today:
        return prox
    else:
        print(today)
        print(prox.data)
        return None


def mandar_proxima_refeicao(refeicao):
    """
    Recebendo a refeicao (almoço ou jantar) a ser enviada, esse metodo cria a string da notificação e chama o método para envia-la
    caso exista um cardapio valido (dia útil).


    :param refeicao: string com valor "almoço" ou "jantar", indicando qual a refeicao a ser informada.
    """

    if not segunda_a_sexta():
        print("Nao deve haver notificação no sábado ou domingo.")
        return None


    cardapio = cardapio_valido()

    # h, m = datetime.utcnow().hour - 2, datetime.utcnow().minute
    # hora = "{}:{} - ".format(h, str(m).zfill(2))

    template = "Hoje tem {} no {}."



    if cardapio != None:
        if refeicao == "almoço":
            tradicional = template.format(cardapio.almoco.prato_principal.lower(), refeicao)
            vegetariano = template.format(cardapio.almoco_vegetariano.prato_principal.lower(), refeicao)
        elif refeicao == "jantar":
            tradicional = template.format(cardapio.jantar.prato_principal.lower(), refeicao)
            vegetariano = template.format(cardapio.jantar_vegetariano.prato_principal.lower(), refeicao)
        else:
            print("Erro ao determinar refeicao.")
            return

        push_next_notification(tradicional, vegetariano)
    else:
        print("Agora não há um cardápio válido.")



def testar_notificacao():

    h, m = datetime.utcnow().hour - 2, datetime.utcnow().minute # retiro 2 por causa do horario de verao
    hora = "{}:{} - ".format(h, str(m).zfill(2))

    template = "Hoje tem {} no {}."

    cardapios = get_all_cardapios()
    cardapio = cardapios[0]

    tradicional = template.format(cardapio.almoco.prato_principal.lower(), "almoço")
    vegetariano = template.format(cardapio.almoco_vegetariano.prato_principal.lower(), "almoço")

    push_next_notification(tradicional, vegetariano)



def main():

    today = datetime.utcnow()
    hour = today.hour


    # horario em UTC! horario Brasil = UTC - 3h (talvez diferente em horario de verao).

    if hour >= 13 and hour <= 15:
        refeicao = "almoço"
    elif hour >= 19 and hour <= 21:
        refeicao = "jantar"
    else:
        print("Tentativa de envio de notificação em horário impropio.")
        return



    mandar_proxima_refeicao(refeicao)






if __name__ == '__main__':
    main()


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
