# Importar librerías a utilizar
import numpy as np
import pandas as pd
import json

# Cargar info de diputados
diputados_raw = json.load(open('../data-scraping/data/diputados.extended.1418.json'))

# Cargar Matriz CSV
matrix_votos = pd.read_csv('./data/votaciones.mensajes.texto.csv')
num_votaciones = matrix_votos['boletin'].count()

# Obtener número de votaciones en donde todos aprobaron
todos_deacuerdo = 0
matrix_votos_np = matrix_votos.iloc[:, 8:].values
for x in matrix_votos_np:
    unique, counts = np.unique(x, return_counts=True)
    votos = dict(zip(unique, counts))
    for i in range(0,6):
        votos[i] = votos[i] if i in votos else 0
    if votos[2] + votos[3] == 0:
        todos_deacuerdo = todos_deacuerdo + 1

# Iniciar variable que guardará a los diputados y sus indicadores
diputados_info = []
diputados_info_matrix = []

# Función de cálculo de lealtad 
def calcularLealtad(rep, con_asistencia = False):
    global num_votaciones
    if con_asistencia:
        return round((rep['favor']/ (num_votaciones - rep['ausencia'])), 2)
    else:
        return round((rep['favor']/ (num_votaciones)), 2)

for diputado in diputados_raw['data']:
    rep = {
        'prmid': diputado['prmid'],
        'nombre': diputado['nombre'],
        'comite_parlamentario': diputado['comite_parlamentario'],
        'favor': int(matrix_votos[diputado['nombre']][matrix_votos[diputado['nombre']] == 1].count()),
        'contra': int(matrix_votos[diputado['nombre']][matrix_votos[diputado['nombre']] == 2].count()),
        'abstencion': int(matrix_votos[diputado['nombre']][matrix_votos[diputado['nombre']] == 3].count()),
        'pareo': int(matrix_votos[diputado['nombre']][matrix_votos[diputado['nombre']] == 4].count()),
        'articulo_quinto': int(matrix_votos[diputado['nombre']][matrix_votos[diputado['nombre']] == 5].count()),
        'ausencia': 0,
        'lealtad': 0,
        'lealtad_con_asistencia': 0
    }
    
    rep['ausencia'] = int(num_votaciones - rep['favor'] - rep['contra'] - rep['abstencion'] - rep['pareo'] - rep['articulo_quinto'])
    
    rep['lealtad'] = calcularLealtad(rep)
    rep['lealtad_con_asistencia'] = calcularLealtad(rep, con_asistencia = True)
    
    diputados_info.append(rep)
    
    matrix_columnas = [k for k, v in rep.items()]
    diputados_info_matrix.append([v for k, v in rep.items()])

# Crear dataframe con la matriz resumen
diputados_info_df = pd.DataFrame(diputados_info_matrix, columns=matrix_columnas)

# Ordenarlo por lealtad
diputados_info_df = diputados_info_df.sort_values('lealtad', axis = 0)

# Guardar info
with open('../www/public/data/diputados.laealtad.json', 'w') as outfile:
    json.dump(diputados_info, outfile)

diputados_info_df.to_csv('./data/resumen.lealtad.csv', index = False, encoding='utf-8-sig')