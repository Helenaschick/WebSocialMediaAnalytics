# -*- coding: utf-8 -*-

import lxml
from lxml import html
from lxml import etree
import numpy as np
import pandas as pd
import requests
import re
import csv
from csv import writer

from scipy import stats

import os
import sys

import time
import datetime
from datetime import date


Ort = ["berlin", "frankfurt-am-main", "hamburg", "koeln", "leipzig", "muenchen", "stuttgart"]
Umkreis = 50
Objekt = ["haeuser"]
Seite = list(range(250))

Website = "https://www.immowelt.de/liste/"
Slash = "/"
Snippet1 = "/kaufen?d=true&efs=NEW_BUILDING_PROJECT&efs=JUDICIAL_SALE&r="
Snippet2 = "&sd=DESC&sf=RELEVANCE&sp="


AnzahlElementebyID=0

nmax = [[0 for i in range(10000)] for j in range(10000)]
nmax[0][0]=0
for i in range(1,len(Seite),1):
    if nmax[i-1][0] <= len(Seite):
        nmax[i][0]=i*10        
    else:
        break
    q=i


a = [[0 for j in range(len(Ort)*len(Seite)+10)] for i in range(len(Ort)*len(Seite)+10)]
for i in range(len(Ort)):
    for j in range(len(Seite)):
        a[i][j]= Website + Ort[i] + Slash + Objekt[0] +Snippet1 + str(Umkreis) + Snippet2 + str(Seite[j]+1)
        page = requests.get(a[i][j])
        tree = html.fromstring(page.content)
        id = tree.xpath(".//a/@id")
        
        AnzahlElementebyID=AnzahlElementebyID+len(id)

b = [[0 for s in range(15)] for r in range(len(Ort)*AnzahlElementebyID)]
a = [[0 for j in range(len(Ort)*len(Seite)+10)] for i in range(len(Ort)*len(Seite)+10)]
laenge = 0
for i in range(len(Ort)):    
    for j in range(len(Seite)):
        
        for r in range(1,q,1):
            if j==nmax[r][0]:
                    time.sleep(3)
            else:
                break
                
        a[i][j]= Website + Ort[i] + Slash + Objekt[0] +Snippet1 + str(Umkreis) + Snippet2 + str(Seite[j]+1)
        page = requests.get(a[i][j])
        tree = html.fromstring(page.content)
        id = tree.xpath(".//a/@id")
        prices = tree.xpath('//div[@data-test="price"]/text()')
        MaxOrt = tree.xpath('//div[@class="estateFacts-f11b0"]/div[1]/span/text()')
        for e in range(len(MaxOrt)):
            MaxOrt[e]=MaxOrt[e][MaxOrt[e].index(""): MaxOrt[e].index("|")-1] 
        
        rooms = [[0 for s in range(1)] for r in range(len(id))]
        area= [[0 for s in range(1)] for r in range(len(id))]
        
        for e in range(len(id)):
            rooms[e][0]= tree.xpath('//a[@id="%s"]/div[2]/div[1]/div[1]/div[3]/text()'% id[e])
            area[e][0]= tree.xpath('//a[@id="%s"]/div[2]/div[1]/div[1]/div[2]/text()'% id[e])
              
        for r in range(len(id)):
             b[laenge+r][0]= id[r] 
             b[laenge+r][1]= MaxOrt[r]     
             b[laenge+r][2]= prices[r]      
             b[laenge+r][3]= Ort[i]
             b[laenge+r][4]=Umkreis
             b[laenge+r][5]= area[r][0]
             b[laenge+r][6]= rooms[r][0]
             
             
        laenge = laenge + len(id) 
        

haus_url= [[0 for j in range(100000)] for i in range(AnzahlElementebyID+100)]
website = "https://www.immowelt.de/expose/"

for i in range(AnzahlElementebyID):
    haus_url[0][i] = website + str(b[i][0])
    
