import pyrebase
import environment_vars


"""
Responsavel pela configuracao do firebase.


"""


def setup_firebase():
    """
    Instancia objeto de acesso do BD Firebase.

    :return: o objeto do BD Firebase instanciado.
    """
    config = {
        "apiKey": environment_vars.FIREBASE_API_KEY,
        "authDomain": environment_vars.FIREBASE_PROJECT_ID,
        "databaseURL": environment_vars.FIREBASE_DB_URL,
        "storageBucket": environment_vars.FIREBASE_PROJECT_ID,
        "serviceAccount": "./bandex_services_account.json"
    }

    try:
        service_account = environment_vars.FIREBASE_SERVICE_ACCOUNT
        f = open('./bandex_services_account.json', 'w')
        f.write(service_account)
        f.close()

    except Exception as e:
        print("Erro ao escrever no arquivo de service account: ", e)
    else:
        print("Service account configurado com sucesso.")

    firebase = pyrebase.initialize_app(config)

    db = firebase.database()
    return db