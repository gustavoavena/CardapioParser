import requests
import pprint
from enum import Enum
import json


class Refeicao(Enum):
    ALMOCO = "Almoço"
    ALMOCO_VEGETARIANO = "Almoço Vegetariano"
    JANTAR = "Jantar"
    JANTAR_VEGETARIANO = "Jantar Vegetariano"

class ItemCardapio(Enum):
    ARROZ_FEIJAO = "arroz_feijao"
    PRATO_PRINCIPAL = "prato_principal"
    SALADA = "salada"
    SOBREMESA = "sobremesa"
    SUCO = "suco"
    OBSERVACOES = "observacoes"


# pega o cardapio de uma data, dada a string desta data no formato yyyy-MM-dd. Retorna um dicionario representando o cardapio do dia.
# def cardapio_por_data(date):

# retorna um array de cardapios para as datas
# def cardapio_para_datas(dates):




if __name__ == '__main__':
    main()


