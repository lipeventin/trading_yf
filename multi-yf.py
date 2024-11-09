import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts

import json
import numpy as np
import yfinance as yf
import pandas as pd
import pandas_ta as ta
#import talib
from lightweight_charts import Chart
#import plotly.graph_objs as go
from fel_indicadores import Indicador_fel




def dataToJSON(df, column, slice=0, color=None):
    data = df[['time', column, 'color']].copy()
    data = data.rename(columns={column: "value"})
    if(color == None):
        data.drop('color', axis=1)
    elif(color != 'default'):
        data['color'] = color
    if(slice > 0):
        data = data.iloc[slice:,:]
    return json.loads(data.to_json(orient = "records"))

def create_chart(df):
    candlestick_chart = go.Figure(data=[go.Candlestick(x=df.index,open=df)])
    chart = Chart()
    chart.set(df)

    return candlestick_chart


def calculate_sma2(df, period):
    teste= pd.DataFrame({'time': df['date'],f'SMA {period}': df.ta.sma(close="close", length=20, talib=True , offset =None)}).dropna()
    #df["SMA1"] = df.ta.sma(close="close", length=20, talib=True , offset =None)
    return (teste)


COLOR_BULL = 'rgba(38,166,154,0.9)' # #26a69a
COLOR_BEAR = 'rgba(239,83,80,0.9)'  # #ef5350
 

#Listar o Primeiro ativo a ser comparado
ticker_list = pd.read_csv('brasil.txt')
tickerSymbol = st.sidebar.selectbox('Stock ticker', ticker_list) # Select ticker symbol

# Request historic pricing data via finance.yahoo.com API
df = yf.Ticker(tickerSymbol).history(period='5y')[['Open', 'High', 'Low', 'Close', 'Volume']]
tickerData = yf.Ticker(tickerSymbol) # Get ticker data
tickerDf = tickerData.history(period='1d') #get the historical prices for this ticker
string_name = tickerData.info['longName']
st.header('**%s**' % string_name)

# Some data wrangling to match required format
df = df.reset_index()
df.columns = ['time','open','high','low','close','volume']                  # rename columns
df['time'] = df['time'].dt.strftime('%Y-%m-%d')                             # Date to string
df['color'] = np.where(  df['open'] > df['close'], COLOR_BEAR, COLOR_BULL)  # bull or bear
df.ta.macd(close='close', fast=6, slow=12, signal=5, append=True)           # calculate macd
#df["RSI"] = talib.RSI(df["close"], timeperiod=14)
df["rvi"]=df.ta.rvi(close="close",high="high",low="low", length=14)
print(df['time'],df["close"],df["rvi"])

 
 




# Listar o segundo ativo a ser comparado
ticker_compare = pd.read_csv('compare.lst')
tickercompare = st.sidebar.selectbox('Comparar', ticker_compare) # Select ticker symbol
if tickercompare != "Nenhum":
    df2=yf.Ticker(tickercompare).history(period='5y')[['Open', 'High', 'Low', 'Close', 'Volume']]
    df2 = df.reset_index()
    df2.columns = ['time','open','high','low','close','volume']                  # rename columns
    df2['time'] = df['time'].dt.strftime('%Y-%m-%d')   



clickSMA1 = st.sidebar.checkbox("SMA curta",  value=True)
if clickSMA1:
    curta = st.sidebar.number_input(label="Curta", value = 14 )
# SMA média
clickSMA2 = st.sidebar.checkbox("SMA Média",value=False)
if clickSMA2:
    media = st.sidebar.number_input(label="Média", value = 80 )

# SMA longa
clickSMA3 = st.sidebar.checkbox("SMA longa",value=False)
if clickSMA3:
    longa = st.sidebar.number_input(label="longa", value = 200 )

clickbandas = st.sidebar.checkbox("BandasBollinger",value=True)
if clickbandas:
    timebandas = st.sidebar.number_input(label="Tempo", value = 14 )
    bandapadrao = st.sidebar.number_input(label="padrao", value = 2.0 , step=0.5)
    
    
listaindicadores = pd.read_csv('indicators.lst')
indicator1 = st.sidebar.selectbox('Indicador', listaindicadores)
if indicator1 != "Nenhum":
    indicador1_dados, ind1_col, painel1, ind1_dic1, ind1_segundo, ind1_dic2 , ind1_time = Indicador_fel(indicator1, df )
 
 
    pass

