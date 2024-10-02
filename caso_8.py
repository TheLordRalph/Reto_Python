import csv
import json
import math
import datetime
import ast
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Admin1234@172.17.0.2:3306/matriculas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Distancia(db.Model):
    id = db.Column(db.VARCHAR, primary_key=True)
    distancia = db.Column(db.FLOAT)
    latitud = db.Column(db.FLOAT)
    longitud = db.Column(db.FLOAT)
    fecha = db.Column(db.VARCHAR)

    def __json__(self):
        return {
            "id": self.id,
            "distancia": self.distancia,
            "latitud": self.latitud,
            "longitud": self.longitud,
            "fecha": self.fecha
            }

dataJSON = []

with open("reto.csv", 'r', encoding='utf-8') as file_csv:
    file = csv.DictReader(file_csv)
    for linea in file:
        dataJSON.append(linea)

distanciaMatricula = []

def buscarKeyInArray(array, key):
    for i, value in enumerate(array):
        if value['matricula'] == key:
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
            'matricula': dato['Matricula'],
            'distancia': float(dato['Distance']),
            'latitud': float(dato['Latitud']),
            'longitud': float(dato['Longitud']),
            'date': posDateFormat
        })
    else:
        indexMatricula = buscarKeyInArray(distanciaMatricula, dato['Matricula'])

        if indexMatricula != None:
            distancia = haversine(distanciaMatricula[indexMatricula]['latitud'], distanciaMatricula[indexMatricula]['longitud'], float(dato['Latitud']), float(dato['Longitud']))

            distanciaMatricula[indexMatricula]['distancia'] += distancia
            distanciaMatricula[indexMatricula]['latitud'] = float(dato['Latitud'])
            distanciaMatricula[indexMatricula]['longitud'] = float(dato['Longitud'])

        else:
            distanciaMatricula.append({
                'matricula': dato['Matricula'],
                'distancia': float(dato['Distance']),
                'latitud': float(dato['Latitud']),
                'longitud': float(dato['Longitud']),
                'date': posDateFormat
            })

def selectMatriculaData(data):
    return data['date']

listaOrdenada = sorted(distanciaMatricula, key=(lambda x : x['date']), reverse=True)

with open("matriculas_ordenadas.csv", 'w') as newFile:
    fieldnames = listaOrdenada[0].keys()
    writer = csv.DictWriter(newFile, fieldnames=fieldnames)
    writer.writeheader()
    for linea in listaOrdenada:
        writer.writerow(linea)


@app.route('/<matricula>', methods=['GET'])
def last_position(matricula):
    items = Distancia.query.all()

    for linea in items:
        if linea.id == matricula:
            return jsonify(linea.__json__())

    return jsonify('No se ha encontrado la matricula')


if __name__ == '__main__':
    app.run(debug=True)
