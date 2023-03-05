# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 14:04:48 2023

@author: cbure
"""

import requests

chainName = 'eth-mainnet'

walletAddress = '0x4CAECFc01ad2907d37F51d23e0691244f4B57692'

url = f"https://api.covalenthq.com/v1/{chainName}/address/{walletAddress}/portfolio_v2/"
        
headers = {
    "content-type": "application/json",
}

auth = ('ckey_5e3ae0ddd55745329fa31c57fd3', '')
    
response = requests.get(url, headers=headers, auth=auth)

#%%

resp_json = response.json()

#%%
import pandas as pd

num_coins_df = pd.DataFrame()
price_df = pd.DataFrame()

for coin_dict in resp_json['data']['items']:
    intermediate_num_coins_df = pd.DataFrame()
    intermediate_price_df = pd.DataFrame()
    coin = coin_dict['contract_ticker_symbol']
    for day_dict in coin_dict['holdings']:
        index = day_dict['timestamp']
        try:
            price = float(day_dict['quote_rate'])
            num_coins = float(day_dict['close']['balance']) / 10**18
        except TypeError:
            price = 0
            num_coins = 0
        
        temp_num_coins_df = pd.DataFrame(data = {coin: num_coins}, index = [index])
        intermediate_num_coins_df = pd.concat([intermediate_num_coins_df, temp_num_coins_df])
        
        temp_price_df = pd.DataFrame(data = {coin: price}, index = [index])
        intermediate_price_df = pd.concat([intermediate_price_df, temp_price_df])
        
        
        
    num_coins_df[coin] = intermediate_num_coins_df
    price_df[coin] = intermediate_price_df
    #%%


for df_name in [num_coins_df, price_df]:
    for col_name in df_name.columns:  
        if (df_name[col_name] == 0).all():
            print(f'{col_name} is all 0s')
            del df_name[col_name]

#%%

### change in balance

bal_df = num_coins_df.iloc[::-1].copy()

for column in bal_df.columns:
    start_val = bal_df[column][0]
    for row in bal_df.index:
        bal_df.loc[row,column] = bal_df.loc[row,column] / start_val

#%%

### change in price

delta_price_df = price_df.iloc[::-1].copy()

delta_price_df = delta_price_df.diff()

delta_price_df = delta_price_df.iloc[1:, :]
bal_df = bal_df.iloc[1:, :]


#%%

pnl_df = bal_df.copy()

for column in pnl_df.columns:
    for row in pnl_df.index:
        pnl_df.loc[row, column] = pnl_df.loc[row, column] * delta_price_df.loc[row, column]
        
#%%

coin_fin_pnl_dict = {}

for coin in pnl_df.columns:
    coin_fin_pnl_dict[coin] = sum(pnl_df[coin])

#%%

pnl_df['total_pnl'] = [0]*len(pnl_df)

for row in pnl_df.index:
    temp_fin_pnl = 0
    for column in pnl_df.columns:
        temp_fin_pnl = temp_fin_pnl + pnl_df.loc[row, column]
        
    pnl_df.loc[row, 'total_pnl'] = temp_fin_pnl

#%%

cumulative_df = price_df.iloc[::-1].copy()

cumulative_df['cumul_pnl'] = [0]*len(cumulative_df)

for i in range(1, len(cumulative_df)):
    temp_index_now = cumulative_df.index[i]
    temp_index_old = cumulative_df.index[i-1]
    cumulative_df.loc[temp_index_now, 'cumul_pnl'] = cumulative_df.loc[temp_index_old, 'cumul_pnl'] + pnl_df.loc[temp_index_now, 'total_pnl']

cumulative_df = cumulative_df[['cumul_pnl']]

#%%   
        
import plotly.express as px

fig = px.line(cumulative_df['cumul_pnl'], y="cumul_pnl", title='Cumulative Performance')
fig.show()

#%%


        
        
        
        
        