listaindicadores2 = pd.read_csv('indicators.lst')
indicator2 = st.sidebar.selectbox('Indicador2', listaindicadores2)
if indicator2 != "Nenhum":
    pass


 
#tickerData = yf.Ticker(tickerSymbol) # Get ticker data


#selected_indicator = st.selectbox("Select a technical analysis indicator:", indicators)



#def atr(high, low, close, length=None, mamode=None, talib=None, drift=None, offset=None, **kwargs):

# Se bandas ativadas
if clickbandas:
    bandas = df.ta.bbands(close="close", length=timebandas , std=bandapadrao,  ddof=0, mamode=None, talib=True , offset =None)

    df["LowBB"] = bandas.iloc[:, :1]
    lowbb = dataToJSON(df,"LowBB", 0 , "black") #timebandas

    df["HighBB"] = bandas.iloc[:, 2]
    highbb = dataToJSON(df,"HighBB", 0 , "black")

if indicator1 != "Nenhum":
    if ind1_col == 1:
        pass
    elif ind1_col == 2:
        
        df["Ind1_L1"] =  indicador1_dados.iloc[:, 0]
        df["Ind1_L2"] =  indicador1_dados.iloc[:, 1]
        print("coluna 1 aberration: \n",df["Ind1_L1"]  )
        print("coluna 2 aberration: \n",df["Ind1_L2"]  )
        Ind1_L1 = dataToJSON(df,"Ind1_L1", 0, "purple") #ind1_time 
        Ind1_L2 = dataToJSON(df,"Ind1_L2", 0 , "purple") #ind1_time 
    pass


# curta
if clickSMA1:
    df["SMA1"] = df.ta.sma(close="close", length=curta, talib=True , offset =None)
    #sma1 = json.loads(df.rename(columns={"SMA1": "value"}).to_json(orient = "records"))
    sma1 = dataToJSON(df,"SMA1", 0, 'blue')

# SMA média
if clickSMA2:
    	df["SMA2"] = df.ta.sma(close="close", length=media, talib=True , offset =None).dropna()

    	sma2 = dataToJSON(df,"SMA2", 0, 'red')

# SMA longa
if clickSMA3:
    df["SMA3"] = df.ta.sma(close="close", length=longa, talib=True , offset =None, append=True).dropna()
    sma3 = dataToJSON(df,"SMA3", 0, 'gold')





# export to JSON format - Parece ser importante
candles = json.loads(df.filter(['time','open','high','low','close'], axis=1).to_json(orient = "records") )

if tickercompare != "Nenhum":
    lines2 = json.loads(df.filter(['time','open','high','low','close'], axis=1).to_json(orient = "records") )


#candles = json.loads(df.to_json(orient = "records"))
#volume = json.loads(df.rename(columns={"volume": "value",}).to_json(orient = "records"))
macd_fast = json.loads(df.rename(columns={"MACDh_6_12_5": "value"}).to_json(orient = "records"))
macd_slow = json.loads(df.rename(columns={"MACDs_6_12_5": "value"}).to_json(orient = "records"))
df['color'] = np.where(  df['MACD_6_12_5'] > 0, COLOR_BULL, COLOR_BEAR)  # MACD histogram color
macd_hist = json.loads(df.rename(columns={"MACD_6_12_5": "value"}).to_json(orient = "records"))

rvi_indicador = dataToJSON(df,"rvi",0, 'blue')  

