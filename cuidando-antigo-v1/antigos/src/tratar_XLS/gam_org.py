import json
from collections import OrderedDict


def converter_para_float(texto):
    texto = texto.replace(".","")
    texto = texto.replace(",",".")
    return float(texto)

def linha_csv(entidade, valores):
    linha = ""
    linha += entidade["orgao"]+";"
    linha += entidade["unidade"]+";"
    linha += entidade["funcao"]+";"
    linha += entidade["subfuncao"]+";"
    linha += entidade["descricao"]+";"
    linha += str(valores[0])+";"
    linha += str(valores[1])+";"
    linha += str(valores[2])+";"
    linha += str(valores[3])+";"
    linha += valores[4]
    return linha


arq = open("../../resources/data/json/2014-geocoded.json")
dados = json.load(arq)["data"]
arq.close()

orgaos = {}

# Monta dicionario separando Projetos de cada Orgao
for entidade in dados:
    projetos = orgaos.get(entidade["orgao"])
    if not projetos:
        projetos = {}
        orgaos[entidade["orgao"]] = projetos

    entidades = projetos.get(entidade["descricao"])
    if not entidades:
        entidades = []
        projetos[entidade["descricao"]] = entidades

    entidades.append(entidade)

#print orgaos.values()[0].values()[0]

saida = {}

for nome_projeto, projetos in orgaos.items():
    saida[nome_projeto] = []
    for projeto in projetos.values(): 
        orcado = 0.0
        atualizado = 0.0
        empenhado = 0.0
        liquidado = 0.0
        for entidade in projeto:
            orcado += converter_para_float(entidade["orcado"])
            atualizado += converter_para_float(entidade["atualizado"])
            empenhado += converter_para_float(entidade["empenhado"])
            liquidado += converter_para_float(entidade["liquidado"])
        if entidade["coordenadas"]:
            mapeado = "sim"
        else:
            mapeado = "nao"

        valores = (orcado, atualizado, empenhado, liquidado, mapeado)
        saida[nome_projeto].append(linha_csv(entidade, valores))
        saida[nome_projeto].sort()

saida = OrderedDict(sorted(saida.items(), key=lambda t: t[0]))
arq = open("orgaos.json","w")
json.dump(saida, arq, indent=1, separators=(',', ': '))
