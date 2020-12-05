"""
	Alfonso García Martínez

	Desarrollo de Aplicaciones para Internet
	Práctica 0

	Ejercicio 1
	Programe un mini-juego de "adivinar" un número (entre 1 y 100) que el
	ordenador establezca al azar. El usuario puede ir introduciendo números y
	el ordenador le responderá con mensajes del estilo "El número buscado el
	mayor / menor". El programa debe finalizar cuando el usuario adivine el
	número (con su correspondiente mensaje de felicitación) o bien cuando el
	usuario haya realizado 10 intentos incorrectos de adivinación.
"""

import random

# Generar un número entre 1 y 100
secret_number = random.randint(1,100)



if __name__ == "__main__":

	i = 1

	print()
	print("****************************************************")
	print("***************** ADIVINA 1 - 100 ******************")
	print("****************************************************")
	print()

	print("Por favor, introduzca un número entre 1 y 100")
	input_number = int(input())

	while(input_number != secret_number and i<10):
		i += 1
		if(input_number > secret_number):
			print("Incorrecto. El número introducido es demasiado alto.")
		else:
			print("Incorrecto. El número introducido es demasiado bajo.")
		print("Por favor, vuelva a introducir un número entre 1 y 100")
		input_number = int(input())

	if(input_number != secret_number):
		print("Intentos agotados. La respuesta correcta era: {}".format(secret_number))
	else:
		print("¡CORRECTO!")
