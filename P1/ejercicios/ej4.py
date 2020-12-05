"""
	Alfonso García Martínez

	Desarrollo de Aplicaciones para Internet
	Práctica 0

	Ejercicio 4
	Cree un programa que lea de un fichero de texto un número entero n y escriba
	en otro fichero de texto el n-ésimo número de la sucesión de Fibonacci.
"""

import sys


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



def main(args):

	# Tomar nombres de los ficheros de entrada y salida de
	input_filename = args[1]
	output_filename = args[2]
	print(input_filename + ' ' + output_filename)
	# Abrir el fichero de entrada y leer el número que contiene
	try:
	    file = open(input_filename,'r')
	    input_str = file.readline()
	    input_num = int(input_str)
	except OSError as err:
	    print("Error del sistema: {0}".format(err))
	except ValueError:
	    print("Error al convertir dato leído en entero.")
	except:
	    print("Error inesperado:", sys.exc_info()[0])
	    raise
	file.close()


	print(input_num)
	# Calcular el n-ésimo elemento de la serie de Fibonacci
	fib = fibonacci(input_num)

	# Escribir el elemento en el fichero de salida
	file = open(output_filename,'w')
	file.write(str(fib))
	file.close()


if __name__ == '__main__':
	main(sys.argv)
