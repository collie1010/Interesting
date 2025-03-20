# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 15:53:14 2024

@author: HW-T06
"""

import pandas as pd
import requests
import json
import argparse

def fetch_stock_data(date, stock_no):
    url = f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={date}&stockNo={stock_no}'
    html = requests.get(url)
    content = json.loads(html.text)
    stock_data = content['data']
    col_name = content['fields']


    df = pd.DataFrame(data=stock_data, columns=col_name)
    return df

def main():

    parser = argparse.ArgumentParser(description='Fetch stock data from TWSE')
    parser.add_argument('date', type=str, help='Date in YYYYMMDD format')
    parser.add_argument('stock_no', type=str, help='Stock number')

    args = parser.parse_args()
    
    df = fetch_stock_data(args.date, args.stock_no)
    print(df)

if __name__ == "__main__":
    main()
