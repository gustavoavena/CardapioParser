import os, requests
proxyDict = {
              "http"  : os.environ.get('FIXIE_URL', ''),
              "https" : os.environ.get('FIXIE_URL', '')
            }


r = requests.get("https://webservices.prefeitura.unicamp.br/cardapio_json.php", proxies=proxyDict)

print(r.content)