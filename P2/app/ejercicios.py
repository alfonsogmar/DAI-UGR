"""
	Alfonso García Martínez

	Desarrollo de Aplicaciones para Internet
	Práctica 2

	Script con funciones de los ejercicios de la práctica 1
"""

import math
from itertools import compress
import re
import time


"""
	Ejercicio 2 de la Práctica 1
	Algoritmos de ordenación
"""

# O(n²)
def bubblesort(array):
	n = len(array)
	# Límite
	for i in range(1,n):
		# Subir la burbuja
		for j in range(0, n-i):
			if array[j] > array[j+1]:
				array[j], array[j+1] = array[j+1], array[j]

# O(n log(n))
def quicksort(array, threshold=3):
	n = len(array)
	# Si el array no lleva al tamaño mínimo, se ordena
	# con uno de los métodos clásicos
	if(n <= threshold):
		sorted_arr = array.copy()
		#print("Antes de bubble: ",sorted_arr)
		bubblesort(sorted_arr)
		#print("Después de bubble: ",sorted_arr)
		return sorted_arr
	else:
		# Seleccionamos un elemento pivote y particionamos el array para que
		# todos los elementos a la izquierda del pivote sean menores que él,
		# y que todos los que estén a la sean
		"""
		print("Antes de particionar:")
		print(array)
		print('Intermedio ',array[n//2])
		"""
		p, part_array = partition(array)
		"""
		print("Después de particionar:")
		print(part_array)
		print('Pivote ',part_array[p])
		print("----------------------------------------")
		"""

		# Ordenamos por separado las partes del vector
		first_part = quicksort(part_array[0:p])
		second_part = quicksort(part_array[p:n])

		# Recomponemos el vector
		return (first_part + second_part)


# Particionar el array
# Devuelve la posición del elemento pivote y el array particionado
def partition(array):
	arr = array.copy()
	n = len(arr)
	pivot = arr[n-1]
	i = 0
	for j in range(n):
		if arr[j] < pivot:
			arr[i],arr[j] = arr[j],arr[i]
			i += 1
	arr[i],arr[n-1] = arr[n-1],arr[i]
	return i, arr


"""
	Ejercicio 3 de Práctica 0
	Criba de Eratóstenes
"""
def eratosthenes_sieve(n):
	# Generamos una lista de booleanos para tachar los números del 2 a n
	marks = [True]*n

	for i in range(2, math.floor(math.sqrt(n))+1):
		# Si el número no ha sido tachado, se añade a la lista de primos
		if marks[i]:
			# Se tachan todos los números múltiplos del primo
			for multip in range(i+i,n,i):
				marks[multip] = False

	# Comprimimos en una lista los números no tachados
	prime_nums = list(compress(range(n+1), marks))[2:]   # [2:] para no incluir al 0 ni al 1

	return prime_nums


"""
	Ejercicio 4 de la Práctica 0
	Sucesión de Fibonacci
"""

# Calcular n-ésimo elemento de la sucesión de Fibonacci.
# Se empieza desde 1, de forma que el primer elemento de la serie sería
# el 1-ésimo, es decir, el primer elemento corresponde
# al elemento para el que n=1
def fibonacci(n):
	# Caso base
	if n<=2:
		fibo = 1
	else:
		prev_fibo = 1
		fibo = 1
		for i in range(2,n):
			prev_fibo,  fibo = fibo, prev_fibo + fibo
	return fibo


"""
	Ejercicio 5 de la Práctica 0
	Secuencia de corchetes balanceada
"""

def bracket_sequence_is_balanced(bracket_sequence_string):
	br_count = 0
	for br in bracket_sequence_string:
		# Corchete izquierdo: incrementar contador
		if br == '[':
			br_count += 1
		# Corchete derecho: decrementar contador
		elif br == ']':
			br_count -= 1
			# Si contador llega a ser negativo en algún momento,
			# la secuencia no está balanceada
			if br_count < 0:
				return False
		# Si se encuentra un caracter que no es corchete,
		# la secuencia no será válida
		else:
			return False
	# Si el contador termina igual a 0, significa que para cada
	# corchete izquierdo que abre, hay un corchete derecho que cierra
	# (a su derecha)
	return br_count == 0


"""
	Ejercicio 6 de Práctica 0
	Expresiones regulares
"""

# Palabra + letra mayúscula
def find_word_and_uppercase_character(string):
	return re.search("[A-z]+ [A-Z]",string)

# Dirección de correo electrónico
def find_valid_email_address(string):
	return re.search("\w+@\w+\.[a-z]+",string)

# Número de tarjeta de crédito
def find_credit_card_number(string):
	#return re.search("[0-9]{4}((-|\s)[0-9]{4}){3}",string)
	return re.search("[0-9]{4}(((-[0-9]{4}){3})|((\s[0-9]{4}){3}))",string)
