"""
	Alfonso García Martínez

	Desarrollo de Aplicaciones para Internet
	Práctica 0

	Ejercicio 6
	Utilizando expresiones regulares realice funciones para:
		- Identificar cualquier palabra seguida de un espacio y
		  una única letra mayúscula (por ejemplo: Apellido N).
		- Identificar correos electrónicos válidos
		  (empieza por una expresión genérica y ve refinándola todo lo posible).
		- Identificar números de tarjeta de crédito cuyos dígitos estén
		  separados por - o espacios en blanco cada paquete de cuatro dígitos:
		  1234-5678-9012-3456 ó 1234 5678 9012 3456.
"""


import re

def find_word_and_uppercase_character(string):
	match = re.search("[A-z]+ [A-Z]",string)
	if match is not None:
		return match
	#	return match.string == match.group
	else:
		return False


def find_valid_email_address(string):
	match = re.search("\w+@\w+\.[a-z]+",string)
	if match is not None:
		return match
	#	return match.string == match.group
	else:
		return False



def find_credit_card_number(string):
	match = re.search("[0-9]{4}((-|\s)[0-9]{4}){3}",string)
	if match is not None:
		return match
	#	return match.string == match.group
	else:
		return False


if __name__ == '__main__':
	# Probar palabra + letra mayúscula
	m1 = find_word_and_uppercase_character('AdsadDSA A')
	print(m1.group())
	m1 = find_word_and_uppercase_character('342423 G dsadDSas AG dsaDSAdsa T dsadDSA r')
	print(m1.group())

	# Probar dirección de correo electrónico
	m2 = find_valid_email_address('pep@dsa.com')
	print(m2.group())
	m2 = find_valid_email_address('fdsf@sdfa fdsfdsa fdsafsda@dsad.dfdsfrew fds')
	print(m2.group())

	# Probar número de tarjeta de crédito
	m3 = find_credit_card_number('3456 2345 2345 6543')
	print(m3.group())
	m3 = find_credit_card_number('4325-6247-2845-2998')
	print(m3.group())
	m3 = find_credit_card_number('432d5-624d7-284d5-29d98')
	print(m3)
	m3 = find_credit_card_number('4325-6247-2845-2998-2998')
	print(m3)
