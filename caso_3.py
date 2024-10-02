import csv
import json

dataJSON = []

with open("reto.csv", 'r', encoding='utf-8') as file_csv:
    file = csv.DictReader(file_csv)
    for linea in file:
        dataJSON.append(linea)

sumatorio = 0
for dato in dataJSON:
    sumatorio += float(dato['Distance'])

print(sumatorio)
