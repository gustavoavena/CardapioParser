from flask import Flask
# from flask_cache import Cache


app = Flask(__name__)
# cache = Cache(app,config={'CACHE_TYPE': 'simple'})

from app import views
import os

# Check Configuring Flask-Cache section for more details

try:
    f = open('./bandex_services_account.json', 'w')
    service_account = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
    f.write(service_account)
    f.close()
except:
    print("Erro ao escrever no arquivo de service account.")


if __name__ == '__main__':
    app.run()