import time
from apns import APNs, Frame, Payload



apns = APNs(use_sandbox=True, cert_file='./../Certificates/bandex_push_notifications_dev_cert.pem', key_file='./../Certificates/bandex_push_notifications_dev_key.pem')

# senha dev: bandextest

# Send a notification
token_hex = 'e77c39f01e46911ae21bc93a57dc55ca29d9a81325a22cc4fee340c75a2957d9'
payload = Payload(alert="Hello World!", sound="default", badge=1)
apns.gateway_server.send_notification(token_hex, payload)


#
# # Send an iOS 10 compatible notification
# token_hex = 'e77c39f01e46911ae21bc93a57dc55ca29d9a81325a22cc4fee340c75a2957d9'
# payload = Payload(alert="Hello World!", sound="default", badge=1, mutable_content=True)
#
# apns.gateway_server.send_notification(token_hex, payload)
# # Send multiple notifications in a single transmission
# frame = Frame()
# identifier = 1
# expiry = time.time()+3600
# priority = 10
# frame.add_item('b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b87', payload, identifier, expiry, priority)
# apns.gateway_server.send_notification_multiple(frame)


