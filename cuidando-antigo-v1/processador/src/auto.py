# coding: utf-8

import os
import sys
import urllib.request
import shutil
import json

import xlrd


def baixar_dados_da_prefeitura(nome_arq):
    """Baixa os dados da prefeitura e salva em arquivo"""
    link = "http://sempla.prefeitura.sp.gov.br/orcamento/uploads/%s/basedadosexecucao%s.xls" % ((ano,)*2)
    with urllib.request.urlopen(link) as response, open(nome_arq, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)


def processar_xls(nome_arq):
    """Lê um arquivo XLS montando uma lista de dicionários com o conteúdo"""
    wb = xlrd.open_workbook(nome_arq)
    sh = wb.sheets()[0]
    titulos = []
    for c in sh.row_values(0):
        titulos.append(c.strip().lower())
    elementos = []
    for n in range(1,sh.nrows):
        l = sh.row_values(n)
        elem = {}
        i = 0
        for c in l:
            elem[titulos[i]] = c
            i += 1
        elementos.append(elem)
    return elementos


def formatar_num(num):
    """Converte um número para str com 2 casas decimais e usando , como
    separador decimal"""
    return "{:.2f}".format(num).replace('.', ',')


def exportar_json(lido, nome_arq):
    """Prepara a salva arquivo JSON para ser geolocalizado"""
    data = []
    id = 0
    for l in lido:
        linha = {}

        linha['liquidado'] = formatar_num(l["vl_liquidado"])
        linha['orcado'] = formatar_num(l["sld_orcado_ano"])
        linha['empenhado'] = formatar_num(l["vl_empenhado"])
        linha['atualizado'] = formatar_num(l["vl_atualizado"])

        if linha['atualizado'] == linha['orcado']:
            linha['atualizado'] = "0,00"

        linha['subfuncao'] = l["ds_subfuncao"]
        linha['programa'] = l["ds_programa"]
        linha['orgao'] = l["ds_orgao"]
        linha['descricao'] = l["ds_projeto_atividade"]
        linha['descricao_desp'] = l["cd_despesa"]
        linha['id'] = id
        linha['unidade'] = l["ds_unidade"]
        linha['funcao'] = l["ds_funcao"]
        id += 1
        data.append(linha)

    arq = open(nome_arq, "w")
    json.dump(data, arq)


if __name__ == "__main__":
    ano = sys.argv[1]
    pasta_dados = "../../site/data/" + ano
    nome_arq_xls = "xlss/%s.xls" % ano
    nome_arq_json_nao_localizado = "jsons/%s.json" % ano
    nome_arq_json_localizado = "jsons/%s-geocoded.json" % ano

    print("ANO: %s" % ano)

    print("Baixando")
    baixar_dados_da_prefeitura(nome_arq_xls)

    print("Pré-Processando")
    dados = processar_xls(nome_arq_xls)
    exportar_json(dados, nome_arq_json_nao_localizado)

    print("Geolocalizando via PERL:")
    os.system("perl main2.pl -y %s" % ano)
    os.system("cp %s %s/geocoded.json" % (nome_arq_json_localizado, pasta_dados))

    print("Gerando Arquivo com Orgãos")
    os.system("perl json2csv.pl %s/geocoded.json > %s/orgaos.json" % ((pasta_dados,)*2))

    print("Feito")
