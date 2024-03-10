import numpy as np

def generate_random_matrix(n):
    return np.random.randint(1000000, size=(n, n)).tolist()

lista=[16,32,64,128,256,512,1024,2048]

# with open('numeros.txt', 'w') as archivo: 
#    for n in lista:
#        matriz = generate_random_matrix(n)
#        archivo.write('%s\n'%matriz)

with open('numeros.txt', 'r') as archivo: 
    listados = archivo.readlines()
    print(len(listados))
