"""
	Alfonso García Martínez

	Desarrollo de Aplicaciones para Internet
	Práctica 0

	Ejercicio 5
	Cree un programa que:
		- Genere aleatoriamente una cadena de [ y ].
		- Compruebe mediante una función si dicha secuencia está balanceada,
		  es decir, que se componga de parejas de corchetes
		  de apertura y cierre correctamente anidados.
"""

import random

# Genere aleatoriamente una cadena de [ y ]
def generate_random_bracket_sequence(max_length = 50):
	length = random.randint(2,max_length)
	br_string = ""
	for i in range(length):
		right_br = random.choice([True, False])
		if right_br:
			br_string += ']'
		else:
			br_string += '['

	return br_string


def bracket_sequence_is_balanced(br_string):
	br_count = 0
	for br in br_string:
		if br == '[':
			br_count += 1
		else:
			br_count -= 1
			if br_count < 0:
				return False
	return br_count == 0


def main():
	br_seq_list = ['[[][][[[]]]]',
	'[]',
	'[[][[]]]',
	'[][]',
	'][',
	'[[][[',
	'[]][[]']

	print('Batería de prueba')
	for br_seq in br_seq_list:
		result_str = 'Correcto' if bracket_sequence_is_balanced(br_seq) else 'Incorrecto'
		print(br_seq + ' -> ' + result_str)

	random_br_seq = generate_random_bracket_sequence()
	result_str = 'Correcto' if bracket_sequence_is_balanced(random_br_seq) else 'Incorrecto'
	print('Secuencia aleatoria de corchetes')
	print(random_br_seq + ' -> ' + result_str)

if __name__ == '__main__':
	main()
