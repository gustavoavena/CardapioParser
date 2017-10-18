import os
from envparse import env
# Check Configuring Flask-Cache section for more details


def main():
    try:
        service_account = env.json('FIREBASE_SERVICE_ACCOUNT')
        f = open("./bandex_services_account.json", "w")
        f.write(service_account)
        f.close()
    except Exception as e:
        print("Erro ao escrever no arquivo de service account: ", e)
    else:
        print("Service account configurado com sucesso.")


if __name__ == '__main__':
    main()