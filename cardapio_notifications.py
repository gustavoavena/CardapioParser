
from datetime import date, datetime
import os
from apns2.client import APNsClient, Notification
from apns2.payload import Payload
from unicamp_webservices import get_all_cardapios

from date_services import segunda_a_sexta
from persistence.firebase import setup_firebase
import pytz

from persistence import environment_vars

from pprint import pprint

"""

Notas para mim: 

- Armazenar tokens dos devices em um BD.
    - Qual BD?
        - Firebase!!!
    - Armazenar com o que?
        - Last used: Date.
        - Vegetariano: Bool.
        - Horarios para almoco e jantar (nil caso nao queria notificacao para aquela refeicao).
        - (Futuramente) Pratos favoritos.
    - Operacoes:
        - UPDATE:
            - Last used
            - Vegetariano
            - Horarios
        - CREATE:
            - DeviceNotificationToken
        - DELETE:
            - By HTTP request.
            - By expiration.


Como funciona esse modulo:


O usuarios poderao escolher se receberao notificacoes do almoco e/ou jantar e as horas que receberao.

Almoco: 07:00-13:30, com precisao de 30min.
Jantar: 14:00-19:00, com precisao de 30min.



Fluxo para mandar notificacao:

- Criar trigger para executar a cada 10min no heroku scheduler. Esse trigger executa a funcao main desse modulo.
    - Confere se é segunda a sexta.
        - Se for, pega o primeiro cardapio.
        - Confere se é o cardapio do mesmo dia (porque pode ser feriado).

    - Ele chama um metodo que recebe almoco ou jantar como parametro (o trigger da manha passa almoco e o da tarde passa jantar).
        - Esse metodo pega a refeicao, cria uma string e chama o metodo push_next_notification(mensagem).
    - Definir quais usuarios devem receber notificacao naquele momento.
        - Pega todos os tokens, separa os tradicionais dos vegetarianos e filtra para pegar so os que querem notificacao naquele momento.
        - TODO: melhorar isso porque percorrer todos os tokens toda vez e uma solucao muito ineficiente (assintoticamente pelo menos).



curl -X PUT -H "Content-Type: application/json" -d '{"token":"e77c39f01e46911ae21bc93a57dc55ca29d9a81325a22cc4fee340c75a2957d9","vegetariano" : false }' 127.0.0.1:5000/tokens



"""


# Metodos relacionados ao armazenamento dos iOS Device Tokens, fornecidos pelos devices ao se registrarem para Push Notifications.


def update_or_create_token(token, vegetariano, notificacao_almoco="11:00", notificacao_jantar="17:00"):
    """
    Registra device token ou atualiza os seus parametros "last_used" e/ou "vegetariano".

    Acho que tenho que deixas os valores default do almoco e janta como os originais, para manter as notificacoes dos usuarios que nao atualizarem o app.

    :param token: token a ser registrado ou atualizado.
    :param vegetariano: preferencia de cardapio do usuario.
    :return: True caso nao haja erros durante o processo.
    """
    new_dict = {"last_used": date.today().strftime("%y-%m-%d"), "vegetariano": vegetariano }

    if notificacao_almoco is not None:
        new_dict["almoco"] = notificacao_almoco

    if notificacao_jantar is not None:
        new_dict["jantar"] = notificacao_jantar



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

def same_time_with_margin(hora):
    """
    Compara um horario fornecido com o horario atual para decidir se uma notificacao deve ser enviada para o token correspondente a esse horario. Ele leva em consideracao um possivel atraso de ate 3min no heroku scheduler.

    :param hora: horario a ser verificado
    :return: booleano dizendo esta proximo o suficiente a hora atual para receber notificacao no momento.
    """

    if hora is None:
        return False


    tz = pytz.timezone('America/Sao_Paulo')
    today = datetime.now(tz)

    minutes_today = int(today.hour * 60 + today.minute)

    hours, minutes = map(int, hora.split(':'))
    minutes_notification = hours * 60 + minutes

    # print(hora, "{}:{}".format(today.hour, today.minute))
    return abs(minutes_today - minutes_notification) <= 5



def get_device_tokens(refeicao):
    """
    Pega os device tokens no firebase, separa os tradicionais dos vegetarianos e filtra os tokens que devem receber notificacao no momento. Lembrando que o heroku scheduler vai rodar o script de notificacao a cada 10min.


    :return: uma tupla (toks_trad, toks_veg) contendo os tokens tradicionais e vegetarianos.
    """

    # obtems device tokens dos usuarios registrados
    db = setup_firebase()
    tokens = db.child('tokens').get().val()

    # pprint("All tokens: {}".format(tokens))

    if refeicao == "almoço":
        refeicao = "almoco" # consertando inconsistencia nos nomes de chaves e da mensagem...

    try:
        # filtra os tokens que devem receber notificacao no momento.
        tokens = [(t, d) for t, d in tokens.items() if refeicao in d and same_time_with_margin(d[refeicao])]
    except KeyError:
        # o usuario nao quer receber notificacao nessa refeicao.
        print("KeyError em get_device_token!")
        return [], []


    # pprint("Tokens filtrados pelo horario da notificacao: {}".format(tokens))


    # separa usuarios vegetarianos
    tokens_tradicional = [t for t, d in tokens if d["vegetariano"] == False]
    tokens_vegetariano = [t for t, d in tokens if d["vegetariano"]]

    # print("Tokens tradicionais: ", tokens_tradicional)
    # print("Tokens vegetarianos: ", tokens_vegetariano)

    return tokens_tradicional, tokens_vegetariano



