import re


def uppercase(matchobj):
    return matchobj.group(0).upper()

def capitalize(s):
    return re.sub('^([a-z])|'
                  '[\.|\?|\!]\s*([a-z])|'
                  '\s+([a-z])(?=\.)|'
                  '[\s,\.]+(ru|rs|ra)[\s,\.]+', uppercase, s)

def clean_spaces(s):
    s = re.sub('\s{2,}|\n', ' ', s)
    s = re.sub('\s\:\s*', ': ', s)
    return s


def limpa_especificos(ref):
    """
    Faz modificacoes especificas, como remover tags HTML e transformar siglas em maiusculo.
    :param ref: dicionario da refeicao a ser "limpada"
    """
    ref['observacoes'] = ref['observacoes'].replace('<font color = "red">', '')
    ref['observacoes'] = ref['observacoes'].replace('</font>', '')
    ref['observacoes'] = capitalize(capitalize(ref['observacoes'])) # chamar duas vezes pra resovler o problema do RA, que nao era alterado porque o RU dava match com a virgula primeiro.
    ref['observacoes'] = clean_spaces(ref['observacoes'])


    for key in ['pts', 'prato_principal']:
        ref[key] = ref[key].replace('pts', 'PTS').replace('Pts', 'PTS')  # vergonhoso, mas dps conserto



def limpa_chaves(refeicoes_list):
    """
    Faz a "limpeza" dos cardapios. Transforma letras em minusculas ou titulos, remove tags HTML, etc.
    Tambem altera o nome de algumas chaves para ficarem iguais aos atributos das classes definidas em BandecoClasses.
    :param refeicoes_list: lista com dicionarios contendo as informacoes das refeicoes.
    :return: lista atualizada apos a "limpeza"
    """
    for ref in refeicoes_list:
        try:
            for key in list(ref.keys()):
                ref[key] = ref[key].capitalize()
                ref[key.lower()] = ref.pop(key)

            # modificar chaves para ficarem de acordo com os atributos da classe que eu defini.
            ref['prato_principal'] = ref.pop('prato principal')
            ref['arroz_feijao'] = ref.pop('acompanhamento')
            ref['observacoes'] = ref.pop('obs')
            limpa_especificos(ref)

            # TODO: consertar essa gambiarra depois.

        except AttributeError as e:
            print("Refeicoes nao sao dicionarios")


# TODO: melhorar isso depois. Muito zona e ruim...
def limpa_nao_informado(cardapio):
    attributes = ['guarnicao', 'pts']
    NAO_INF = 'Não informado'
    DASH = '-'

    try:
        cardapio.almoco.guarnicao = cardapio.almoco.guarnicao.replace(NAO_INF, DASH)
        cardapio.jantar.guarnicao = cardapio.jantar.guarnicao.replace(NAO_INF, DASH)

        cardapio.almoco.pts = cardapio.almoco.pts.replace(NAO_INF, DASH)
        cardapio.jantar.pts = cardapio.jantar.pts.replace(NAO_INF, DASH)
    except AttributeError:
        print("AttributeError limpando nao informado.")
    except:
        print("Erro desconhecido limpando nao informado.")


    for at in attributes:
        try:

            value = getattr(cardapio.almoco_vegetariano, at)
            value = value.replace('Não informado', getattr(cardapio.almoco, at))
            value = value.replace(' ', getattr(cardapio.almoco, at))
            setattr(cardapio.almoco_vegetariano, at, value)

            value = getattr(cardapio.jantar_vegetariano, at)
            value = value.replace('Não informado', getattr(cardapio.jantar, at))
            value = value.replace(' ', getattr(cardapio.jantar, at))
            setattr(cardapio.jantar_vegetariano, at, value)
        except AttributeError as e:
            print("Attribute error!")
        except:
            print("Erro desconhecido limpando nao informados.")

    return cardapio

