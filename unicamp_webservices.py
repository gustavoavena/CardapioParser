import os, requests
from BandecoClasses import *
import date_services

UNICAMP_WEBSERVICES_URL = "https://webservices.prefeitura.unicamp.br/cardapio_json.php"
from app import cache
import pprint


JSON_RESPONSE = b'{"CARDAPIO":[{"DATA":"2017-06-12","TIPO":"Almo\\u00e7o","ACOMPANHAMENTO":"ARROZ E FEIJ\\u00c3O","PRATO PRINCIPAL":"STROGONOFF DE CARNE","GUARNICAO":"BATATA FRITA LISA","PTS":"PTS COM MANDIOQUINHA","SALADA":"ALFACE","SOBREMESA":"MA\\u00c7\\u00c3","SUCO":"CAJ\\u00da","OBS":"O CARD\\u00c1PIO CONT\\u00c9M GL\\u00daTEN NO P\\u00c3O E NO STROGONOFF DE CARNE E CONT\\u00c9M LACTOSE NO STROGONOFF DE CARNE. N\\u00c3O CONT\\u00c9M OVOS.\\r\\n<font color = \\"red\\"> N\\u00c3O ESQUE\\u00c7A SUA CANECA ! <\\/font>"},{"DATA":"2017-06-12","TIPO":"Almo\\u00e7o Vegetariano","ACOMPANHAMENTO":"ARROZ INTEGRAL E FEIJ\\u00c3O","PRATO PRINCIPAL":"STROGONOFF VEGANO","GUARNICAO":"BATATA PALHA","PTS":"-","SALADA":"ALFACE","SOBREMESA":"MA\\u00c7\\u00c3","SUCO":"CAJ\\u00da","OBS":"O CARD\\u00c1PIO CONT\\u00c9M GL\\u00daTEN NO P\\u00c3O E NO STROGONOFF VEGANO. N\\u00c3O CONT\\u00c9M OVOS E LACTOSE.\\r\\n<font color = \\"red\\"> N\\u00c3O ESQUE\\u00c7A SUA CANECA ! <\\/font>"},{"DATA":"2017-06-12","TIPO":"Jantar","ACOMPANHAMENTO":"ARROZ E FEIJ\\u00c3O","PRATO PRINCIPAL":"BIFE PAULISTA","GUARNICAO":"n\\u00e3o informado","PTS":"PTS COM VAGEM","SALADA":"CENOURA RALADA","SOBREMESA":"BANANA","SUCO":"CAJ\\u00da","OBS":"O CARD\\u00c1PIO CONT\\u00c9M GL\\u00daTEN NO P\\u00c3O E CONT\\u00c9M TRA\\u00c7OS DE LACTOSE NO BIFE PAULISTA. N\\u00c3O CONT\\u00c9M OVOS .\\r\\n<font color = \\"red\\"> N\\u00c3O ESQUE\\u00c7A SUA CANECA ! <\\/font>"},{"DATA":"2017-06-12","TIPO":"Jantar Vegetariano","ACOMPANHAMENTO":"ARROZ INTEGRAL E FEIJ\\u00c3O","PRATO PRINCIPAL":"TORTA DE SOJA E AVEIA AO MOLHO DE MANDIOQUINHA","GUARNICAO":"-","PTS":"-","SALADA":"CENOURA RALADA","SOBREMESA":"BANANA","SUCO":"CAJ\\u00da","OBS":"O CARD\\u00c1PIO CONT\\u00c9M GL\\u00daTEN NO P\\u00c3O E NA TORTA DE SOJA E AVEIA. N\\u00c3O CONT\\u00c9M OVOS E LACTOSE.\\r\\n<font color = \\"red\\"> N\\u00c3O ESQUE\\u00c7A SUA CANECA ! <\\/font>"},{"DATA":"2017-06-13","TIPO":"Almo\\u00e7o","ACOMPANHAMENTO":"ARROZ E FEIJ\\u00c3O","PRATO PRINCIPAL":"CARNE MO\\u00cdDA COM VAGEM","GUARNICAO":"MACARR\\u00c3O AO SUGO","PTS":"PTS COM VAGEM","SALADA":"MISTA DE GR\\u00c3O DE BICO","SOBREMESA":"BARRA DE CEREAL COM CHOCOLATE","SUCO":"TANGERINA","OBS":"O CARD\\u00c1PIO CONT\\u00c9M GL\\u00daTEN NO P\\u00c3O, MACARR\\u00c3O AO SUGO E NA BARRA DE CEREAL. CONT\\u00c9M LACTOSE E DERIVADOS DE SOJA NA BARRA DE CEREAL.\\r\\n<font color = \\"red\\"> N\\u00c3O ESQUE\\u00c7A SUA CANECA ! <\\/font>"},{"DATA":"2017-06-13","TIPO":"Almo\\u00e7o Vegetariano","ACOMPANHAMENTO":"ARROZ INTEGRAL E FEIJ\\u00c3O","PRATO PRINCIPAL":"MACARR\\u00c3O INTEGRAL AO SUGO","GUARNICAO":"n\\u00e3o informado","PTS":"n\\u00e3o informado","SALADA":"MISTA DE GR\\u00c3O DE BICO","SOBREMESA":"FRUTA","SUCO":"TANGERINA","OBS":"O CARD\\u00c1PIO CONT\\u00c9M GL\\u00daTEN NO P\\u00c3O E NO MACARR\\u00c3O INTEGRAL AO SUGO E N\\u00c3O CONT\\u00c9M LACTOSE.\\r\\n<font color = \\"red\\"> N\\u00c3O ESQUE\\u00c7A SUA CANECA ! <\\/font>"},{"DATA":"2017-06-13","TIPO":"Jantar","ACOMPANHAMENTO":"ARROZ E FEIJ\\u00c3O","PRATO PRINCIPAL":"ISCA DE CARNE COM LEGUMES","GUARNICAO":"n\\u00e3o informado","PTS":"PTS COM CENOURA E BATATA","SALADA":"REPOLHO COM RABANETE","SOBREMESA":"GELATINA DE ABACAXI","SUCO":"TANGERINA","OBS":"O CARD\\u00c1PIO CONT\\u00c9M GL\\u00daTEN NO P\\u00c3O. N\\u00c3O CONT\\u00c9M OVOS E LACTOSE.\\r\\n<font color = \\"red\\"> N\\u00c3O ESQUE\\u00c7A SUA CANECA ! <\\/font>"},{"DATA":"2017-06-13","TIPO":"Jantar Vegetariano","ACOMPANHAMENTO":"ARROZ INTEGRAL E FEIJ\\u00c3O","PRATO PRINCIPAL":"STROGONOFF VEGANO","GUARNICAO":"n\\u00e3o informado","PTS":"n\\u00e3o informado","SALADA":"REPOLHO COM RABANETE","SOBREMESA":"FRUTA","SUCO":"TANGERINA","OBS":"O CARD\\u00c1PIO CONT\\u00c9M GL\\u00daTEN NO P\\u00c3O E NO STROGONOFF VEGANO. N\\u00c3O CONT\\u00c9M OVOS E LACTOSE.\\r\\n<font color = \\"red\\"> N\\u00c3O ESQUE\\u00c7A SUA CANECA ! <\\/font>"},{"DATA":"2017-06-14","TIPO":"Almo\\u00e7o","ACOMPANHAMENTO":"ARROZ E FEIJ\\u00c3O","PRATO PRINCIPAL":"OVO MEXIDO COM SALSICHA","GUARNICAO":"JARDINEIRA DE LEGUMES (BATATA, CENOURA E VAGEM)","PTS":"PTS COM BETERRABA","SALADA":"PEPINO","SOBREMESA":"TANGERINA MURCOTE","SUCO":"UVA","OBS":"O CARD\\u00c1PIO CONT\\u00c9M GL\\u00daTEN NO P\\u00c3O E N\\u00c3O CONT\\u00c9M  LACTOSE.\\r\\n<font color = \\"red\\"> N\\u00c3O ESQUE\\u00c7A SUA CANECA ! <\\/font>"},{"DATA":"2017-06-14","TIPO":"Almo\\u00e7o Vegetariano","ACOMPANHAMENTO":"ARROZ INTEGRAL E FEIJ\\u00c3O","PRATO PRINCIPAL":"SOJA XADREZ","GUARNICAO":"JARDINEIRA DE LEGUMES (BATATA, CENOURA E VAGEM)","PTS":"n\\u00e3o informado","SALADA":"PEPINO","SOBREMESA":"TANGERINA MURCOTE","SUCO":"UVA","OBS":"O CARD\\u00c1PIO CONT\\u00c9M GL\\u00daTEN NO P\\u00c3O. N\\u00c3O CONT\\u00c9M OVOS E LACTOSE.\\r\\n<font color = \\"red\\"> N\\u00c3O ESQUE\\u00c7A SUA CANECA ! <\\/font>"},{"DATA":"2017-06-14","TIPO":"Jantar","ACOMPANHAMENTO":"ARROZ E FEIJ\\u00c3O","PRATO PRINCIPAL":"CARNE ASSADA AO MOLHO DE ABACAXI","GUARNICAO":"ARROZ CARRETEIRO","PTS":"PTS COM CAR\\u00c1","SALADA":"SOJA COM TOMATE","SOBREMESA":"MA\\u00c7\\u00c3","SUCO":"UVA","OBS":"O CARD\\u00c1PIO CONT\\u00c9M GL\\u00daTEN NO P\\u00c3O E N\\u00c3O CONT\\u00c9M OVOS E LACTOSE.\\r\\n<font color = \\"red\\"> N\\u00c3O ESQUE\\u00c7A SUA CANECA ! <\\/font>"},{"DATA":"2017-06-14","TIPO":"Jantar Vegetariano","ACOMPANHAMENTO":"ARROZ INTEGRAL E FEIJ\\u00c3O","PRATO PRINCIPAL":"CUSCUZ VEGETARIANO","GUARNICAO":"n\\u00e3o informado","PTS":"n\\u00e3o informado","SALADA":"SOJA COM TOMATE","SOBREMESA":"MA\\u00c7\\u00c3","SUCO":"UVA","OBS":"O CARD\\u00c1PIO CONT\\u00c9M GL\\u00daTEN NO P\\u00c3O E N\\u00c3O CONT\\u00c9M OVOS E LACTOSE.\\r\\n<font color = \\"red\\"> N\\u00c3O ESQUE\\u00c7A SUA CANECA ! <\\/font>"},{"DATA":"2017-06-19","TIPO":"Almo\\u00e7o","ACOMPANHAMENTO":"ARROZ E FEIJ\\u00c3O","PRATO PRINCIPAL":"ALM\\u00d4NDEGA ACEBOLADA","GUARNICAO":"CREME DE MILHO","PTS":"PTS COM AB\\u00d3BORA","SALADA":"ACELGA","SOBREMESA":"IOGURTE","SUCO":"ABACAXI","OBS":"O CARD\\u00c1PIO CONT\\u00c9M GL\\u00daTEN NO P\\u00c3O, ALM\\u00d4NDEGA E NO CREME DE MILHO. CONT\\u00c9M LACTOSE NO CREME DE MILHO E NO IOGURTE.  N\\u00c3O CONT\\u00c9M OVOS.\\r\\n<font color = \\"red\\"> N\\u00c3O ESQUE\\u00c7A SUA CANECA ! <\\/font>"},{"DATA":"2017-06-19","TIPO":"Almo\\u00e7o Vegetariano","ACOMPANHAMENTO":"ARROZ E FEIJ\\u00c3O","PRATO PRINCIPAL":"QUIBE DE BERINJELA COM CENOURA","GUARNICAO":"CREME DE MILHO","PTS":"n\\u00e3o informado","SALADA":"ACELGA","SOBREMESA":"FRUTA","SUCO":"ABACAXI","OBS":"O CARD\\u00c1PIO CONT\\u00c9M GL\\u00daTEN NO P\\u00c3O, NO QUIBE DE BERINJELA COM CENOURA E NO CREME DE MILHO. N\\u00c3O CONT\\u00c9M OVOS E LACTOSE.\\r\\n<font color = \\"red\\"> N\\u00c3O ESQUE\\u00c7A SUA CANECA ! <\\/font>"},{"DATA":"2017-06-19","TIPO":"Jantar","ACOMPANHAMENTO":"ARROZ E FEIJ\\u00c3O","PRATO PRINCIPAL":"OVO MEXIDO COM LINGUI\\u00c7A","GUARNICAO":"CHUCHU REFOGADO","PTS":"PTS COM BERINJEA","SALADA":"ALFACE COM R\\u00daCULA","SOBREMESA":"BARRA DE CEREAL","SUCO":"ABACAXI","OBS":"O CARD\\u00c1PIO CONT\\u00c9M GL\\u00daTEN NO P\\u00c3O E NA BARRA DE CEREAL. \\r\\nCONT\\u00c9M LACTOSE E DERIVADOS DE SOJA NA BARRA DE CEREAL.\\r\\nN\\u00c3O CONT\\u00c9M OVOS.\\r\\n<font color = \\"red\\"> N\\u00c3O ESQUE\\u00c7A SUA CANECA ! <\\/font>"},{"DATA":"2017-06-19","TIPO":"Jantar Vegetariano","ACOMPANHAMENTO":"ARROZ INTEGRAL E FEIJ\\u00c3O","PRATO PRINCIPAL":"SOJA COZIDA COM LEGUMES","GUARNICAO":"CHUCHU REFOGADO","PTS":"n\\u00e3o informado","SALADA":"ALFACE COM R\\u00daCULA","SOBREMESA":"FRUTA","SUCO":"ABACAXI","OBS":"O CARD\\u00c1PIO CONT\\u00c9M GL\\u00daTEN NO P\\u00c3O E N\\u00c3O CONT\\u00c9M OVOS E LACTOSE.\\r\\n<font color = \\"red\\"> N\\u00c3O ESQUE\\u00c7A SUA CANECA ! <\\/font>"}]}'



