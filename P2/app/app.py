"""
	Alfonso García Martínez

	Desarrollo de Aplicaciones para Internet
	Práctica 2

	Script principal con routing y llamadas a los métodos de Flask
"""

from flask import Flask
import ejercicios
import time
import random

app = Flask(__name__)


@app.route('/')
def root():
	#return 'Index'
	return app.send_static_file('index.html')



# Página no encontrada
@app.errorhandler(404)
def page_not_found(error):
	return app.send_static_file('page_not_found.html'), 404


# Prueba
@app.route('/hola_mundo')
def hello_world():
	return 'Hello, World!'


# Ejercicio 2
@app.route('/ordena/<num_sequence>')
def compare_sort_algs(num_sequence):

	str_array = num_sequence.split(',')
	num_array = [int(x) for x in str_array]

	# Ejecutar y medir tiempo del bubblesort
	bubble_start = time.time()
	arr_bubble = num_array.copy()
	ejercicios.bubblesort(arr_bubble)
	bubble_end = time.time()
	bubble_time = bubble_end - bubble_start

	# Ejecutar y medir tiempo del quicksort
	quick_start = time.time()
	arr_quick = ejercicios.quicksort(num_array)
	quick_end = time.time()
	quick_time = quick_end - quick_start

	arr_bubble_str = ','.join([str(x) for x in arr_bubble])
	arr_quick_str  = ','.join([str(x) for x in arr_quick])

	ret_str = '<h3>Array a ordenar:</h3>\n'
	ret_str += '<div>' + num_sequence + '</div>\n'

	ret_str += '<h3>Array ordenado por bubblesort:</h3>\n'
	ret_str += '<div>' + arr_bubble_str + '</div>\n'

	ret_str +='<h3>Tiempo ejecución bubblesort:</h3> <div>{:.10f}</div>'.format(bubble_time)
	ret_str += '<h3>Array ordenado por quicksort:</h3>'
	ret_str += '<div>' + arr_quick_str + '</div>\n'

	ret_str +='<h3>Tiempo ejecución quicksort:</h3><div>{:.10f}</div>'.format(quick_time)

	return ret_str


# Ejercicio 3
@app.route('/eratostenes/<number>')
def prime_numbers(number):
	n = int(number)
	primes = ejercicios.eratosthenes_sieve(n)
	return ', '.join([str(prime) for prime in primes])



# Ejercicio 4
@app.route('/fibonacci/<number>')
def fibonacci_number(number):
	n = int(number)
	fibo = ejercicios.fibonacci(n)
	return str(fibo)


# Ejercicio 5
@app.route('/corchetes/<sequence>')
def check_brackets_sequence(sequence):
	is_balanced = ejercicios.bracket_sequence_is_balanced(sequence)
	if is_balanced:
		ret_str = 'Secuencia balanceada'
	else:
		ret_str = 'Secuencia NO balanceada'
	return ret_str


# Ejercicio 6

@app.route('/palabra_y_letra/<string>')
def regex_word_and_letter(string):
	match = ejercicios.find_word_and_uppercase_character(string)
	if match is not None:
		found = match.string == match.group()
	else:
		found = False

	if found:
		ret_str = 'Palabra y letra ENCONTRADA'
	else:
		ret_str = 'Palabra y letra NO ENCONTRADA'

	return ret_str



@app.route('/email/<string>')
def regex_email_address(string):
	match = ejercicios.find_valid_email_address(string)
	if match is not None:
		found = match.string == match.group()
	else:
		found = False

	if found:
		ret_str = 'Dirección de correo electrónico ENCONTRADA'
	else:
		ret_str = 'Dirección de correo electrónico NO ENCONTRADA'

	return ret_str



@app.route('/tarjeta_credito/<string>')
def regex_credit_card_number(string):
	match = ejercicios.find_credit_card_number(string)
	if match is not None:
		found = match.string == match.group()
	else:
		found = False

	if found:
		ret_str = 'Número de tarjeta de crédito ENCONTRADA'
	else:
		ret_str = 'Número de tarjeta de crédito NO ENCONTRADA'

	return ret_str



@app.route('/svg')
def random_svg_shape():
	# Dimensiones del marco de SVG
	svg_width = 1000
	svg_height = 500
	svg_tag = ('<svg width=\"' + str(svg_width) + '\" height=\"' +
	           str(svg_height) +
			   '\" version=\"1.1\" xmlns=0.0.0.0:5000/svg>')

	# Forma de la figura y colores
	shape = random.choice(['rect', 'circle', 'ellipse','line']) # DEBUG
	stroke_width = 4
	stroke_color = random.choice(['red','black','blue','orange','green'])
	fill = random.choice(['transparent','black','blue','orange','red','green'])

	shape_colors_svg_params = ('stroke=\"' + stroke_color + '\" fill=\"' + fill
	                          + '\" stroke-width=\"' + str(stroke_width) + '\"')

	# Márgen de la figura con los límites del marco SVG
	margin = 5

	if shape == 'rect':
		x = random.randint(1,svg_width-margin)
		y = random.randint(1,svg_height-margin)
		max_rect_width = svg_width - x
		max_rect_height = svg_height - y
		rect_width = random.randint(1, abs(max_rect_width-margin))
		rect_height = random.randint(1, abs(max_rect_height-margin))


		svg_element = ('<rect x=\"'+ str(x) +'\" y=\"'+ str(y) + '\" width=\"' +
		                    str(rect_width) + '\" height=\"' + str(rect_height)+
							'\" ' + shape_colors_svg_params + '/>')
	elif shape == 'circle':
		x = random.randint(1,svg_width-margin)
		y = random.randint(1,svg_height-margin)
		max_radius = min(abs(svg_width - x),abs(svg_height - y),x,y)
		radius = random.randint(1,max_radius)

		svg_element = ('<circle cx=\"' + str(x) + '\" cy=\"' + str(y) +
		               '\" r=\"' + str(radius) + '\" ' + shape_colors_svg_params
					    + '/>')
	elif shape == 'ellipse':
		x = random.randint(1,svg_width-margin)
		y = random.randint(1,svg_height-margin)
		max_x_radius = min(abs(svg_width - x),x)
		max_y_radius = min(abs(svg_height - y),y)

		x_radius = random.randint(1,max_x_radius)
		y_radius = random.randint(1,max_y_radius)

		svg_element = ('<ellipse cx=\"' + str(x) + '\" cy=\"' + str(y) +
		               '\" rx=\"' + str(x_radius) + '\" ry=\"' + str(y_radius) +
					    '\" ' + shape_colors_svg_params + '/>')
	else:
		#shape == 'line'
		x1 = random.randint(1,svg_width-margin)
		x2 = random.randint(1,svg_width-margin)
		y1 = random.randint(1,svg_height-margin)
		y2 = random.randint(1,svg_height-margin)
		line_colors_svg_params = ('stroke=\"' + stroke_color +
		                        '\" stroke-width=\"' + str(stroke_width) + '\"')
		svg_element = ('<line x1=\"' + str(x1) + '\" x2=\"' + str(x2) +
		               '\" y1=\"' + str(y1) + '\" y2=\"' + str(y2) + '\" ' +
					   line_colors_svg_params + '/>')

		#<line x1="10" x2="50" y1="110" y2="150" stroke="orange" stroke-width="5"/>

	return svg_tag + svg_element + '</svg>'
