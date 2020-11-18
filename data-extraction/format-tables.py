#!/usr/bin/env python3

import numpy as np
import pandas as pd
import sys

def save_xls(dict_df, path):

    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    workbook = writer.book

    head_format = workbook.add_format({'bold': True, 'border': 1, 'font_name': 'Calibri', 'font_size': 14, 'align': 'center', 'valign': 'vcenter'})
    cell_format = workbook.add_format({'font_name': 'Calibri', 'font_size': 12, 'valign': 'vcenter', 'num_format': '#,##0.00'})
    month_format = workbook.add_format({'font_name': 'Calibri', 'font_size': 12, 'align': 'center', 'valign': 'vcenter'})
    sum_format = workbook.add_format({'bold': True, 'font_name': 'Calibri', 'font_size': 14, 'align': 'center', 'valign': 'vcenter', 'num_format': '#,##0.00'})

    for key in dict_df:
        if key==str(year):
            dict_df[key].to_excel(writer, key, index=False, header=False, startrow=1)
            worksheet = writer.sheets[key]
            for row_num in range(2, len(dict_df[key])+2):
                worksheet.write_formula('E' + str(row_num), '=SUM(STYCZEŃ:GRUDZIEŃ!E' + str(row_num+1) + ')')
                worksheet.write_formula('F' + str(row_num), '=SUM(STYCZEŃ:GRUDZIEŃ!F' + str(row_num+1) + ')')
                worksheet.write_formula('G' + str(row_num), '=SUM(STYCZEŃ:GRUDZIEŃ!G' + str(row_num+1) + ')')
                worksheet.write_formula('H' + str(row_num), '=SUM(STYCZEŃ:GRUDZIEŃ!H' + str(row_num+1) + ')')
            for col_num, value in enumerate(['YEAR'] +list(toSave.columns[1:])):
                worksheet.write(0, col_num, value, head_format)
            worksheet.set_column('A:A', 12, month_format)
            worksheet.set_column('B:H', 18, cell_format)
            worksheet.write('A' + str(len(dict_df[key])+4), 'GRAND TOTAL', sum_format)
            worksheet.write_formula('F' + str(len(dict_df[key])+4), '=SUM(F2:F' + str(row_num+1) + ')', sum_format)
            worksheet.write_formula('H' + str(len(dict_df[key])+4), '=SUM(H2:H' + str(row_num+1) + ')', sum_format)
        else:
            dict_df[key].to_excel(writer, key, index=False, header=False, startrow=2)
            worksheet = writer.sheets[key]
            for row_num in range(2, len(dict_df[key])+3):
                worksheet.write_formula('I' + str(row_num), '=SUM(STYCZEŃ:' + key + '!E' + str(row_num) + ')')
                worksheet.write_formula('J' + str(row_num), '=SUM(STYCZEŃ:' + key + '!F' + str(row_num) + ')')
                worksheet.write_formula('K' + str(row_num), '=SUM(STYCZEŃ:' + key + '!G' + str(row_num) + ')')
                worksheet.write_formula('L' + str(row_num), '=SUM(STYCZEŃ:' + key +'!H' + str(row_num) + ')')
            for col_num, value in enumerate(list(toSave.columns) + ['AMOUNT', 'TOTAL', 'AMOUNT_INVOICE', 'TOTAL_INVOICE']):
                worksheet.write(1, col_num, value, head_format)
            worksheet.merge_range('I1:L1', 'RUNNING', head_format)
            worksheet.set_column('A:A', 12, month_format)
            worksheet.set_column('B:L', 18, cell_format)
            worksheet.write('A' + str(len(dict_df[key])+4), 'GRAND TOTAL', sum_format)
            worksheet.write_formula('F' + str(len(dict_df[key])+4), '=SUM(F3:F' + str(row_num+1) + ')', sum_format)
            worksheet.write_formula('H' + str(len(dict_df[key])+4), '=SUM(H3:H' + str(row_num+1) + ')', sum_format)
            worksheet.write_formula('J' + str(len(dict_df[key])+4), '=SUM(J3:J' + str(row_num+1) + ')', sum_format)
            worksheet.write_formula('L' + str(len(dict_df[key])+4), '=SUM(L3:L' + str(row_num+1) + ')', sum_format)
            
    writer.save()

    
invoiceFile = 'invoices/invoices.csv'
invoices = pd.read_csv(invoiceFile)
invoices.columns = ['MONTH'] + (list(invoices.columns[1:]))

contract = sys.argv[1]
year = sys.argv[2]
file = "raw_csv/" + contract.replace('/',":") + ".csv"
outFile =  contract.replace('/',":") + ".xlsx"
monthsMap = {1: 'STYCZEŃ', 2: 'LUTY', 3: 'MARZEC', 4: 'KWIECIEŃ',
                                      5: 'MAJ', 6: 'CZERWIEC', 7: 'LIPIEC', 8: 'SIERPIEŃ', 9: 'WRZESIEŃ',
                                      10: 'PAŹDZIERNIK', 11: 'LISTOPAD', 12: 'GRUDZIEŃ', year: str(year)}

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
    allData = allData.append({'MONTH': year, 'PRODUCT': prod, 'NAME': allData[allData['PRODUCT']==prod]['NAME'].unique()[0],
                'PRICE': allData[allData['PRODUCT']==prod]['PRICE'].unique()[0], 'AMOUNT': amountContract, 'TOTAL': totalContract, 'AMOUNT_INVOICE': amountInvoice, 'TOTAL_INVOICE': totalInvoice}, ignore_index=True)
    
toSave = allData[['MONTH', 'PRODUCT', 'NAME', 'PRICE', 'AMOUNT', 'TOTAL', 'AMOUNT_INVOICE', 'TOTAL_INVOICE']]

toSave = toSave.replace(np.nan, 0, regex=True)

data_dict = {}
data_dict[str(year)] = toSave[toSave['MONTH']==year]
for month in toSave['MONTH'].unique()[:-1]:
    data_dict[monthsMap[month]] = toSave[toSave['MONTH']==month]
save_xls(dict_df = data_dict, path = outFile)

