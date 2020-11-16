#!/usr/bin/env python3

import numpy as np
import pandas as pd
import sys

def save_xls(dict_df, path):

    writer = pd.ExcelWriter(path)
    
    for key in dict_df:
        dict_df[key].to_excel(writer, key, index=False) 

    writer.save()
    
invoiceFile = 'invoices/invoices.csv'
invoices = pd.read_csv(invoiceFile)
invoices.columns = ['MONTH'] + (list(invoices.columns[1:]))

contract = sys.argv[1]
file = "raw_csv/" + contract.replace('/',":") + ".csv"
outFile =  contract.replace('/',":") + ".xls"
monthsMap = {1: 'STYCZEŃ', 2: 'LUTY', 3: 'MARZEC', 4: 'KWIECIEŃ',
                                      5: 'MAJ', 6: 'CZERWIEC', 7: 'LIPIEC', 8: 'SIERPIEŃ', 9: 'WRZESIEŃ',
                                      10: 'PAŹDZIERNIK', 11: 'LISTOPAD', 12: 'GRUDZIEŃ', 2020: '2020'}

data = pd.read_csv(file)
data.columns = data.columns.str.lstrip()
data.columns = data.columns.str.upper()
data = data.drop(['W'], axis=1)
data['PRICE'] = data['PRICE'].str.split().str.join('').str.replace('zł', '').astype(float)
data['TOTAL'] = data['TOTAL'].str.split().str.join('').str.replace('zł', '').astype(float)

allData = data.merge(invoices[invoices['CONTRACT'] == contract], left_on=['MONTH','PRODUCT'], right_on=['MONTH','PRODUCT'], how="left", suffixes=('', '_INVOICE'))

for prod in allData['PRODUCT'].unique():
    amountContract = allData[allData['PRODUCT']==prod]['AMOUNT'].sum()
    totalContract = allData[allData['PRODUCT']==prod]['TOTAL'].sum()
    amountInvoice = allData[allData['PRODUCT']==prod]['FINAL_AMOUNT'].sum()
    totalInvoice = allData[allData['PRODUCT']==prod]['FINAL_TOTAL'].sum()
    allData = allData.append({'MONTH': 2020, 'PRODUCT': prod, 'NAME': allData[allData['PRODUCT']==prod]['NAME'].unique()[0],
                'PRICE': allData[allData['PRODUCT']==prod]['PRICE'].unique()[0], 'AMOUNT': amountContract, 'TOTAL': totalContract, 'AMOUNT_INVOICE': amountInvoice, 'TOTAL_INVOICE': totalInvoice}, ignore_index=True)
    
toSave = allData[['MONTH', 'PRODUCT', 'NAME', 'PRICE', 'AMOUNT', 'TOTAL', 'AMOUNT_INVOICE', 'TOTAL_INVOICE']]

toSave = toSave.replace(np.nan, 0, regex=True)

data_dict = {}
data_dict['2020'] = toSave[toSave['MONTH']==2020]
for month in toSave['MONTH'].unique()[:-1]:
    data_dict[monthsMap[month]] = toSave[toSave['MONTH']==month]
save_xls(dict_df = data_dict, path = outFile)