def get_notification_objects(msg_tradicional, msg_vegetariano, tokens_tradicional, tokens_vegetariano):
    """

    Instancia os objetos de notificacao utilizados pelo modulo apns2. Para entender mais, olhar a documentacao dessa biblioteca.

    :param msg_tradicional: mensagem da notificacao do cardapio tradicional.
    :param msg_vegetariano: mensagem da notificacao do cardapio vegetariano.
    :return: objetos de notificacao a serem enviados.
    """


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


def setup_apns_client(use_sandbox):
    """
    Configura um cliente do servico apns2. Para mais informacoes, olhar a documentacao e o codigo dessa biblioteca.
    :param use_sandbox:
    :return: um objeto do tipo APNsClient para enviar push notifications.
    """
    try:
        apns_key = environment_vars.APNS_PROD_KEY_CONTENT
        f = open('./apns_key.pem', 'w')
        f.write(apns_key)
        f.close()
    except Exception as e:
        os.remove('./apns_key.pem')
        print("Erro ao escrever no arquivo apns_key.pem: ", e)

    if os.path.exists('./apns_key.pem'):
        print("Executando no heroku")
        file_path = "./apns_key.pem"
    else:  # local development. Usar o certificado armazenado localmente para development.
        print("Usando chave de development localmente...")
        file_path = './../Certificates/bandex_push_notifications_dev_key.pem'

    client = APNsClient(file_path, use_sandbox=use_sandbox, use_alternative_port=False)

    return client

def push_next_notification(msg_tradicional, msg_vegetariano, refeicao):
    """
    Utiliza a biblioteca apns2 para enviar push notifications para os usuarios registrados.


    :param msg_tradicional: string de notificacao para o cardapio tradicional.
    :param msg_vegetariano: string de notificacao para o cardapio vegetariano.
    :return: None
    """

    # separa tradicional e vegetariano e filtra tokens que querem receber notificacao agora para a refeicao fornecida.
    tokens_tradicional, tokens_vegetariano = get_device_tokens(refeicao)

    # instancia objetos de notificacao a serem enviados usando a biblioteca apns2.
    notifications = get_notification_objects(msg_tradicional, msg_vegetariano, tokens_tradicional, tokens_vegetariano)

    topic = 'com.Gustavo.Avena.BandecoUnicamp'

    # IMPORTANTE: define se estamos em development ou production! Com use_sandbox = True, os devices em modo teste recebem notificacoes. MUITO cuidado ao mexer aqui.
    use_sandbox = False if os.environ.get('PRODUCTION_ENVIRONMENT') != None else True


    client = setup_apns_client(use_sandbox)
    response = client.send_notification_batch(notifications, topic)

    # pprint(response)

    successful = [t for t, d in response.items() if d == "Success"]
    failed = [t for t, d in response.items() if d != "Success"]




    tz = pytz.timezone('America/Sao_Paulo')
    today = datetime.now(tz)
    env_name = "[TESTING] " if use_sandbox else ""

    print("{}Push notifications sent successfully on {} to {} devices.".format(env_name, today.strftime("%A, %b %d, %H:%M:%S"), len(successful)))
    print("Notifications failed for {} devices.".format(len(failed)))

    if(len(failed) > 0):
        pprint([d for t, d in response.items() if d != "Success"])




def cardapio_valido():
    """
    Pega o proximo cardapio disponivel e confere se é do dia de hoje. Retorna None quando nao há cardapio disponivel ou
    quando for fim de semana ou feriado.

    :return: o proximo cardapio, se for valido, ou None caso contrário.
    """

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

        push_next_notification(tradicional, vegetariano, refeicao)
    else:
        print("Agora não há um cardápio válido.")



def testar_notificacao():
    """
    Funcao para testar o envio de notificacoes.

    TODO: refatorar isso para mandar notificacoes para todos os tokens em development, independente do horario da notificacao.

    """

    template = "Hoje tem {} no {}."

    cardapios = get_all_cardapios()
    cardapio = cardapios[0]

    tradicional = template.format(cardapio.almoco.prato_principal.lower(), "almoço")
    vegetariano = template.format(cardapio.almoco_vegetariano.prato_principal.lower(), "almoço")

    tz = pytz.timezone('America/Sao_Paulo')
    today = datetime.now(tz)
    hour = today.hour

    if hour >= 7 and hour <= 13:
        refeicao = "almoço"
    elif hour >= 14 and hour <= 19:
        refeicao = "jantar"

    push_next_notification(tradicional, vegetariano, refeicao)



def main():

    # fuso horario sempre certo (independente do horario de verao).
    tz = pytz.timezone('America/Sao_Paulo')
    today = datetime.now(tz)
    hour = today.hour


    if hour >= 7 and hour <= 13:
        refeicao = "almoço"
    elif hour >= 14 and hour <= 19:
        refeicao = "jantar"
    else:
        print("Tentativa de envio de notificação em horário impropio.")
        return



    mandar_proxima_refeicao(refeicao)






if __name__ == '__main__':
    main()


