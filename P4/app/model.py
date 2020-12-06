"""
	Alfonso García Martínez

	Desarrollo de Aplicaciones para Internet
	Práctica 4

	Script con toda la funcionalidad para persistencia/bases de datos
	(modelo)
"""

# Seguiremos usando PickleShareDB como base de datos
# para la información de los usuarios
from pickleshare import PickleShareDB
# Cliente de MongoDB para consultar SampleCollections
from pymongo import MongoClient
from datetime import date
# Para buscar documentos/entradas según _id
from bson.objectid import ObjectId


"""
	Funciones para datos de usuario (PickeShare)
"""

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


"""
	Funciones para base de datos MongoDB
"""


def get_collections():
	client = MongoClient("mongo", 27017)
	db = client['SampleCollections']
	return db.list_collection_names()



def get_all_entries(collection):
	client = MongoClient("mongo", 27017)
	db = client['SampleCollections']
	entries = db[collection].find()
	return [entry for entry in entries]



def search(collection,search_string):
	client = MongoClient("mongo", 27017)
	db = client['SampleCollections']
	distinct_results = {}
	results = [] # DEBUG
	# Obtener nombres de los campos (comunes a todos los documentos)
	fields = db[collection].find_one().keys()
	for field in list(fields):
		entries = db[collection].find({field: {'$regex': '.*'+search_string+'.*','$options' : 'i'}})
		for entry in entries:
			#distinct_results[entry['_id']]=entry
			results.append(entry) # DEBUG
	#return distinct_results.values()
	return results # DEBUG



def get_entry(collection,id):
	client = MongoClient("mongo", 27017)
	db = client['SampleCollections']
	return db[collection].find_one({'_id':ObjectId(id)})



def delete_entry(collection,id):
	client = MongoClient("mongo", 27017)
	db = client['SampleCollections']
	result = db[collection].delete_one({'_id':ObjectId(id)})
	return result.deleted_count==1



def update_entry(collection,id,new_data):
	client = MongoClient("mongo", 27017)
	db = client['SampleCollections']
	result = db[collection].update_one({'_id':ObjectId(id)},{"$set":new_data})
	return result.acknowledged



def create_entry(collection,new_data):
	client = MongoClient("mongo", 27017)
	db = client['SampleCollections']
	result = db[collection].insert_one(new_data)
	return result.acknowledged


def get_fields(collection):
	client = MongoClient("mongo", 27017)
	db = client['SampleCollections']
	return list(db[collection].find_one().keys())
