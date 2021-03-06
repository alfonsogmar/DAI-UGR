"""
	Alfonso García Martínez

	Desarrollo de Aplicaciones para Internet
	Práctica 4

	Script principal con routing y llamadas a los métodos de Flask
	(controlador)
"""

from flask import Flask, render_template, request, flash, url_for, redirect, session
import time
import random
import model
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # para usar mensajes flash

MAX_VISITED_PAGES = 3
ENTRIES_PER_PAGE = 6


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




@app.route('/mongo')
def collection_selection():
	update_visited_pages('Selección de colección',url_for('collection_selection'))
	collections = model.get_collections()
	return render_template('collection_selection.html',collection_list=collections)





@app.route('/mongo/<collection>', methods=['GET', 'POST'])
def show_collection_table(collection):
	update_visited_pages('Tabla de colección',url_for('show_collection_table',collection=collection))
	if request.method == 'GET':
		# Variables GET
		search_value = request.args.get('search')
		page = request.args.get('page')

		# Buscar en MongoDB (si así se indica)
		not_searching = search_value is None
		if not_searching:
			# Datos del cuerpo de la tabla, extraídos de la colección de MongoDB
			collection_data = model.get_all_entries(collection)
		else:
			#return search_value
			collection_data = model.search(collection,search_value)

		is_empty = len(collection_data)==0

		# Control página
		page_num = 1 if (page is None) else max(int(page),1)
		last_page=max(len(collection_data)//ENTRIES_PER_PAGE,1)
		if page_num > last_page:
			page_num = last_page
		is_last_page = (page_num==last_page)
		is_first_page = (page_num==1)

		if is_empty:
			collection_data_page = []
			collection_headers = []
		else:
			collection_data_page = collection_data[(page_num-1)*ENTRIES_PER_PAGE:page_num*ENTRIES_PER_PAGE]

			# Cabecera de la tabla (claves de cualquier elemento de la lista)
			collection_headers = collection_data[0].keys() if not is_empty else None



		return render_template('collection_table.html',collection=collection,data=collection_data_page,data_headers=collection_headers,no_results=is_empty,page=str(page_num),search_value=search_value,prev_page=str(page_num-1),next_page=str(page_num+1),is_last_page=is_last_page,is_first_page=is_first_page,not_searching=not_searching)






@app.route('/load_collection', methods=['GET', 'POST'])
def load_collection():
	if request.method == 'POST':
		# Nombre de la colección (obtenido por POST del formulario)
		collection_name = request.form['collection-select']
		return redirect(url_for('show_collection_table',collection=collection_name))
	else:
		flash('Error al leer seleccionar la colección','alert-danger')
		return redirect(url_for('root'))



@app.route('/mongo/<collection>/confirm_deletion/<id>')
def confirm_deletion(collection,id):
	data = model.get_entry(collection,id)
	return render_template('confirm_deletion.html',collection=collection,entry=data)




@app.route('/mongo/<collection>/edit_form/<id>')
def edit_entry(collection,id):
	# Obtener datos de la entrada desde la BD
	data = model.get_entry(collection,id)
	return render_template('edit_form.html',collection=collection,data=data)

@app.route('/mongo/<collection>/create_form')
def create_entry(collection):
	# Obtener datos de la entrada desde la BD
	fields = model.get_fields(collection)
	return render_template('create_form.html',collection=collection,fields=fields)




@app.route('/mongo/<collection>/delete/<id>', methods=['GET', 'POST'])
def delete(collection,id):
	# Borrar en base de datos Mongo
	deleted = model.delete_entry(collection,id)
	if deleted:
		flash('Entrada borrada con éxito','alert-success')
	else:
		flash('Error al intentar borrar','alert-danger')
	return redirect(url_for('show_collection_table',collection=collection))


@app.route('/mongo/<collection>/update/<id>', methods=['GET', 'POST'])
def update(collection,id):
	if request.method == 'POST':
		new_data = dict(request.form.copy())
		updated = model.update_entry(collection,id,new_data)
		if updated:
			flash('Entrada editada con éxito','alert-success')
		else:
			flash('Error al intentar editar entrada','alert-danger')
	else:
		flash('Error al intentar editar entrada','alert-danger')
	return redirect(url_for('show_collection_table',collection=collection))


@app.route('/mongo/<collection>/create', methods=['GET','POST'])
def create(collection):
	if request.method == 'POST':
		new_data = dict(request.form.copy())
		created = model.create_entry(collection,new_data)
		if created:
			flash('Entrada creada con éxito','alert-success')
		else:
			flash('Error al intentar crear entrada','alert-danger')
	else:
		flash('Error al intentar crear entrada','alert-danger')
	return redirect(url_for('show_collection_table',collection=collection))


"""


@app.route('/search/<collection>', methods=['GET', 'POST'])
def search(collection):
	if request.method == 'GET':
		pass
	else:
		flash('Error al leer seleccionar la colección','alert-danger')
		return redirect(url_for('root'))
"""


# Página no encontrada
@app.errorhandler(404)
def page_not_found(error):
	return app.send_static_file('page_not_found.html'), 404
