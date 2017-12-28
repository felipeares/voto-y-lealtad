# Importar librerías a utilizar
import numpy as np
import pandas as pd
from datetime import datetime
import json

# Cargar json con todas las sesiones
sesiones_raw = json.load(open('./data/sesiones.extended.1418.json'))
votaciones_raw = json.load(open('./data/votaciones.extended.1418.json'))
diputados_raw = json.load(open('./data/diputados.simple.1418.json'))

# Construir mapeo de id de diputados a número del 0-119
diputados_dict = {}
columnas_diputados = []
for i,diputado in enumerate(diputados_raw['data']):
    diputados_dict[diputado['prmid']] = i
    columnas_diputados.append(diputado['nombre'])

# Iniciar matriz con los datos de los boletines
boletines_mensajes = []
boletines_mensajes_num = []

# Funciones de ayuda
def crearVectorDeDiputados(arreglo, valor):
    # cargar el diccionario de manera global
    global diputados_dict
    # crear arreglo de 119 ceros
    vector_votacion = [0] * 120
    # cambiar "valor" en la posicion del diputado
    for diputado_prmid in arreglo:
        if diputado_prmid in diputados_dict:
            vector_votacion[diputados_dict[diputado_prmid]] = valor
    # return
    return vector_votacion


# Loop para cargar la matriz de los boletines-mensajes
for sesion in sesiones_raw['data']:
    for orden in sesion['ordenes']:
        if orden['origen'] == 'Cámara de Diputados / Mensaje':
            boletines_mensajes.append(
                    [sesion['sesion'],
                     orden['origen'],
                     sesion['fecha'], 
                     sesion['prmid'], 
                     orden['boletin'], 
                     orden['proyecto'], 
                     orden['pley_prmid']]
                    )
            boletines_mensajes_num.append(orden['boletin'])

# Crear el dataframe de los boletines de mensajes
boletines_mensajes_df = pd.DataFrame(boletines_mensajes, columns=['sesion', 
                                                                  'origen', 
                                                                  'fecha', 
                                                                  'prmid', 
                                                                  'boletin', 
                                                                  'proyecto', 
                                                                  'pley_prmid'])

# Iniciar matriz con las votaciones
votaciones_mensajes = []

# Loop para cargar las votaciones
for votacion in votaciones_raw['data']:
    if votacion['boletin'][3:] in boletines_mensajes_num:
        votos = [votacion['boletin'][3:], 
                 votacion['fecha'], 
                 votacion['materia'], 
                 votacion['articulo'], 
                 votacion['sesion'], 
                 votacion['tramite'],
                 votacion['quorum'],
                 votacion['resultado']]   
        
        vector_favor = crearVectorDeDiputados(votacion['favor'], 10)
        vector_contra = crearVectorDeDiputados(votacion['contra'], -10)
        vector_abstencion = crearVectorDeDiputados(votacion['abstencion'], -5)
        
        vector_final = [f + c + a for f, c, a in zip(vector_favor, vector_contra, vector_abstencion)]
        
        votaciones_mensajes.append(votos + vector_final)
        
# Crear el dataframe de las votaciones
votaciones_mensajes_df = pd.DataFrame(votaciones_mensajes, columns=(['boletin',
                                                                    'fecha',
                                                                    'materia',
                                                                    'articulo',
                                                                    'sesion',
                                                                    'tramite',
                                                                    'quorum',
                                                                    'resultado']+columnas_diputados))

# Guardar a CSV
votaciones_mensajes_df.to_csv('../data-analytics/data/votaciones.mensajes.csv', index = False)


