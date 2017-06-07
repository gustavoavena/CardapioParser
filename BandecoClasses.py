from enum import Enum

import json

def MyEnum(Enum):
    def __repr__(self):
        return json.dumps(self.__dict__)

Enum.__repr__ = MyEnum.__repr__

class TipoRefeicao(Enum):
    ALMOCO = "Almoço"
    ALMOCO_VEGETARIANO = "Almoço Vegetariano"
    JANTAR = "Jantar"
    JANTAR_VEGETARIANO = "Jantar Vegetariano"

    def to_json(self):
        return json.dumps(self.__dict__)

class ItemCardapio(Enum):
    ARROZ_FEIJAO = "arroz_feijao"
    PRATO_PRINCIPAL = "prato_principal"
    SALADA = "salada"
    SOBREMESA = "sobremesa"
    SUCO = "suco"
    OBSERVACOES = "observacoes"



""" Module that monkey-patches json module when it's imported so
JSONEncoder.default() automatically checks for a special "to_json()"
method and uses it to encode the object if found.
"""
from json import JSONEncoder

def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder().default  # Save unmodified default.
JSONEncoder.default = _default # replacement

class Refeicao(json.JSONEncoder):

    def __init__(self, tipo, arroz_feijao, prato_principal, guarnicao, pts, salada, sobremesa, suco, observacoes):
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
        out = "Tipo: " + self.tipo.value
        out += "{}\nsobremesa: {}\nsuco: {}\n".format(self.prato_principal, self.sobremesa, self.suco)
        return out

    def to_json(self):
        return json.dumps(self.__dict__)




class Cardapio:

    def __init__(self, data, almoco, jantar, almoco_vegetariano, jantar_vegetariano):
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

    def to_json(self):
        return json.dumps(self.__dict__)
