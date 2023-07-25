import xmltodict
import pandas as pd
import os
import json
from openpyxl import Workbook


def getFile(cada_arquivo, valores):
    #print(cada_arquivo)
    with open(f'arquivos/{cada_arquivo}', "rb") as arquivo_xml:
        dict_arquivo = xmltodict.parse(arquivo_xml)
        #print(f'{json.dumps(dict_arquivo, indent=4)}')

        if 'NFe' in dict_arquivo:
            infos_nf = dict_arquivo['NFe']['infNFe']
        else:
            infos_nf = dict_arquivo['nfeProc']['NFe']['infNFe']
        numero_nota = infos_nf['@Id']
        empresa_emissora = infos_nf['emit']["xNome"]
        nome_cliente = infos_nf['dest']['xNome']
        endereco = infos_nf['dest']['enderDest']

        if 'vol' in infos_nf['transp']:
            peso = infos_nf['transp']['vol']['pesoB']
        else:
            peso = 'Volume não encotrado!'
        valores.append([numero_nota, empresa_emissora, nome_cliente, endereco, peso])


list_arquivos = os.listdir("arquivos")

colunas = ["numero_nota", "empresa_emissora", "nome_cliente", "endereco", "peso"]
valores = []
for arquivo in list_arquivos:
    getFile(arquivo, valores)
tabela = pd.DataFrame(columns=colunas, data=valores)
#print(tabela)
tabela.to_excel("NotasFiscais.xlsx", index=False)

