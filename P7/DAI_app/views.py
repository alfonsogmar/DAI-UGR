from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse, reverse_lazy
# Views genéricos
from django.views.generic import ListView, CreateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
# Modelos y formularios
from DAI_app.models import Autor, Libro, Prestamo
from DAI_app.forms import AuthorForm, BookForm, LoanForm, LoanAuthorChoiceForm
# Autentificación
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin

# Create your views here.


def index(request):
    #return HttpResponse('Hello World!')
	context = {}
	return render(request,'index.html',context)


"""
	Mixin para asegurarse de que solo los usuarios staff puedan
	alterar las tablas de libros y autores
"""

class StaffRequiredMixin(AccessMixin):
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_staff:
			return self.handle_no_permission()
		return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)


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



class AuthorCreate(StaffRequiredMixin,CreateView):
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



class AuthorDelete(StaffRequiredMixin,DeleteView):
	model = Autor
	template_name = 'author_delete_confirm.html'
	success_url = reverse_lazy('authors')



class AuthorUpdate(StaffRequiredMixin,UpdateView):
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

class BookCreate(StaffRequiredMixin,CreateView):
	model = Libro
	template_name = 'book_creation.html'
	form_class = BookForm
	# URL de AuthorList
	success_url = reverse_lazy('books')


class BookDetail(DetailView):
	model = Libro
	template_name = 'book_details.html'



class BookDelete(StaffRequiredMixin,DeleteView):
	model = Libro
	template_name = 'book_delete_confirm.html'
	success_url = reverse_lazy('authors')


class BookUpdate(StaffRequiredMixin,UpdateView):
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


"""
	Views para autentificación
"""


def authenticate_user(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	user = authenticate(request, username=username, password=password)
	if user is not None:
	    login(request, user)
	    # Redirect to a success page.
	else:
		# Return an 'invalid login' error message.
		return redirect('login_error')


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('registered_user')
    template_name = 'registration/signup.html'



def login_error(request):
	context = {}
	return render(request,'registration/login_error.html',context)



def registered_user(request):
	context = {}
	return render(request,'registration/registered_user.html',context)



# Lista de préstamos de un usuario (necesario iniciar sesión)
@login_required
def list_user_loans(request):
	# Obtener préstamos del usuario actual
	loans = Prestamo.objects.filter(usuario=request.user)
	context = {'loans': loans}
	# return render(request, 'user_loans.html', context)
	return render(request,'user_loans_table.html',context)



@login_required
def take_out_loan(request):
	# Formulario para pedir un préstamo (elegir libro)
	form = LoanAuthorChoiceForm
	context = {'form': form}
	return render(request,'user_loan_creation.html',context)



@login_required
def create_user_loan(request):
	# Obtener libro
	book_id = request.POST.get('book')
	book = Libro.objects.get(id=book_id)
	# Crear préstamo con libro y el usuario actual
	new_loan = Prestamo(usuario=request.user, libro=book)
	new_loan.save()
	# Redirigir a lista de préstamos del usuario
	return redirect('user_loans')