for i in range(AnzahlElementebyID):    
    expose = requests.get(haus_url[0][i])
    ex_tree = html.fromstring(expose.content) 
    
    Grundstuecksflaeche= ex_tree.xpath(".//p[text()='Grundstücksfläche']")
    Kategorie= ex_tree.xpath(".//p[text()='Kategorie']")
    Etagen= ex_tree.xpath(".//p[text()='Geschosse']")
    Baujahr= ex_tree.xpath(".//p[text()='Baujahr']")
    Effizienzklasse= ex_tree.xpath(".//p[text()='Effizienzklasse']")
    Energietraeger= ex_tree.xpath(".//p[text()='Energieträger']")
    Heizungsart= ex_tree.xpath(".//p[text()='Heizungsart']")
    
     
    b[i][7]= ex_tree.xpath('//div[@class="flex ng-star-inserted"]/div[3]/span/text()') 
        
    
    if (len(Kategorie)) >= 1:  
        b[i][8] = ex_tree.xpath('//sd-cell-col[(@class="cell__col") and (.//p[text()="Kategorie"])]/p[2]/text()')
    else: 
        b[i][8]= "n.a" 
    
    if (len(Etagen)) >= 1:  
        b[i][9] = ex_tree.xpath('//sd-cell-col[(@class="cell__col") and (.//p[text()="Geschosse"])]/p[2]/text()')
    else:
        b[i][9]= "n.a" 

    if (len(Baujahr)) >= 1:  
        b[i][10]= ex_tree.xpath('//sd-cell-col[(@class="cell__col") and (.//p[text()="Baujahr"])]/p[2]/text()')
    else:
        b[i][10]= "n.a" 
   
    if (len(Effizienzklasse)) >= 1:  
        b[i][11] = ex_tree.xpath('//sd-cell-col[(@class="cell__col") and (.//p[text()="Effizienzklasse"])]/p[2]/text()')
    else: 
        b[i][11]= "n.a" 
   
    if (len(Energietraeger)) >= 1:  
        b[i][12] = ex_tree.xpath('//sd-cell-col[(@class="cell__col") and (.//p[text()="Energieträger"])]/p[2]/text()')
    else:
        b[i][12]= "n.a"
    
    if (len(Heizungsart)) >= 1:  
        b[i][13] = ex_tree.xpath('//sd-cell-col[(@class="cell__col") and (.//p[text()="Heizungsart"])]/p[2]/text()')
    else:
      b[i][13]= "n.a"    

data = {
    'ID': [],
    'Ort': [],
    'Umkreis': [],
    'MaxOrt': [],
    'Preis': [],
    'Fläche': [],
    'Zimmer': [],
    'Grundstuecksflaeche': [],
    'Kategorie': [],
    'Etagen': [],
    'Baujahr': [],
    'Effizienzklasse': [],
    'Energietraeger': [],
    'Heizungsart': [],
}

for q in range(AnzahlElementebyID):
    data['ID'].append(b[q][0])
    data['Ort'].append(b[q][3])
    data['Umkreis'].append(b[q][4])
    data['MaxOrt'].append(b[q][1])
    data['Preis'].append(b[q][2])
    data['Fläche'].append(b[q][5])
    data['Zimmer'].append(b[q][6])
    data['Grundstuecksflaeche'].append(b[q][7])
    data['Kategorie'].append(b[q][8])
    data['Etagen'].append(b[q][9])
    data['Baujahr'].append(b[q][10])
    data['Effizienzklasse'].append(b[q][11])
    data['Energietraeger'].append(b[q][12]) 
    data['Heizungsart'].append(b[q][13]) 
      
         
df=pd.DataFrame(data, columns=['ID','Ort','Umkreis','MaxOrt','Preis','Flaeche','Zimmer','Grundstuecksflaeche','Kategorie','Etagen','Baujahr','Effizienzklasse','Energietraeger','Heizungsart']) 
df.to_csv(str(datetime.date.today())+'_Immobilien.csv')
