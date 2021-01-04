from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from DAI_app.models import Autor, Libro, Prestamo
from DAI_app.forms import AuthorForm, BookForm, LoanForm
# Create your views here.


"""
		CÓMO HACER CONSULTAS
		https://docs.djangoproject.com/en/3.1/topics/db/queries/
"""

def index(request):
    #return HttpResponse('Hello World!')
	context = {}
	return render(request,'index.html',context)



def select_table(request):
	tables = {
		'Autores': 'authors',
		'Libros': 'books',
		'Préstamos': 'loans'
	}
	context = {
		'tables' : tables
	}
	return render(request,'select_table.html',context)


def choose_table(request):
	if request.method == 'POST':
		table = request.POST.get('table_name')
		return redirect(table)
	else:
		return redirect('index')



"""
	Views de Autor
"""

class AuthorList(ListView):
	model = Autor
	template_name = 'authors_table.html'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(AuthorList, self).get_context_data(**kwargs)
		# Get the blog from id and add it to the context
		#context['some_data'] = 'This is just some data'
		context['fields'] = Autor._meta.get_fields()
		return context

	# Sobreescribir método 'get_queryset'
	# para permitir búsquedas a través de formulario
	def get_queryset(self):
		name = self.request.GET.get('name')
		object_list = self.model.objects.all()
		if name:
			object_list = object_list.filter(nombre__icontains=name)
		return object_list



class AuthorCreate(CreateView):
	model = Autor
	template_name = 'author_creation.html'
	form_class = AuthorForm
	# URL de AuthorList
	success_url = reverse_lazy('authors')

	"""
	# Sobreescribir método 'get_context_data'
	def get_context_data(self, **kwargs):
		context = super(AuthorCreate).get_context_data()
		# Añadir formulario al contexto
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)
		# Segundo formulario?
		return context
	"""

	"""
	def post(self, request, *args, **kwargs):
		form = self.form_class
		if form.is_valid():
			form_req = form.save() # commit=False ???
			form_req.save()
			return HttpResponseRedirect(self.get_success_url)
		else:
			pass
	"""


# ¿Sobreescribit get() o get_context_data() para obtener
# lista de libros del autor?
class AuthorDetail(DetailView):
	model = Autor
	template_name = 'author_details.html'

	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(AuthorDetail, self).get_context_data(**kwargs)
		context['books'] = self.object.libro_set.all()

		return context



class AuthorDelete(DeleteView):
	model = Autor
	template_name = 'author_delete_confirm.html'
	success_url = reverse_lazy('authors')



class AuthorUpdate(UpdateView):
	model = Autor
	form_class = AuthorForm
	template_name = 'author_update.html'
	success_url = reverse_lazy('authors')


"""
	Views de Libro
"""

class BookList(ListView):
	model = Libro
	template_name = 'books_table.html'

	# Sobreescribir método 'get_queryset'
	# para permitir búsquedas a través de formulario
	def get_queryset(self):
		#title = self.kwargs.get('title', '')
		title = self.request.GET.get('title')
		object_list = self.model.objects.all()
		if title:
			object_list = object_list.filter(titulo__icontains=title)
		return object_list

class BookCreate(CreateView):
	model = Libro
	template_name = 'book_creation.html'
	form_class = BookForm
	# URL de AuthorList
	success_url = reverse_lazy('books')


class BookDetail(DetailView):
	model = Libro
	template_name = 'book_details.html'



class BookDelete(DeleteView):
	model = Libro
	template_name = 'book_delete_confirm.html'
	success_url = reverse_lazy('authors')


class BookUpdate(UpdateView):
	model = Libro
	form_class = BookForm
	template_name = 'book_update.html'
	success_url = reverse_lazy('books')

"""
	Views de Préstamo
"""

class LoanList(ListView):
	model = Prestamo
	template_name = 'loans_table.html'


class LoanCreate(CreateView):
	model = Prestamo
	form_class = LoanForm
	template_name = 'loan_creation.html'
	success_url = reverse_lazy('loans')


class LoanDelete(DeleteView):
	model = Prestamo
	template_name = 'loan_delete.html'
	success_url = reverse_lazy('loans')
