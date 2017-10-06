from apns2.client import APNsClient
from apns2.payload import Payload


# Script para testar o uso da library apns para mandar push notifications.





payload = Payload(alert="Hello World!", sound="default", badge=1)
topic = 'com.Gustavo.Avena.BandecoUnicamp'
client = APNsClient('./../Certificates/bandex_push_notifications_dev_key.pem', use_sandbox=True, use_alternative_port=False)
client.send_notification(token_hex, payload, topic)