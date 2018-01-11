
# CardapioParser

## Servidor responsavel pela manutencao do Bandex




Esse app implementado em Flask é a ponte entre a fonte de informação dos cardápios do Bandeco e o app para iOS.

Ele obtem os cardapios e instancia objetos das classes Cardapio e Refeicao. Esse objetos são serializados e salvos como JSON no Firebase Realtime Database. Dessa maneira, mantemos uma separacao bem definida entra a obtencao e a leitura dos cardapios.

Observacoes importantes:

- Eu utilizo dois add-ons do heroku: o scheduler e o Fixie.

    - O scheduler executa tarefas em horarios pre-determinados (mais informacoes embaixo).
    - O Fixie atua como um proxy para que o app tenha um outbound IP fixo e possa se comunicar com o API da prefeitura da UNICAMP (que possui whitelisting por IP). Como esse add-on possui um limite de 500 requests por mes no plano gratis, e importante que eu limite o numero de requests para o API da Unicamp. Esta bem evidente no codigo que muita coisa poderia ser feita de maneira melhor e mais organizada, mas nessas situacoes eu tive que optar por uma solucoes "piorres" por causa dessa limitacao dos requests.


### O que esse web app faz?

- Registra, atualiza e remove os push notifications tokens dos devices que desejam receber push notifications.
    - As informacoes de cada device (e.g. token, preferencias de horarios, etc) tambem sao mantidas no Firebase Realtime Database. As regras granulares de acesso permitem que eu mantenha os cardapios publicos (para serem lidos pelos devices) e os tokens privados (para serem acessados somente com autenticacao e autorizacao).
    - Isso e feito utilizando os endpoints definidos no arquivo `view.py`.

#### Ele utiliza o heroku scheduler para executar as seguintes tarefas:

- Obter os cardapios com o API da prefeitura da UNICAMP e atualizar esses valores no Realtime Database do Firebase. O comando executado é `python heroku_cache.py` (preciso mudar o nome desse arquivo depois).

- Enviar push notifications para os devices nos horarios apropriados.
    - O scheduler executa `python cardapio_notifications.py` a cada 10 minutos, para enviar notificacoes pros devices em cada horario. Esse modulo possui mais informacoes sobre seu funcionamento no proprio codigo.

O firebase tem um limite gigante de requests, entao muitas pessoas podem usar o app sem nos preocuparmos. Alem disso, eu uso o firebase para armazenar os tokens de Push Notification. Ele permite que certas chaves tenham regras de leitura especificas, entao os cardapios ficam publicos e os tokens privados.



### TODO:

- Melhorar essa documentacao (depois vou procurar algum servico que ajuda a gerar documentacao melhor).
- Melhorar a maneira de obter e salvar os cardapios. O fluxo dessa tarefa ta muito complexo, em maior parte por causa do limite de requests que eu tenho com o Fixie.

### Instalacao:

Installing:

You must have on your computer: python 3, pip, virtualenv.


Setup the appropriate environment variables (all listed in the `persistence/environment_vars.py` module).

Copy the path of your python 3 interpreter.
```
virtualenv venv -p [path_to_your_python_interpreter]
source venv/bin/activate
pip install -r requirements.txt
chmod a+x run.py
```

To run the app: `bash startup.sh`
