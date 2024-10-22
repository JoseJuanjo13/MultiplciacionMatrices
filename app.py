import datetime
import time
import mysql.connector
from mysql.connector import errorcode
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template
from utils.matrix_operations import matrix_multiply_iterative, generate_random_matrix
from utils.naivonarray import naiv_on_array
from utils.naiveloopunrollingtwo import naive_loop_unrolling_two
from utils.naiveloopunrollingfour import naive_loop_unrolling_four
from utils.winogradoriginal import winograd_original
from utils.winogradscaled import winograd_scaled  
from utils.strassennaiv import strassen_naiv
from utils.strassenwinograd import strassen_winograd 
from utils.sequentialblock import sequential_block 
from utils.parallel_block import parallel_block
from utils.enhanced_parallel_block import enhanced_parallel_block
from utils.parallel_block_iv4 import parallel_block_iv4
from utils.enhanced_parallel_block_iv5 import enhanced_parallel_block_iv5
from utils.sequential_block_v3 import sequential_block_v3
from utils.parallel_block_v4 import parallel_block_v4
from utils.parallel_block_iii_4 import parallel_block_iii_4

app=Flask(__name__)

matrices = []

with open('numeros.txt', 'r') as archivo: 
    listados = archivo.readlines()
    for string_original in listados:
        lista_de_strings = string_original[2:-2].split("], [")
        sublistas_de_strings = [sublista.replace("]", "").split(", ") for sublista in lista_de_strings]
        lista_de_listas = [[int(numero) for numero in sublista] for sublista in sublistas_de_strings]
        matrices.append(lista_de_listas)

def conectar_base_datos():
    try:
        conexion = mysql.connector.connect(
            user='root',  # Cambia esto por tu usuario de MySQL
            password='admin',  # Cambia esto por tu contraseña de MySQL
            host='localhost',
            database='matrices'  # Cambia esto por el nombre de tu base de datos
        )
        return conexion
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error de acceso: Usuario o contraseña incorrectos")
        elif error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Base de datos no existe")
        else:
            print(error)

def insertar_tiempo(id_algoritmo, tamano_matriz, tiempo_ejecucion, conexion, fecha_actual):
    try:
        cursor = conexion.cursor()
        query = "INSERT INTO Tiempos (id_algoritmo, tamano_matriz, tiempo_ejecucion, fecha) VALUES (%s, %s, %s, %s)"
        datos = (id_algoritmo, tamano_matriz, tiempo_ejecucion, fecha_actual)
        cursor.execute(query, datos)
        conexion.commit()
        cursor.close()
    except mysql.connector.Error as error:
        print("Error al insertar tiempo:", error)

@app.route('/')
def inicio():
    return render_template('sitio/index.html')

@app.route('/aplicacion')
def aplicacion():
    return render_template('sitio/aplicacion.html')

def calcular_tiempo(algoritmo, *args):
    inicio = time.time()
    algoritmo(*args)
    fin = time.time()
    return (fin - inicio) * 1_000_000

def promedio_tiempos():

    conexion = conectar_base_datos()
    cursor = conexion.cursor()

    lista=[8,16,32,64,128,256]

    graficos_bytes = []

    nombre_algoritmos = ['naiv_on_array', 'naive_loop_unrolling_two', 'naive_loop_unrolling_four',
                 'winograd_original', 'winograd_scaled', 'strassen_naiv', 'strassen_winograd', 'sequential_block',
                   'parallel_block', 'enhanced_parallel_block', 'parallel_block_iv4', 'enhanced_parallel_block_iv5',
                   'sequential_block_v3','parallel_block_v4','parallel_block_iii_4']

    for i,n in enumerate(lista): 
        # Resto del código para generar las matrices
        
        # Consultar los tiempos registrados en la base de datos para este tamaño de matriz
        tiempos_por_algoritmo = {}
        for algoritmo_id in range(1, 15):  # IDs de los algoritmos en la base de datos
            # Consulta SQL para obtener los tiempos de ejecución para este algoritmo y tamaño de matriz
            query = "SELECT tiempo_ejecucion FROM Tiempos WHERE id_algoritmo = %s AND tamano_matriz = %s"
            cursor.execute(query, (algoritmo_id, n))
            tiempos = cursor.fetchall()
            tiempos = [tiempo[0] for tiempo in tiempos]  # Convertir la lista de tuplas a lista de valores
            if tiempos:  # Verificar si se recuperaron tiempos de ejecución
                promedio_tiempo = sum(tiempos) / len(tiempos)
            else:
                promedio_tiempo = None
            tiempos_por_algoritmo[nombre_algoritmos[algoritmo_id-1]] = promedio_tiempo

        plt.figure(figsize=(10, 6))
        plt.bar(nombre_algoritmos, [tiempos_por_algoritmo.get(algoritmo, 0) for algoritmo in nombre_algoritmos], color='skyblue')
        plt.xlabel('Algoritmo')
        plt.ylabel('Tiempo promedio de ejecución (microsegundos)')
        plt.title(f'Tiempos promedio de ejecución para tamaño de matriz {n}')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        
        # Convertir el gráfico a formato base64 y añadirlo a la lista
        grafico_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()
        
        # Guardar el gráfico en el diccionario
        graficos_bytes.append((i,grafico_base64))

        

    return graficos_bytes

