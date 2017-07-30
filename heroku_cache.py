# from datetime import date
# from parser import get_next_cardapios
from BandecoClasses import MyJsonEncoder
import json
from unicamp_webservices import get_all_cardapios


def main():
    try:
        f = open('cardapio_cache', 'w')
        cardapios = get_all_cardapios()

        # date_string = date.today().strftime("%y-%m-%d")
        # cardapios = get_next_cardapios(date_string, 5)
        f.write(json.dumps(cardapios, cls=MyJsonEncoder))
        f.close()
    except Exception as e:
        print()
        print("Exception at heroku_cache: ", e)
    else:
        print("cardapio_cache updated successfully by the heroku_cache script.")


if __name__ == '__main__':
    main()