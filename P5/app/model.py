"""
	Alfonso García Martínez

	Desarrollo de Aplicaciones para Internet
	Práctica 5

	Script con toda la funcionalidad para persistencia/bases de datos
	(modelo)
"""

from datetime import date
# PickleShareDB como base de datos
# para la información de los usuarios
from pickleshare import PickleShareDB
# Cliente de MongoDB para consultar SampleCollections
from pymongo import MongoClient
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

def set_correct_id(item):
	no_id_item = item.copy()
	del(no_id_item['_id'])
	item_with_id = {'id': str(item['_id'])}
	for key in no_id_item:
		item_with_id[key] = no_id_item[key]
	return item_with_id



def get_all_entries(collection):
	client = MongoClient("mongo", 27017)
	db = client['SampleCollections']
	entries = db[collection].find()
	return [entry for entry in entries]



def get_field_type(collection,field):
	client = MongoClient("mongo", 27017)
	db = client['SampleCollections']
	test_entry = db[collection].find_one()
	return type(test_entry[field])



def search(collection,search_string):
	client = MongoClient("mongo", 27017)
	db = client['SampleCollections']
	distinct_results = {}
	results = [] # DEBUG
	# Obtener nombres de los campos (comunes a todos los documentos)
	fields = db[collection].find_one().keys()
	for field in list(fields):
		if get_field_type(collection,field) is str:
			entries = db[collection].find({field: {'$regex': '.*'+search_string+'.*','$options' : 'i'}})
		elif get_field_type(collection,field) is int and search_string.isdigit():
			entries = db[collection].find({field: int(search_string)})
		else:
			entries = []
		for entry in entries:
			distinct_results[str(entry['_id'])]=entry
			results.append(entry) # DEBUG
	return list(distinct_results.values())
#return results # DEBUG




def search_by_field(collection,field,search_string):
	client = MongoClient("mongo", 27017)
	db = client['SampleCollections']
	entries = db[collection].find({field: {'$regex': '.*'+search_string+'.*','$options' : 'i'}})
	return [entry for entry in entries]




def get_entry(collection,id):
	client = MongoClient("mongo", 27017)
	db = client['SampleCollections']
	entry = db[collection].find_one({'_id':ObjectId(id)})
	if entry is None:
		entry = {}
	return entry



def delete_entry(collection,id):
	client = MongoClient("mongo", 27017)
	db = client['SampleCollections']
	result = db[collection].delete_one({'_id':ObjectId(id)})
	return result.deleted_count==1


def delete_entry_get_id(collection,id):
	client = MongoClient("mongo", 27017)
	db = client['SampleCollections']
	result = db[collection].delete_one({'_id':ObjectId(id)})
	if result.deleted_count == 1:
		return {'id': str(id)}
	else:
		return {}


def update_entry(collection,id,new_data):
	client = MongoClient("mongo", 27017)
	db = client['SampleCollections']
	for field in new_data:
		if get_field_type(collection,field) is int and new_data[field].isdigit():
			new_data[field] = int(new_data[field])
	result = db[collection].update_one({'_id':ObjectId(id)},{"$set":new_data})
	return result.acknowledged



def update_entry_get_data(collection,id,new_data):
	client = MongoClient("mongo", 27017)
	db = client['SampleCollections']
	# Campos en su orden original
	original_sorted_field = list(db[collection].find_one().keys())
	# Cambiar año a tipo 'int'
	for field in new_data:
		if field not in original_sorted_field:
			return {'error':0}
		if get_field_type(collection,field) is int and new_data[field].isdigit():
			new_data[field] = int(new_data[field])
	"""
	# Reordenar campos
	sorted_new_data = {}
	for field in original_sorted_field:
		if field != '_id':
			sorted_new_data[field] = new_data[field]
	"""
	# Actualizar/editar datos en la BD
	result = db[collection].update_one({'_id':ObjectId(id)},{"$set":new_data})
	if result.modified_count==1:
		return set_correct_id(db[collection].find_one({'_id':ObjectId(id)}))
	else:
		return {}



def create_entry(collection,new_data):
	client = MongoClient("mongo", 27017)
	db = client['SampleCollections']
	for field in new_data:
		if get_field_type(collection,field) is int and new_data[field].isdigit():
			new_data[field] = int(new_data[field])
	result = db[collection].insert_one(new_data)
	return result.acknowledged


def create_entry_get_data(collection,new_data):
	client = MongoClient("mongo", 27017)
	db = client['SampleCollections']
	# Campos en su orden original
	original_sorted_field = list(db[collection].find_one().keys())
	# Cambiar año a tipo 'int'
	for field in new_data:
		if get_field_type(collection,field) is int and new_data[field].isdigit():
			new_data[field] = int(new_data[field])
	# Reordenar campos
	sorted_new_data = {}
	for field in original_sorted_field:
		if field != '_id':
			new_data_value = new_data.get(field,False)
			if not new_data_value:
				return {}
			sorted_new_data[field] = new_data_value
	# Insertar datos
	result = db[collection].insert_one(sorted_new_data)
	if result.acknowledged:
		#item = db[collection].find_one({'_id':ObjectId(result.inserted_id)})
		item = db[collection].find_one({'_id':ObjectId(result.inserted_id)})
		return set_correct_id(item)
	else:
		return {}


def get_fields(collection):
	client = MongoClient("mongo", 27017)
	db = client['SampleCollections']
	return list(db[collection].find_one().keys())



def set_correct_id_field(items):
	return [set_correct_id(item) for item in items]



# En todos los items, cambiamos campo '_id' por campo 'id'
def get_all_entries_correct_id(collection):
	return set_correct_id_field(get_all_entries(collection))
	#return get_all_entries(collection)



def search_by_field(collection,field,search_string):
	client = MongoClient("mongo", 27017)
	db = client['SampleCollections']
	if get_field_type(collection,field) is str:
		entries = db[collection].find({field: {'$regex': '.*'+search_string+'.*','$options' : 'i'}})
	elif get_field_type(collection,field) is int and search_string.isdigit():
		entries = db[collection].find({field: int(search_string)})
	else:
		entries = []
	return set_correct_id_field([entry for entry in entries])


def get_entry_correct_id(collection,id):
	entry = get_entry(collection,id)
	if entry != {}:
		entry = set_correct_id(entry)
	return entry
