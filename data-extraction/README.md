# Data Extraction

![data extraction diagram](https://github.com/pkieliba/bits-bobs/blob/master/data-extraction/extract-data.png?raw=true)

Many companies have valuable information in huge amounts of document images (e.g. pdf files) but the volume makes the manual extraction and organizing unfeasible.

Here I have created a system for automatically extracting information about the amount of contracted and realised medical services. This system was originally created for a hospital in Łęczyca, Poland. The hospital 
holds a large amount of contracts with National Health Fund (NFZ). The information related to the held contracts is stored in a secure online system, whereas the invoices related to the realisation of those contracts are stored in pdf files. The hospital wanted to extract the information from both of the sources and put it in Excel spredsheets, sperately for each contract type. This has been achieved using regular expressions and python library *[pdfplumber](https://github.com/jsvine/pdfplumber)*.





