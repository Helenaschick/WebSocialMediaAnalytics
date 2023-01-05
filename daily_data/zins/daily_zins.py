# -*- coding: utf-8 -*-

# Umwandlung Jupyter Notebook "webscraping_comdirect" zu Python Skript
# Dieses Skript wird auf den AWS-Server gespeichert und über einen Cronjob täglich ausgeführt

import pandas as pd
import requests
import lxml
from lxml import html
from datetime import date

url = "https://www.comdirect.de/kredit/bauzinsen.html#Bauzinsen"

page = requests.get(url)
tree = html.fromstring(page.content)

eff5 = tree.xpath('//div[@class="table__container--scroll"]/table/tbody/tr[1]/td[4]/eff5/text()')
eff10 = tree.xpath('//div[@class="table__container--scroll"]/table/tbody/tr[2]/td[4]/eff10/text()')
eff15 = tree.xpath('//div[@class="table__container--scroll"]/table/tbody/tr[3]/td[4]/eff15/text()')
eff20 = tree.xpath('//div[@class="table__container--scroll"]/table/tbody/tr[4]/td[4]/eff20/text()')
eff25 = tree.xpath('//div[@class="table__container--scroll"]/table/tbody/tr[5]/td[4]/eff25/text()')

stand = tree.xpath('//div[@class="col__content outer-spacing--xlarge-bottom"]/p/date/text()')



matrix = [[0 for s in range(10)] for r in range(10)]

matrix[0][0]="Sollzinsbindung"
matrix[0][1]="5 Jahre"
matrix[0][2]="10 Jahre"
matrix[0][3]="15 Jahre"
matrix[0][4]="20 Jahre"
matrix[0][5]="25 Jahre"
matrix[1][0]="Effektiver Jahreszins"
matrix[1][1]=eff5
matrix[1][2]=eff10
matrix[1][3]=eff15
matrix[1][4]=eff20
matrix[1][5]=eff25
matrix[2][0]="Datenstand"
matrix[2][1]=stand
matrix[2][2]=stand
matrix[2][3]=stand
matrix[2][4]=stand
matrix[2][5]=stand


data = {
    'Sollzinsbindung': [],
    'Effektiver Jahreszins': [],
    'Datenstand': [],
}

for i in range(5):
    data['Sollzinsbindung'].append(matrix[0][i+1])
    data['Effektiver Jahreszins'].append(matrix[1][i+1])
    data['Datenstand'].append(matrix[2][i+1])

df=pd.DataFrame(data, columns=['Sollzinsbindung','Effektiver Jahreszins','Datenstand'])

df.to_csv(str(date.today()) +'_Zinsen.csv')