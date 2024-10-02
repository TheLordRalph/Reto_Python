import csv
import json
import math
import datetime

dataJSON = []

with open("reto.csv", 'r', encoding='utf-8') as file_csv:
    file = csv.DictReader(file_csv)
    for linea in file:
        dataJSON.append(linea)

distanciaMatricula = []

def buscarKeyInArray(array, key):
    for i, value in enumerate(array):
        if key in value:
            return i
    return None

def haversine(lat1, lon1, lat2, lon2):
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Diferencias
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    semiverseno = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    arcoseno = 2 * math.asin(math.sqrt(semiverseno))

    radioTierra = 6371
    distance = radioTierra * arcoseno
    return distance


for dato in dataJSON:
    posDateFormat = datetime.datetime.fromtimestamp(int(dato['Pos_date'])/1000.0).strftime('%d/%m/%Y %H:%M:%S')

    if len(distanciaMatricula) <= 0:
        distanciaMatricula.append({
            dato['Matricula']: float(dato['Distance']),
            'latitud': float(dato['Latitud']),
            'longitud': float(dato['Longitud']),
            'date': posDateFormat
        })
    else:
        indexMatricula = buscarKeyInArray(distanciaMatricula, dato['Matricula'])

        if indexMatricula != None:
            distancia = haversine(distanciaMatricula[indexMatricula]['latitud'], distanciaMatricula[indexMatricula]['longitud'], float(dato['Latitud']), float(dato['Longitud']))

            distanciaMatricula[indexMatricula][dato['Matricula']] += distancia
            distanciaMatricula[indexMatricula]['latitud'] = float(dato['Latitud'])
            distanciaMatricula[indexMatricula]['longitud'] = float(dato['Longitud'])

        else:
            distanciaMatricula.append({
                dato['Matricula']: float(dato['Distance']),
                'latitud': float(dato['Latitud']),
                'longitud': float(dato['Longitud']),
                'date': posDateFormat
            })

def selectMatriculaData(data):
    return data['date']

listaOrdenada = sorted(distanciaMatricula, key=(lambda x : x['date']), reverse=True)

with open("matriculas_ordenadas.txt", 'w') as newFile:
    for linea in listaOrdenada:
        newFile.write(str(linea) + '\n')
