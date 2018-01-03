# Importar librerías a utilizar
import numpy as np
import pandas as pd
import json

# Cargar info de diputados
diputados_raw = json.load(open('../data-scraping/data/diputados.extended.1418.json'))

# Cargar Matriz CSV
matrix_votos = pd.read_csv('./data/votaciones.mensajes.texto.csv')
num_votaciones = {
    'total': matrix_votos['boletin'].count(),
    'total_tr01': matrix_votos['tramite'][matrix_votos['tramite'] == 'PRIMER TRÁMITE / PRIMER INFORME'].count(),
    'total_rec': matrix_votos['tramite'][matrix_votos['resultado'] == 'RECHAZADO'].count()
}

# Tipos de Trámites
tipos_tramites = list(matrix_votos['tramite'].astype('category').cat.categories)

# Obtener número de votaciones en donde todos aprobaron/ Todos desaprobaron
todos_deacuerdo = 0
todos_desacuerdo = 0
matrix_votos_np = matrix_votos.iloc[:, 8:].values
for x in matrix_votos_np:
    unique, counts = np.unique(x, return_counts=True)
    votos = dict(zip(unique, counts))
    for i in range(0,6):
        votos[i] = votos[i] if i in votos else 0
    if votos[2] + votos[3] == 0:
        todos_deacuerdo = todos_deacuerdo + 1
    if votos[1] == 0:
        todos_desacuerdo = todos_desacuerdo + 1

# Iniciar variable que guardará a los diputados y sus indicadores
diputados_info = []
diputados_info_matrix = []
partidos_info = []

# Función de cálculo de lealtad 
def calcularLealtad(rep, tramite = '', con_asistencia = False):
    global num_votaciones
    if con_asistencia:
        return round((rep['favor' + tramite]/ (num_votaciones['total' + tramite] - rep['ausencia' + tramite])), 2)
    else:
        return round((rep['favor' + tramite]/ (num_votaciones['total' + tramite])), 2)

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
        'lealtad_con_asistencia': 0,
        
        
        'favor_tr01': int(matrix_votos[diputado['nombre']][(matrix_votos[diputado['nombre']] == 1) & (matrix_votos['tramite'] == 'PRIMER TRÁMITE / PRIMER INFORME')].count()),
        'contra_tr01': int(matrix_votos[diputado['nombre']][(matrix_votos[diputado['nombre']] == 2) & (matrix_votos['tramite'] == 'PRIMER TRÁMITE / PRIMER INFORME')].count()),
        'abstencion_tr01': int(matrix_votos[diputado['nombre']][(matrix_votos[diputado['nombre']] == 3) & (matrix_votos['tramite'] == 'PRIMER TRÁMITE / PRIMER INFORME')].count()),
        'pareo_tr01': int(matrix_votos[diputado['nombre']][(matrix_votos[diputado['nombre']] == 4) & (matrix_votos['tramite'] == 'PRIMER TRÁMITE / PRIMER INFORME')].count()),
        'articulo_quinto_tr01': int(matrix_votos[diputado['nombre']][(matrix_votos[diputado['nombre']] == 5) & (matrix_votos['tramite'] == 'PRIMER TRÁMITE / PRIMER INFORME')].count()),
        'ausencia_tr01': 0,
        'lealtad_tr01': 0,
        'lealtad_con_asistencia_tr01': 0,
        
        'favor_rec': int(matrix_votos[diputado['nombre']][(matrix_votos[diputado['nombre']] == 1) & (matrix_votos['resultado'] == 'RECHAZADO')].count()),
        'contra_rec': int(matrix_votos[diputado['nombre']][(matrix_votos[diputado['nombre']] == 2) & (matrix_votos['resultado'] == 'RECHAZADO')].count()),
        'abstencion_rec': int(matrix_votos[diputado['nombre']][(matrix_votos[diputado['nombre']] == 3) & (matrix_votos['resultado'] == 'RECHAZADO')].count()),
        'pareo_rec': int(matrix_votos[diputado['nombre']][(matrix_votos[diputado['nombre']] == 4) & (matrix_votos['resultado'] == 'RECHAZADO')].count()),
        'articulo_quinto_rec': int(matrix_votos[diputado['nombre']][(matrix_votos[diputado['nombre']] == 5) & (matrix_votos['resultado'] == 'RECHAZADO')].count()),
        'ausencia_rec': 0,
        'lealtad_rec': 0,
        'lealtad_con_asistencia_rec': 0
        
        
    }
    
    rep['ausencia'] = int(num_votaciones['total'] - rep['favor'] - rep['contra'] - rep['abstencion'] - rep['pareo'] - rep['articulo_quinto'])
    rep['lealtad'] = calcularLealtad(rep)
    rep['lealtad_con_asistencia'] = calcularLealtad(rep, con_asistencia = True)
    
    rep['ausencia_tr01'] = int(num_votaciones['total_tr01'] - rep['favor_tr01'] - rep['contra_tr01'] - rep['abstencion_tr01'] - rep['pareo_tr01'] - rep['articulo_quinto_tr01'])
    rep['lealtad_tr01'] = calcularLealtad(rep, tramite = '_tr01')
    rep['lealtad_con_asistencia_tr01'] = calcularLealtad(rep, tramite = '_tr01', con_asistencia = True)
    
    rep['ausencia_rec'] = int(num_votaciones['total_rec'] - rep['favor_rec'] - rep['contra_rec'] - rep['abstencion_rec'] - rep['pareo_rec'] - rep['articulo_quinto_rec'])
    rep['lealtad_rec'] = calcularLealtad(rep, tramite = '_rec')
    rep['lealtad_con_asistencia_rec'] = calcularLealtad(rep, tramite = '_rec', con_asistencia = True)
    
    diputados_info.append(rep)
    matrix_columnas = [k for k, v in rep.items()]
    diputados_info_matrix.append([v for k, v in rep.items()])
    
    if diputado['comite_parlamentario'] not in partidos_info:
        partidos_info.append(diputado['comite_parlamentario'])

# Crear dataframe con la matriz resumen
diputados_info_df = pd.DataFrame(diputados_info_matrix, columns=matrix_columnas)

# Ordenarlo por lealtad
diputados_info_df = diputados_info_df.sort_values('lealtad', axis = 0)

# Guardar info
json_data = {
    'partidos': partidos_info,
    'diputados': diputados_info
}
with open('../www/public/data/diputados.laealtad.json', 'w') as outfile:
    json.dump(json_data, outfile)

diputados_info_df.to_csv('./data/resumen.lealtad.csv', index = False, encoding='utf-8-sig')