# import time
# from apns import APNs, Frame, Payload
#
#
#
# apns = APNs(use_sandbox=True, cert_file='./../Certificates/bandex_push_notifications_dev_cert.pem', key_file='./../Certificates/bandex_push_notifications_dev_key.pem')
#
# # senha dev: bandextest
#
# # Send a notification
# token_hex = 'e77c39f01e46911ae21bc93a57dc55ca29d9a81325a22cc4fee340c75a2957d9'
# payload = Payload(alert="Hello World!", sound="default", badge=1)
# apns.gateway_server.send_notification(token_hex, payload)
#
#
# #
# # # Send an iOS 10 compatible notification
# # token_hex = 'e77c39f01e46911ae21bc93a57dc55ca29d9a81325a22cc4fee340c75a2957d9'
# # payload = Payload(alert="Hello World!", sound="default", badge=1, mutable_content=True)
# #
# # apns.gateway_server.send_notification(token_hex, payload)
#
#
# # Send multiple notifications in a single transmission
# frame = Frame()
# identifier = 1
# expiry = time.time()+3600
# priority = 10
# frame.add_item('e77c39f01e46911ae21bc93a57dc55ca29d9a81325a22cc4fee340c75a2957d9', payload, identifier, expiry, priority)
# apns.gateway_server.send_notification_multiple(frame)


from apns2.client import APNsClient
from apns2.payload import Payload

token_hex = 'e77c39f01e46911ae21bc93a57dc55ca29d9a81325a22cc4fee340c75a2957d9'
payload = Payload(alert="Hello World!", sound="default", badge=1)
topic = 'com.Gustavo.Avena.BandecoUnicamp'
client = APNsClient('./../Certificates/bandex_push_notifications_dev_key.pem', use_sandbox=True, use_alternative_port=False)
client.send_notification(token_hex, payload, topic)