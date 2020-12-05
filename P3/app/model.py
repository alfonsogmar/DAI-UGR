"""
	Alfonso García Martínez

	Desarrollo de Aplicaciones para Internet
	Práctica 3

	Script con toda la funcionalidad para persistencia/bases de datos
	(modelo)
"""

# Usaremos PickleShareDB como base de datos basada en archivos
from pickleshare import PickleShareDB
from datetime import date

def signup_user(username,password):
	db = PickleShareDB('DAI_database')
	user_not_in_database = username not in db
	if user_not_in_database:
		# Usuario no existía en la base de datos: se registra
		today = date.today()
		db[username] = {'signup_date': today.strftime("%d/%m/%Y"),
		                'password': password}

	return user_not_in_database


def is_user_registered(username):
	db = PickleShareDB('DAI_database')
	return username in db


def get_users_hashed_password(username):
	db = PickleShareDB('DAI_database')
	return db[username]['password']



def get_user_info(username):
	db = PickleShareDB('DAI_database')
	return db[username].copy()


def update_email(username,new_email):
	db = PickleShareDB('DAI_database')
	db[username]['email'] = new_email
	db[username] = db[username]


def update_fullname(username, new_fullname):
	db = PickleShareDB('DAI_database')
	db[username]['fullname'] = new_fullname
	db[username] = db[username]
