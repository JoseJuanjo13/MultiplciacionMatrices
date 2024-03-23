import time
import mysql.connector
from mysql.connector import errorcode
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

def insertar_tiempo(id_algoritmo, tamano_matriz, tiempo_ejecucion, conexion):
    try:
        cursor = conexion.cursor()
        query = "INSERT INTO Tiempos (id_algoritmo, tamano_matriz, tiempo_ejecucion) VALUES (%s, %s, %s)"
        datos = (id_algoritmo, tamano_matriz, tiempo_ejecucion)
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
    return fin - inicio

@app.route('/resultados')
def resultados():
    tiempos = []
    conexion = conectar_base_datos()
    lista=[16,32,64,128,256]

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

        insertar_tiempo(1, n, tiempo_matriz2, conexion)  # ID 1 corresponde a 'naiv_on_array'
        insertar_tiempo(2, n, tiempo_matriz3, conexion)  # ID 2 corresponde a 'naive_loop_unrolling_two'
        insertar_tiempo(3, n, tiempo_matriz4, conexion)  # ID 3 corresponde a 'naive_loop_unrolling_four'
        insertar_tiempo(4, n, tiempo_matriz5, conexion)  # ID 4 corresponde a 'winograd_original'
        insertar_tiempo(5, n, tiempo_matriz6, conexion)  # ID 5 corresponde a 'winograd_scaled'
        insertar_tiempo(6, n, tiempo_matriz7, conexion)  # ID 6 corresponde a 'strassen_naiv'
        insertar_tiempo(7, n, tiempo_matriz8, conexion)  # ID 7 corresponde a 'strassen_winograd'
        insertar_tiempo(8, n, tiempo_matriz9, conexion)  # ID 8 corresponde a 'sequential_block'

        tiempos.append({
            'n': n,
            'matriz2': tiempo_matriz2,
            'matriz3': tiempo_matriz3,
            'matriz4': tiempo_matriz4,
            'matriz5': tiempo_matriz5,
            'matriz6': tiempo_matriz6,
            'matriz7': tiempo_matriz7,
            'matriz8': tiempo_matriz8,
            'matriz9': tiempo_matriz9
        })
      

    conexion.close()
    return render_template('sitio/resultados.html', tiempos=tiempos)

if __name__ == '__main__':
    app.run(debug=True)