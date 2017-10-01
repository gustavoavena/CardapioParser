
Esse app implementado em Flask é a ponte entre a fonte de informação dos cardápios do Bandeco (pode ser HTML da pagina da Prefeitura da UNICAMP ou o API fornecido por eles) e o app para iOS.

Ele obtem os cardapios e instancia objetos das classes Cardapio e Refeicao. Esse objetos são serializados e enviados como JSON para o app. Dessa maneira, caso a fonte do cardapio seja alterada, o app não será afetado, contanto que o servidor retorne objetos dessas classes.

O processo:
- Obter dados dos cardápios.
- Instanciar objetos da classe Cardapio.
- Retornar esses objetos em uma lista, no formato JSON.


Além disso, esse servidor implementa um cache.

Installing:

You must have on your computer: python 3, pip, virtualenv.


Clone the repository.
Copy the path of your python 3 interpreter.
Execute: 'virtualenv venv -p [path_to_your_python_interpreter]'.
Execute: 'source venv/bin/activate'
Execute: 'pip install -r requirements.txt'
Execute: 'chmod a+x run.py'

To run the app: 'python run.py'
