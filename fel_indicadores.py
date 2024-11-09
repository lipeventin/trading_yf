#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 22:13:57 2024

@author: felipe
"""

import streamlit as st
import pandas as pd

print(" Felipes Indicadores")

def Indicador_fel( nome, df):
    print(" imprimindo  base de calculo como chamada na função \n", df)
    if nome == "Aberration: aberration":
        #aberration(high, low, close, length=None, atr_length=None, offset=None, **kwargs)
        aberration_comp = st.sidebar.number_input(label="Tempo(aberration)", value = 14 )
        aberrationdata= df.ta.aberration(close="close", 
            high="high",low="low", lenght =5, atr_length=aberration_comp)
        print("La vem aberration")
        print(aberrationdata)
        print("feito")
        aberrationdata = aberrationdata.reset_index()
        aberrationdata.columns = ["Index",'AbMean','AbHigh','AbLow','AbATR']  
        aberrationdata = aberrationdata.drop(columns=["Index",'AbMean', 'AbATR'])
        print(aberrationdata)
        data = aberrationdata
        colunas = 1
        painel = 3
        dicionario1 =["Line"]
        #dicionario1 = { "type": 'Line',"data": aberrationdata['AbLow'] ,"options": { "color": 'purple',"lineWidth": 1} }
        temsegundo = True
        dicionario2 =  ["Line"]
        ind_time = aberration_comp
        
        print(data, painel, dicionario1, temsegundo, dicionario2, ind_time)
       
        print("painel é  = ", painel)
        
    elif nome == "Average True Range: atr":
        atr_time = st.sidebar.number_input(label="Tempo(ATR)", value = 14 )
        atr_data= df.ta.atr(close="close", 
            high="high",low="low", lenght =atr_time)
        print("La vem ATR")
        print(atr_data)
        print("feito")
        atr_data = atr_data.reset_index()
        atr_data.columns = ["Index", "ATR"]  
        atr_data = atr_data.drop(columns=["Index"])
        print("\n  ----------\n Dados de ATR finalizados: \n ", atr_data)
        data = atr_data
        colunas = 1
        painel = 3
        dicionario1 =["Line"]
        #dicionario1 = { "type": 'Line',"data": aberrationdata['AbLow'] ,"options": { "color": 'purple',"lineWidth": 1} }
        temsegundo = False
        dicionario2 =  ["Line"]
        ind_time = atr_time
    pass
     
    return data,colunas, painel, dicionario1, temsegundo, dicionario2, ind_time
   

"""
if linguagem == "C++":
print('C++ é uma linguagem de programação compilada.')
elif linguagem == "Python":
print("Python é uma linguagem de programação de alto nível")
elif linguagem == "Java":
print("Java é uma linguagem de programação amplamante utilizada no mercado")
else:
print('Não é nenhuma das duas opções')
"""