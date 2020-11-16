#!/bin/bash
#
# Extracts information from an .html file and saves it as a .csv file
#

clean_html(){
    sed -e '/ctl00_ContentPlaceHolder1_gvwPlan/,/table/!d' $inputFile > temp.txt 
    sed 's/<[^>]*>//g' temp.txt | awk '$1=$1' | sed '1,5d' > temp2.txt
    sed 's/Cena://g' temp2.txt | sed 's/Liczba://g' | sed 's/Kwota://g' | sed 's/Szczegóły//g' > temp.txt
    tr '\r\n' '*' < temp.txt | tr -s '*' > toCSV.txt
    rm temp.txt temp2.txt
}

create_csv(){
    echo 'Month, Product, Name, W, Amount, Price, Total' > $outFile.csv
    tr '*' '\n' < toCSV.txt | paste -s -d '******\n' - | sed 's/,/./g' | sed 's/*/,/g' >> $outFile.csv
    rm toCSV.txt
}

inputFile=$1
outFile="${inputFile%%.*}"

clean_html
create_csv

