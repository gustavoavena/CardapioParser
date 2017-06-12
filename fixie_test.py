import os, requests
proxyDict = {
              "http"  : os.environ.get('FIXIE_URL', ''),
              "https" : os.environ.get('FIXIE_URL', '')
            }


r = requests.get('http://bandex.herokuapp.com', proxies=proxyDict)