def limpa_chaves(refeicoes_list):
    for ref in refeicoes_list:
        try:
            for key in list(ref.keys()):
                ref[key] = ref[key].capitalize()
                ref[key.lower()] = ref.pop(key)

            ref['prato_principal'] = ref.pop('prato principal')
            ref['arroz_feijao'] = ref.pop('acompanhamento')
            ref['observacoes'] = ref.pop('obs')
            ref['pts'] = ref['pts'].replace("pts", "PTS") # TODO
            # TODO: consertar essa gambiarra depois.

        except AttributeError as e:
            print("Refeicoes nao sao dicionarios")




def cria_refeicoes(refeicoes_list):

    cardapios_por_data = {}

    for ref in refeicoes_list:
        try:
            d = ref['data']
        except KeyError as e:
            print("KeyError nas datas.")
            print(e, end="\n\n")
            break

        try:
            cardapios_por_data[d].append(Refeicao(**ref))
        except KeyError as e:
            # print("criando list para data: {}".format(d))
            # print(e)
            cardapios_por_data[d] = [Refeicao(**ref)]
        except TypeError as e:
            print("provavelmente argumento a mais no construtor de Refeicao")
            print(e)

    pprint.pprint(cardapios_por_data)
    return cardapios_por_data




def request_cardapio():
    # TODO: fazer request de verdade.
    raw_json = JSON_RESPONSE

    try:
        cardapios = json.loads(raw_json)
        refeicoes_list = cardapios['CARDAPIO']
    except KeyError as e:
        print('KeyError tentando pegar array de refeicoes.')
        refeicoes_list = []
    except:
        print("erro deserializando conteudo do JSON.")
        refeicoes_list = []


    return refeicoes_list







def cria_cardapios(cardapios_por_data):
    cardapios = []

    chaves_para_tipos = {
        'Almoço':'almoco',
        'Almoço vegetariano': 'almoco_vegetariano',
        'Jantar': 'jantar',
        'Jantar vegetariano': 'jantar_vegetariano'
    }

    for data in list(cardapios_por_data.keys()):
        refeicoes = {chaves_para_tipos[r.tipo] : r for r in cardapios_por_data[data]}
        cardapios.append(Cardapio(data=data, **refeicoes))


    return cardapios



def get_all_cardapios():
    refeicoes_list = request_cardapio()

    limpa_chaves(refeicoes_list)

    cardapios_por_data = cria_refeicoes(refeicoes_list)

    pprint.pprint(cardapios_por_data)

    cardapios = cria_cardapios(cardapios_por_data)

    pprint.pprint(cardapios)


def main():
    get_all_cardapios()


if __name__ == '__main__':
    main()
# def cardapio_para_datas(data_strings):


# @cache.memoize(timeout=60 * 5)  # cache com timeout de 5min
# def get_next_cardapios(date_string, next)