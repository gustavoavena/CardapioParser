from BandecoClasses import MyJsonEncoder
import json
from unicamp_webservices import get_all_cardapios


def main():
    try:
        f = open('cardapio_cache', 'w')
        cardapios = get_all_cardapios()
        f.write(json.dumps(cardapios, cls=MyJsonEncoder))
        f.close()
    except Exception as e:
        print()
        print("Exception at heroku_cache: ", e)
    else:
        print("cardapio_cache updated successfully by the heroku_cache script.")


if __name__ == '__main__':
    main()