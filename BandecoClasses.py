from enum import Enum

import json

class TipoRefeicao(Enum):
    ALMOCO = "Almoço"
    ALMOCO_VEGETARIANO = "Almoço Vegetariano"
    JANTAR = "Jantar"
    JANTAR_VEGETARIANO = "Jantar Vegetariano"

    def to_json(self):
        return json.dumps(self.__dict__)



class MyJsonEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class Refeicao:

    def __init__(self, tipo, arroz_feijao, prato_principal, guarnicao, pts, salada, sobremesa, suco, observacoes, **kwargs):
        self.tipo = tipo # TODO: garatir que eh do tipo Refeicao
        self.arroz_feijao = arroz_feijao
        self.prato_principal = prato_principal
        self.guarnicao= guarnicao
        self.pts = pts
        self.salada = salada
        self.sobremesa = sobremesa
        self.suco = suco
        self.observacoes = observacoes

    @staticmethod
    def fromDict(tipo, refeicoes):
        try:
            return Refeicao(tipo=tipo, **refeicoes)
        except:
            print("problema com convienience init de Refeicao.")

    def __str__(self):
        out = "Tipo: " + self.tipo
        out += "{}\nsobremesa: {}\nsuco: {}\n".format(self.prato_principal, self.sobremesa, self.suco)
        return out

    @staticmethod
    def to_json(self):
        return json.dumps(self.__dict__)



'''
{'ACOMPANHAMENTO': 'ARROZ E FEIJÃO',
               'DATA': '2017-06-12',
               'GUARNICAO': 'BATATA FRITA LISA',
               'OBS': 'O CARDÁPIO CONTÉM GLÚTEN NO PÃO E NO STROGONOFF DE '
                      'CARNE E CONTÉM LACTOSE NO STROGONOFF DE CARNE. NÃO '
                      'CONTÉM OVOS.\r\n'
                      '<font color = "red"> NÃO ESQUEÇA SUA CANECA ! </font>',
               'PRATO PRINCIPAL': 'STROGONOFF DE CARNE',
               'PTS': 'PTS COM MANDIOQUINHA',
               'SALADA': 'ALFACE',
               'SOBREMESA': 'MAÇÃ',
               'SUCO': 'CAJÚ',
               'TIPO': 'Almoço'}
'''

class Cardapio:

    def __init__(self, data, almoco, jantar, almoco_vegetariano, jantar_vegetariano, **kwargs):
        self.data = data

        # garante que as refeicoes sao do tipo certo.
        if not isinstance(almoco, Refeicao) or not isinstance(jantar, Refeicao) or not isinstance(almoco_vegetariano, Refeicao) or not isinstance(jantar_vegetariano, Refeicao):
            raise TypeError("Atributos de Cardapio devem ser do tipo Refeicao.")

        self.almoco = almoco
        self.jantar = jantar
        self.almoco_vegetariano = almoco_vegetariano
        self.jantar_vegetariano = jantar_vegetariano


    @staticmethod
    def fromRefeicoesDict(data, refeicoes):
        try:
            return Cardapio(data=data, almoco=refeicoes[TipoRefeicao.ALMOCO], jantar=refeicoes[TipoRefeicao.JANTAR], almoco_vegetariano=refeicoes[TipoRefeicao.ALMOCO_VEGETARIANO], jantar_vegetariano=refeicoes[TipoRefeicao.JANTAR_VEGETARIANO])
        except KeyError as e:
            print("Problema com key no convenience init de Cardapio.")



    def __str__(self):
        return "Cardapio\nData: {}\nAlmoco: \n  {}\nJantar: \n  {}\n".format(self.data, self.almoco, self.jantar)

    @staticmethod
    def to_json(self):
        return json.dumps(self.__dict__)
