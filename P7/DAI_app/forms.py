from django import forms
from .models import Autor, Libro, Prestamo


"""
	Formularios de los modelos
"""

class AuthorForm(forms.ModelForm):
	class Meta:
		model = Autor
		fields = ['nombre', 'fecha_nacimiento']
		labels = {
			'nombre': 'Nombre completo del autor',
			'fecha_nacimiento': 'Fecha de nacimiento del autor'
		}
		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control'}),
			'fecha_nacimiento': forms.DateInput(format=('%d-%m-%Y'), attrs={'class':'form-control'})
		}


class BookForm(forms.ModelForm):
	class Meta:
		model = Libro
		fields = ['titulo', 'publicacion', 'autores']
		labels = {
			'titulo': 'Título del libro',
			'publicacion': 'Año de publicación'
		}
		widgets = {
			'titulo': forms.TextInput(attrs={'class':'form-control'}),
			'publicacion': forms.NumberInput(attrs={'class':'form-control'})#,
			#'autores': forms.ModelChoiceIterator(field='autores', attrs={'class':'form-control'})
		}



class LoanForm(forms.ModelForm):
	class Meta:
		model = Prestamo
		fields = ['usuario','libro']
		labels = {
			'usuario': 'Usuario',
			'libro': 'Libro prestado'
		}
		widgets = {
			'usuario': forms.TextInput(attrs={'class':'form-control'}),
		}


class LoanAuthorChoiceForm(forms.Form):
	book = forms.ModelChoiceField(queryset=Libro.objects.all(), label="Libro")

"""
	Formularios para búsquedas
"""


class AuthorSearchForm():
    author_name = forms.CharField(required=False)


class BookSearchForm():
	book_name = forms.CharField(required=False)


"""


class LoanForm(forms.ModelForm):
	libro   = forms.ForeignKey(Libro, on_delete=models.CASCADE)
	fecha   = forms.DateField(default=timezone.now)
	usuario = forms.CharField(max_length=100)
"""
