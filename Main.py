import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import yfinance as yf
%matplotlib inline
import plotly.graph_objs as go
import statsmodels.formula.api as smf
import plotly.offline as pyo
import plotly.graph_objs as go
plt.style.use('fivethirtyeight')

from datetime import date
pyo.init_notebook_mode()

SP500 = yf.download(tickers='^GSPC', start="1995-01-01", interval='1d')['Adj Close'].dropna()
VIX = yf.download(tickers='^VIX', start="1995-01-01", interval='1d')['Adj Close'].dropna()
SP500 = pd.DataFrame(SP500)
VIX = pd.DataFrame(VIX)

#First step
plt.figure(figsize=(20,14))
plt.title("Comportement du S&P 500 face aux conflits géopolitiques et crises financières", fontsize=20)
SP500['Adj Close'].plot(label='S&P 500', linewidth=2.0)
VIX['Adj Close'].plot(label='VIX',secondary_y=True, alpha = 0.25, linewidth=2.5)
plt.axvline(x='2022-02-19', color='purple', linestyle='--', label='Conflits géopolitiques', alpha =0.25)
plt.text(19000, -2,'Invasion Ukraine',rotation=0,fontsize=15, bbox=dict(facecolor='purple', alpha=0.25))
plt.axvline(x='2001-09-11', color='purple', linestyle='--', alpha =0.65)
plt.text(10000, -2,'Attentat : 11 Septembre 2001',rotation=0, fontsize=15, bbox=dict(facecolor='purple', alpha=0.25))
plt.axvline(x='2008-09-15', color='green', linestyle='--', label ='Crise financière / Krach boursier', alpha =0.65)
plt.text(13000, -2,'Crise des Subprimes',rotation=0, fontsize=15, bbox=dict(facecolor='green', alpha=0.25))
plt.axvline(x='2017-07-28', color='purple', linestyle='--', alpha =0.65)
plt.text(15300, -2,'Crise des missiles : Corée du Nord',fontsize=15, rotation=0, bbox=dict(facecolor='purple', alpha=0.25))
plt.axvline(x='2019-09-14', color='green', linestyle='--', alpha =0.65)
plt.text(17800, -2,'Crise Covid-19',rotation=0,fontsize=15 ,bbox=dict(facecolor='green', alpha=0.25))
plt.legend(prop={'size': 12}, bbox_to_anchor=(1,1))
plt.show() # show the plot
plt.clf() # clear the plot space

#Second step
df = SP500['Adj Close']
returns = df.pct_change()
last_price = df[-1] # on utilise ici le dernier prix
num_simulations = 100 # nombre de scénario
num_days = 180 # les jours simulés
simulation_df = pd.DataFrame()

np.random.seed(2) # modifier la seed pour générer des scénarios différents
for x in range(num_simulations):
 count = 0
 daily_vol = returns.std()

 price_series = []

 price = last_price * (1 + np.random.normal(0, daily_vol))
 price_series.append(price)

 for y in range(num_days):
 if count == 251:
 break
 price = price_series[count] * (1 + np.random.normal(0, daily_vol))
 price_series.append(price)
 count += 1

 simulation_df[x] = price_series

plt.figure(figsize=(20,14))
plt.title('Simulation de 100 scénarios : S&P 500')
plt.axhline(y = last_price, color = 'black', linestyle = 'dotted', label='Dernier prix')
plt.legend()
plt.plot(simulation_df, alpha=0.55)
plt.xlabel('Jours')
plt.show()

#Third step
simulation_df.columns = ['scénario ' + str(col) for col in simulation_df.columns] # on nomme chaque colonne
simulation_df # nos scénarios
simulation_df.describe() #show table

#only downgrade scenario
liste = []
for col_name in simulation_df.columns:
 liste.append(col_name)
 #print(col_name)

lowval = simulation_df[simulation_df <= AvgVal['50%']]

df = pd.DataFrame(lowval,columns=liste)
df = df.dropna(axis='columns')
print(df)

fig = px.line(df, x=df.index, y=df.columns,labels={
 "index": "Jours simulés",
"value": "Cours"
 },)
fig.update_layout(title_text='S&P 500 : scénario baissier', title_x=0.5)
fig.add_hline(y=last_price, line_dash="dot",
 annotation_text="Dernier prix")
fig.show()

#worth scenario
percent = pd.concat([df.head(1), df.tail(1)]) 
fall = (percent-percent.shift(1))/percent.shift(1)
minvalue = fall.min().min()
mincol = fall.min().idxmin()
pd.DataFrame({'Perte max (en %) ' : minvalue}, index = [mincol]) #show worth scenario (52)


#All scenario in one graph
df0 = SP500['Adj Close']
df1 = df0.reset_index()
df1 = df1.reset_index()
df2 = df
df1['new date'] = pd.to_datetime(df1['Date'])
df2['new date'] = pd.date_range(df1['Date'].max()+pd.Timedelta(1,unit='d'),periods=len(df2))
test = pd.DataFrame(df1['Date'].append(df2['new date']))
for column in df2:
 test[column] = df1['Adj Close'].append(df2[column])
test['Date'] = pd.DataFrame(df1['Date'].append(df2['new date']))
del test['new date']
del test[0]
test = test.set_index('Date')

plt.figure(figsize=(20,15))
plt.plot(test.index, test, alpha = 0.75, linewidth=1.5)
plt.xlim(18950,19250)
plt.ylim(3000,4800)
plt.show()
plt.clf() 

#detailed view
last_date = max(df1.Date) # on prend la dernière date du S&P 500 observée à ce jour
last_prediction = max(test.index) # on prend la dernière date de la prédiction du S&P 500
fig = go.Figure()
s = test.index
fig = px.line(test, x=s, y=test.columns,labels={
 "index": "Jours simulés",
"value": "Cours"
 },)
fig.update_layout(title_text='S&P 500 : les scénarios baissiers', title_x=0.5)
fig.add_hline(y=last_price, line_dash="dot",
 annotation_text="Dernier prix")
fig.add_vrect(x0=last_date, x1=last_prediction,
 annotation_text="Prévision", annotation_position="top right",
 fillcolor="green", opacity=0.15, line_width=0)
fig.show()
