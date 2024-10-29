#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

def ler_planilha(nome_arq):
    with open(nome_arq, 'r') as csvfile:
        arq = csv.reader(csvfile, delimiter=',', quotechar='|')
        titulos = []
        for c in arq.next():
            titulos.append(c.strip())
        elementos = []
        for l in arq:
            elem = {}
            i = 0
            for c in l:
                elem[titulos[i]] = c.decode('utf-8')
                i += 1
            elementos.append(elem)
        return elementos
