import json

from leitorPlanilhas import ler_planilha

lido = ler_planilha("../resources/data/raw/2013.csv")

data = []
saida = {
    'data': data,
}

id = 0
for l in lido:
    linha = {}
    linha['liquidado'] = l["Vl_Liquidado"]
    linha['empenhado'] = l["Vl_Empenhado"]
    linha['subfuncao'] = l["Ds_SubFuncao"]
    linha['programa'] = l["Ds_Programa"]
    linha['atualizado'] = l["Vl_Atualizado"]
    linha['orgao'] = l["Ds_Orgao"]
    linha['descricao'] = l["Ds_Projeto_Atividade"]
    linha['id'] = id
    #linha['orcado'] =
    linha['unidade'] = l["Ds_Unidade"]
    linha['funcao'] = l["Ds_Funcao"]
    #linha['entidades'] =
    #linha['tipo'] =
    id += 1
    data.append(linha)

arq = open("2013.json","w")
json.dump(data, arq)
