import os

FIREBASE_API_KEY = os.environ.get('FIREBASE_API_KEY')
FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID') + ".firebaseapp.com"
FIREBASE_DB_URL = os.environ.get('FIREBASE_DB_URL')
FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID') + ".appspot.com"

FIREBASE_SERVICE_ACCOUNT = os.environ.get('FIREBASE_SERVICE_ACCOUNT')


APNS_PROD_KEY_CONTENT = os.environ.get('APNS_PROD_KEY_CONTENT')

FIXIE_URL = os.environ.get('FIXIE_URL', '')