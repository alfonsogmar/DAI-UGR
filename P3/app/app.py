"""
	Alfonso García Martínez

	Desarrollo de Aplicaciones para Internet
	Práctica 3

	Script principal con routing y llamadas a los métodos de Flask
	(controlador)
"""

from flask import Flask, render_template, request, flash, url_for, redirect, session
import ejercicios
import time
import random
import model
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # para usar mensajes flash

MAX_VISITED_PAGES = 3

# Añade el nombre y la URL de la página actual a la lista
# de últimas páginas visitadas
def update_visited_pages(page_name,page_url):
	current_page_entry = {'name':page_name,'url':page_url}
	# Crear lista de páginas si la actual es la primera en ser visitada
	if 'visited_pages' not in session:
		session['visited_pages'] = [current_page_entry]
	else:
		# Situal página actual al principio de la lista
		visited_pages_list = session['visited_pages']
		visited_pages_list.insert(0,current_page_entry)
		# Eliminar última página si se excede el límite de páginas almacenadas
		if len(visited_pages_list) > MAX_VISITED_PAGES:
			visited_pages_list.pop()
		session['visited_pages'] = visited_pages_list

	for page in session['visited_pages']:
		app.logger.debug(page)

@app.route('/')
def root():
	update_visited_pages('Inicio',url_for('root'))
	return render_template('index.html')


@app.route('/signup')
def signup():
	if 'logged_in' not in session:
		update_visited_pages('Registrarse',url_for('signup'))
		return render_template('signup.html')
	elif not session['logged_in']:
		update_visited_pages('Registrarse',url_for('signup'))
		return render_template('signup.html')
	else:
		flash('Imposible registrarse si ya se ha iniciado sesión')
		return redirect(url_for('root'))


@app.route('/signup_user', methods=['GET','POST'])
def signup_user():
	if request.method == 'POST':
		username = '@'+request.form['username']
		passwd = generate_password_hash(request.form['passwd'])
		success = model.signup_user(username,passwd)
		if success:
			session['logged_in'] = True
			session['username'] = username
			flash('Te has registrado con éxito como {}, ¡enhorabuena!'.format(username),'alert-success')
			return redirect(url_for('root'))
		else:
			flash('Ese nombre de usuario ya está registrado','alert-danger')
			return redirect(url_for('signup'))


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = '@'+request.form['username']
		if not model.is_user_registered(username):
			flash('¡Vaya! Parece que no existe ese usuario o la contraseña es incorrecta','alert-danger')
			return redirect(url_for('root'))
		else:
			hashed_psswd = model.get_users_hashed_password(username)
			correct_psswd = check_password_hash(hashed_psswd,request.form['passwd'])
			if correct_psswd:
				session['logged_in'] = True
				session['username'] = username
				flash('Bienvenido, {}'.format(username),'alert-success')
				return redirect(url_for('root'))
			else:
				flash('¡Vaya! Parece que no existe ese usuario o la contraseña es incorrecta','alert-danger')
				return redirect(url_for('root'))




@app.route('/logout', methods=['GET', 'POST'])
def logout():
	session['logged_in'] = False
	flash('Has cerrado sesión. ¡Hasta pronto!','alert-success')
	return redirect(url_for('root'))


@app.route('/profile')
def profile():
	if session['logged_in']:
		# Cargar los datos del usuario desde la base de datos
		user_info = model.get_user_info(session['username'])
		user_info['email'] = user_info.get('email',False)
		user_info['fullname'] = user_info.get('fullname',False)
		update_visited_pages('Perfil',url_for('profile'))
		return render_template('profile_page.html',user_info=user_info)
	else:
		flash('Para entrar en la página de perfil, debes haber iniciado sesión','alert-danger')
		return redirect(url_for('root'))

@app.route('/update_user_info/<info_kind>', )
def update_user_info(info_kind):
	page_name = 'Editar email' if info_kind == 'email' else 'Editar nombre completo'
	update_visited_pages(page_name,url_for('update_user_info',info_kind=info_kind))
	return render_template('edit_user_info.html',user_info_kind=info_kind)


@app.route('/update_email', methods=['GET', 'POST'])
def update_email():
	if request.method == 'POST':
		if session['logged_in']:
			model.update_email(session['username'],request.form['new_user_info'])
	return redirect(url_for('profile'))




@app.route('/update_fullname', methods=['GET', 'POST'])
def update_fullname():
	if request.method == 'POST':
		if session['logged_in']:
			model.update_fullname(session['username'],request.form['new_user_info'])
	return redirect(url_for('profile'))





@app.route('/guess_the_number/<attempt>', methods=['GET', 'POST'])
def guess_the_number_game(attempt):
	attempt_num = int(attempt)
	num=None
	update_visited_pages('Ejercicio 1: Adivina 1-100',url_for('guess_the_number_game',attempt='0'))
	if attempt_num == 0:
		session['correct_number'] = random.randint(1,100)
	elif request.method == 'POST':
		num = int(request.form['number'])
		if num < session['correct_number']:
			flash('El número introducido es demasiado bajo','alert-danger')
		elif num > session['correct_number']:
			flash('El número introducido es demasiado alto','alert-danger')
	return render_template('exercise_1.html',attempt_num=str(attempt_num+1),
	                       correct_num=str(session['correct_number']),num=str(num))




"""
@app.route('/check_number', methods=['GET', 'POST'])
def check_number():

	else:
		return redirect(url_for('guess_the_number_game'))
"""


# Página no encontrada
@app.errorhandler(404)
def page_not_found(error):
	return app.send_static_file('page_not_found.html'), 404




"""
	FUNCIONES NO USADAS EN ESTA PRÁCTICA
"""


@app.route('/ejercicios_static')
def assigment():
	#return 'Index'
	return app.send_static_file('index.html')




# Prueba
@app.route('/hola_mundo')
def hello_world():
	return 'Hello, World!'

"""
	Métodos para ejercicios
"""


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
