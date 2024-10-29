import json

from leitorPlanilhas import ler_planilha

lido = ler_planilha("../resources/data/raw/2014.csv")

data = []
saida = {
    'data': data,
}

id = 0
for l in lido:
    linha = {}
    linha['liquidado'] = l["Vl_Liquidado"]
    if l["Vl_Liquidado"].strip() == "-":
        linha['liquidado'] = "0,00"

    linha['orcado'] = l["Sld_Orcado_Ano"]
    if l["Sld_Orcado_Ano"].strip() == "-":
        linha['orcado'] = "0,00"

    linha['empenhado'] = l["Vl_Empenhado"]
    if l["Vl_Empenhado"].strip() == "-":
        linha['empenhado'] = "0,00"

    linha['atualizado'] = l["Vl_Atualizado"]
    if l["Vl_Atualizado"].strip() == "-":
        linha['atualizado'] = "0,00"

    if linha['atualizado'] == linha['orcado']:
        linha['atualizado'] = "0,00"

    linha['subfuncao'] = l["Ds_SubFuncao"]
    linha['programa'] = l["Ds_Programa"]
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

arq = open("../resources/data/json/2014.json","w")
json.dump(data, arq)
