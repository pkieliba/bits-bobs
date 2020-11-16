#!/usr/bin/env python3
import pdfplumber
import re
import pandas as pd
import glob
import numpy as np

invoices = pd.DataFrame(columns=['MONTH','CONTRACT','PRODUCT','AMOUNT','TOTAL'])
corrections = pd.DataFrame(columns=['MONTH','CONTRACT','PRODUCT','CORR_AMOUNT','CORR_TOTAL'])

dirs = np.sort(glob.glob("./invoices/*/"))

for dir in dirs:
    for file in glob.glob(dir + "*.pdf"):

        text = []
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text.append(page.extract_text())
        wholeText = ' '.join(text)
        wholeText = " ".join(wholeText.splitlines())

        data = re.search("[0-9]{2}\.([0-9]{2})\.[0-9]{4}", wholeText)

        if "korekcie" in wholeText:
            correction = True
            correctionText = re.search("Po korekcie.*?Razem", wholeText)
            cleanText = correctionText.group(0)
        else:
            correction = False
            cleanText = wholeText

        contract = re.search("053/130002/([0-9/N]*)", cleanText)
        points = re.findall("Za .*?zw", cleanText)

        for point in points:
            product = re.search("[0-9]{2}\.[0-9]{4}\.[0-9]{3}\.[0-9]{2}", point)
            amount = re.search("(PUNKT|RYCZA|KWOTA) ([0-9]* ?[0-9]+,[0-9]{4})", point)
            total = re.search(",[0-9]{2} (.*[0-9]+,[0-9]{2}) zw", point)
            if correction:
                temp = {"MONTH": data.group(1), "CONTRACT": contract.group(1), "PRODUCT": product.group(0), "CORR_AMOUNT": amount.group(2), "CORR_TOTAL": total.group(1)}
                corrections = corrections.append(temp, ignore_index=True)
            else:
                temp = {"MONTH": data.group(1), "CONTRACT": contract.group(1), "PRODUCT": product.group(0), "AMOUNT": amount.group(2), "TOTAL": total.group(1)}
                invoices = invoices.append(temp, ignore_index=True)


corrections = corrections.replace(',', '.', regex=True)
corrections = corrections.replace(' ', '', regex=True)
corrections['CORR_AMOUNT'] = corrections['CORR_AMOUNT'].astype('float')
corrections['CORR_TOTAL'] = corrections['CORR_TOTAL'].astype('float')
allCorrections = corrections.groupby(['MONTH','CONTRACT','PRODUCT']).sum().reset_index()

invoices = invoices.replace(',', '.', regex=True)
invoices = invoices.replace(' ', '', regex=True)
invoices['AMOUNT'] = invoices['AMOUNT'].astype('float')
invoices['TOTAL'] = invoices['TOTAL'].astype('float')
allInvoices = invoices.groupby(['MONTH','CONTRACT','PRODUCT']).sum().reset_index()
    
correctedInvoices = allInvoices.merge(allCorrections, left_on=['MONTH', 'CONTRACT', 'PRODUCT'], right_on=['MONTH', 'CONTRACT', 'PRODUCT'], how="left")
correctedInvoices = correctedInvoices.replace(np.nan, 0, regex=True)
correctedInvoices['FINAL_AMOUNT'] = correctedInvoices['AMOUNT'].astype(float) - correctedInvoices['CORR_AMOUNT']
correctedInvoices['FINAL_TOTAL'] = correctedInvoices['TOTAL'].astype(float) - correctedInvoices['CORR_TOTAL']

correctedInvoices.to_csv("invoices.csv", index=False)
