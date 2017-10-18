import os

def main():
    try:
        service_account = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
        f = open('./bandex_services_account.json', 'w')
        f.write(service_account)
        f.close()

        apns_key = os.environ.get('APNS_PROD_KEY_CONTENT')
        f = open('./apns_key.pem', 'w')
        f.write(apns_key)
        f.close()

        print("Escreveu e fechou os arquivos.")

    except Exception as e:
        print("Erro ao escrever no arquivo de service account e/ou apns_key.pem: ", e)
    else:
        print("Service account configurado com sucesso.")


if __name__ == '__main__':
    main()