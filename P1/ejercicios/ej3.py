"""
	Alfonso García Martínez

	Desarrollo de Aplicaciones para Internet
	Práctica 0

	Ejercicio 3
	La Criba de Eratóstenes es un sencillo algoritmo que permite
	encontrar todos los números primos menores de un número natural dado. Prográmelo.
"""

import math
from itertools import compress

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



if __name__ == '__main__':

	print('*******************************************************')
	print('************* CRIBA DE ERATÓSTENES ********************')
	print('*******************************************************\n')

	print('Introduzca un número entero:')
	int_num = int(input())

	# Llamada a la criba de Eratóstenes
	prime_numbers = eratosthenes_sieve(int_num)

	print('Números primos menores o iguales a {}:'.format(int_num))
	print(prime_numbers)
