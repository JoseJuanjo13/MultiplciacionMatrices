import time
from flask import Flask
from flask import render_template
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

    lista=[16,32,64,128,256]

    for index,n in enumerate(lista): 
        # Generar matrices aleatorias
        A = list(matrices[index])
        B = list(matrices[index])


        # Multiplicar las matrices
        # matriz1 = matrix_multiply_iterative(A, B)
        """
        matriz2 = naiv_on_array(A, B, len(A), len(A[0]), len(B[0]))
        matriz3 = naive_loop_unrolling_two(A, B, len(A), len(A[0]), len(B[0]))
        matriz4 = naive_loop_unrolling_four(A, B, len(A), len(A[0]), len(B[0]))
        matriz5 = winograd_original(A, B, len(A), len(A[0]), len(B[0]))
        matriz6 = winograd_scaled(A, B, len(A), len(A[0]), len(B[0]))
        matriz7 = strassen_naiv(A, B, len(A), len(A[0]), len(B[0]))
        matriz8 = strassen_winograd(A, B, len(A), len(A[0]), len(B[0]))
        matriz9 = [[0.0] * len(A) for _ in range(len(A))]
        sequential_block(matriz9, A, B, len(A), len(A[0]))
        """
        tiempo_matriz2 = calcular_tiempo(naiv_on_array, A, B, len(A), len(A[0]), len(B[0]))
        tiempo_matriz3 = calcular_tiempo(naive_loop_unrolling_two, A, B, len(A), len(A[0]), len(B[0]))
        tiempo_matriz4 = calcular_tiempo(naive_loop_unrolling_four,A, B, len(A), len(A[0]), len(B[0]))
        tiempo_matriz5 = calcular_tiempo(winograd_original, A, B, len(A), len(A[0]), len(B[0]))
        tiempo_matriz6 = calcular_tiempo(winograd_scaled,A, B, len(A), len(A[0]), len(B[0]))
        tiempo_matriz7 = calcular_tiempo(strassen_naiv, A, B, len(A), len(A[0]), len(B[0]))
        tiempo_matriz8 = calcular_tiempo(strassen_winograd, A, B, len(A), len(A[0]), len(B[0]))
        matriz9 = [[0.0] * len(A) for _ in range(len(A))]
        tiempo_matriz9 = calcular_tiempo(sequential_block, matriz9, A, B, len(A), len(A[0]))

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


    return render_template('sitio/resultados.html', tiempos=tiempos)

if __name__ == '__main__':
    app.run(debug=True)