import os, requests
from BandecoClasses import *
import date_services

UNICAMP_WEBSERVICES_URL = "https://webservices.prefeitura.unicamp.br/cardapio_json.php"
from app import cache

# def cardapio_por_data(data_string):



# def cardapio_para_datas(data_strings):


# @cache.memoize(timeout=60 * 5)  # cache com timeout de 5min
# def get_next_cardapios(date_string, next)