chartMultipaneOptions = [
    {
        "width": 700,
        "height": 400,
        "layout": {
            "background": {
                "type": "solid",
                "color": 'white'
            },
            "textColor": "black"
        },
        "grid": {
            "vertLines": {
                "color": "rgba(197, 203, 206, 0.5)"
                },
            "horzLines": {
                "color": "rgba(197, 203, 206, 0.5)"
            }
        },
        "crosshair": {
            "mode": 1
        },
        "priceScale": {
            "borderColor": "rgba(197, 203, 206, 0.8)",
            "visible": True,
        },
        "timeScale": {
            "borderColor": "rgba(197, 203, 206, 0.8)",
            "barSpacing": 10
        },
        "watermark": {
            "visible": True,
            "fontSize": 34,
            "horzAlign": 'center',
            "vertAlign": 'center',
            "color": 'rgba(171, 71, 188, 0.3)',
            "text": tickerSymbol,
        }
    },

    {
        "width": 700,
        "height": 200,
        "layout": {
            "background": {
                "type": "solid",
                "color": 'white'
            },
            "textColor": "black"
        },
        "timeScale": {
            "visible": False,
        },
        "watermark": {
            "visible": True,
            "fontSize": 18,
            "horzAlign": 'left',
            "vertAlign": 'center',
            "color": 'rgba(171, 71, 188, 0.7)',
            "text": 'MACD',
        }
    },
    
       { "width": 700,
        "height": 200,
        "layout": {
            "background": {
                "type": "solid",
                "color": 'white'
            },
            "textColor": "black"
        },
        "timeScale": {
            "visible": True,
        },
        "watermark": {
            "visible": True,
            "fontSize": 18,
            "horzAlign": 'left',
            "vertAlign": 'up',
            "color": 'blue',
            "text": "  RVI",
        },
        "watermark2": {
            "visible": True,
            "fontSize": 18,
            "horzAlign": 'Center',
            "vertAlign": 'up',
            "color": 'gold',
            "text": "  Volatilidade",
        }
    }
]

seriesCandlestickChart = [
    {
        "type": 'Candlestick',
        "data": candles,
        "options": {
            "upColor": COLOR_BULL,
            "downColor": COLOR_BEAR,
            "borderVisible": True,
            "wickUpColor": COLOR_BULL,
            "wickDownColor": COLOR_BEAR
        }
    }

]

if clickSMA1:
     seriesCandlestickChart.append( { "type": 'Line',"data": sma1,"options": { "color": 'blue',"lineWidth": 1} })

if clickSMA2:
     seriesCandlestickChart.append( { "type": 'Line',"data": sma2,"options": { "color": 'blue',"lineWidth": 2} })

if clickSMA3:
    seriesCandlestickChart.append( { "type": 'Line',"data": sma3,"options": { "color": 'blue',"lineWidth": 3} })

if clickbandas:
    seriesCandlestickChart.append( { "type": 'Line',"data": lowbb,"options": { "color": 'black',"lineWidth": 1} })
    seriesCandlestickChart.append( { "type": 'Line',"data": highbb,"options": { "color": 'black',"lineWidth": 1} })

if tickercompare != "Nenhum":
    seriesCandlestickChart.append( { "type": 'Line',"data":  lines2,"options": { "color": 'purple',"lineWidth": 2} })

if indicator1  != "Nenhum":
    if ind1_col == 1:
        pass
    elif ind1_col == 2:
        if painel1 == 1:
            seriesCandlestickChart.append({"type": ind1_dic1[0] ,"data":Ind1_L1, "options": { "color": 'purple',"lineWidth": 1 } })
            seriesCandlestickChart.append({"type": ind1_dic2[0], "data":Ind1_L2, "options": { "color": 'purple',"lineWidth": 1 } })
       
    pass
    
    

#print ( "seriesCandlestickChart" , type(seriesCandlestickChart))
seriesMACDchart = [
    {
        "type": 'Line',
        "data": macd_fast,
        "options": {
            "color": 'blue',
            "lineWidth": 2
        }
    },
    {
        "type": 'Line',
        "data": macd_slow,
        "options": {
            "color": 'green',
            "lineWidth": 2
        }
    },
    {
        "type": 'Histogram',
        "data": macd_hist,
        "options": {
            "color": 'red',
            "lineWidth": 1
        }
    }
]

seriesvolatilitychart = [
    {
        "type": 'Line',
        "data": rvi_indicador ,
        "options": {
            "color": 'black',
            "lineWidth": 1
        }
    }
]


#st.subheader("Multipane Chart")

renderLightweightCharts([
    {
        "chart": chartMultipaneOptions[0],
        "series": seriesCandlestickChart
    },

    {
        "chart": chartMultipaneOptions[1],
        "series": seriesMACDchart
    },
    {
        "chart": chartMultipaneOptions[2],
        "series": seriesvolatilitychart
    }
], 'multipane')

#st.plotly_chart(create_chart(df))
