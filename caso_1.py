import csv

with open("reto.csv", 'r', encoding='utf-8') as file_csv:
    file = csv.DictReader(file_csv)
    for linea in file:
        print(linea)