@app.route('/resultados')
def resultados():
    tiempos = []
    conexion = conectar_base_datos()
    lista=[8,16,32,64,128,256]

    graficos_base64 = []

    fecha_actual = datetime.datetime.now()
    for index,n in enumerate(lista): 
        # Generar matrices aleatorias
        A = list(matrices[index])
        B = list(matrices[index])

        tiempo_matriz2 = calcular_tiempo(naiv_on_array, A, B, len(A), len(A[0]), len(B[0]))
        tiempo_matriz3 = calcular_tiempo(naive_loop_unrolling_two, A, B, len(A), len(A[0]), len(B[0]))
        tiempo_matriz4 = calcular_tiempo(naive_loop_unrolling_four,A, B, len(A), len(A[0]), len(B[0]))
        tiempo_matriz5 = calcular_tiempo(winograd_original, A, B, len(A), len(A[0]), len(B[0]))
        tiempo_matriz6 = calcular_tiempo(winograd_scaled,A, B, len(A), len(A[0]), len(B[0]))
        tiempo_matriz7 = calcular_tiempo(strassen_naiv, A, B, len(A), len(A[0]), len(B[0]))
        tiempo_matriz8 = calcular_tiempo(strassen_winograd, A, B, len(A), len(A[0]), len(B[0]))
        matriz9 = [[0.0] * len(A) for _ in range(len(A))]
        tiempo_matriz9 = calcular_tiempo(sequential_block, matriz9, A, B, len(A), len(A[0]))
        tiempo_matriz10 = calcular_tiempo(parallel_block, A, B, len(A), len(A[0]))
        tiempo_matriz11 = calcular_tiempo(enhanced_parallel_block, A, B, len(A), len(A[0]))
        tiempo_matriz12 = calcular_tiempo(parallel_block_iv4, A, B, len(A))
        tiempo_matriz13 = calcular_tiempo(enhanced_parallel_block_iv5, A, B, len(A))
        tiempo_matriz14 = calcular_tiempo(sequential_block_v3, A, B, len(A))
        tiempo_matriz15 = calcular_tiempo(parallel_block_v4, A, B, len(A))
        tiempo_matriz16 = calcular_tiempo(parallel_block_iii_4, A, B, len(A))

        insertar_tiempo(1, n, tiempo_matriz2, conexion, fecha_actual)  
        insertar_tiempo(2, n, tiempo_matriz3, conexion, fecha_actual)  
        insertar_tiempo(3, n, tiempo_matriz4, conexion, fecha_actual)  
        insertar_tiempo(4, n, tiempo_matriz5, conexion, fecha_actual)  
        insertar_tiempo(5, n, tiempo_matriz6, conexion, fecha_actual)  
        insertar_tiempo(6, n, tiempo_matriz7, conexion, fecha_actual)  
        insertar_tiempo(7, n, tiempo_matriz8, conexion, fecha_actual)  
        insertar_tiempo(8, n, tiempo_matriz9, conexion, fecha_actual)
        insertar_tiempo(9, n, tiempo_matriz10, conexion, fecha_actual)   
        insertar_tiempo(10, n, tiempo_matriz11, conexion, fecha_actual)
        insertar_tiempo(11, n, tiempo_matriz12, conexion, fecha_actual)
        insertar_tiempo(12, n, tiempo_matriz13, conexion, fecha_actual)
        insertar_tiempo(13, n, tiempo_matriz14, conexion, fecha_actual)
        insertar_tiempo(14, n, tiempo_matriz15, conexion, fecha_actual)
        insertar_tiempo(15, n, tiempo_matriz16, conexion, fecha_actual)

        tiempos.append({
            'n': n,
            'matriz2': tiempo_matriz2,
            'matriz3': tiempo_matriz3,
            'matriz4': tiempo_matriz4,
            'matriz5': tiempo_matriz5,
            'matriz6': tiempo_matriz6,
            'matriz7': tiempo_matriz7,
            'matriz8': tiempo_matriz8,
            'matriz9': tiempo_matriz9,
            'matriz10': tiempo_matriz10,
            'matriz11': tiempo_matriz11,
            'matriz12': tiempo_matriz12,
            'matriz13': tiempo_matriz13,
            'matriz14': tiempo_matriz14,
            'matriz15': tiempo_matriz15,
            'matriz16': tiempo_matriz16
        })

        # Generar el gráfico y guardarlo en un buffer
        plt.figure(figsize=(10, 6))
        plt.bar(['naiv_on_array', 'naive_loop_unrolling_two', 'naive_loop_unrolling_four',
                 'winograd_original', 'winograd_scaled', 'strassen_naiv', 'strassen_winograd', 'sequential_block', 
                 'parallel_block', 'enhanced_parallel_block', 'parallel_block_iv4', 'enhanced_parallel_block_iv5','sequential_block_v3','parallel_block_v4', 'parallel_block_iii_4'],
                [tiempo_matriz2, tiempo_matriz3, tiempo_matriz4, tiempo_matriz5, tiempo_matriz6, tiempo_matriz7,
                  tiempo_matriz8, tiempo_matriz9, tiempo_matriz10, tiempo_matriz11, tiempo_matriz12, tiempo_matriz13, tiempo_matriz14, tiempo_matriz15, tiempo_matriz16],
                color='skyblue')
        plt.xlabel('Algoritmo')
        plt.ylabel('Tiempo de ejecución (microsegundos)')
        plt.title(f'Tiempos de ejecución para tamaño de matriz {n}')
        plt.xticks(rotation=45, ha='right')
        
        # Guardar el gráfico en un buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        
        # Convertir el gráfico a formato base64 y añadirlo a la lista
        grafico_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()
        graficos_base64.append(grafico_base64)

    calculo_promedio_tiempos = promedio_tiempos()

    graficos_base64 = [(i, grafico_base64) for i, grafico_base64 in enumerate(graficos_base64)]
    conexion.close()
    return render_template('sitio/resultados.html', tiempos=tiempos, graficos_base64=graficos_base64, calculo_promedio_tiempos=calculo_promedio_tiempos)


if __name__ == '__main__':
    app.run(debug=True)