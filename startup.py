import os

# Check Configuring Flask-Cache section for more details


def main():
    try:
        f = open('./bandex_services_account.json', 'w')
        service_account = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
        f.write(service_account)
        f.close()
    except:
        print("Erro ao escrever no arquivo de service account.")


if __name__ == '__main__':
    main()