from django.db import models
from django.utils import timezone
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

class Autor(models.Model):
	nombre = models.CharField(max_length=100)
	fecha_nacimiento = models.DateField()

	def __str__(self):
		return self.nombre


class Libro(models.Model):
	titulo = models.CharField(max_length=200)
	publicacion = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(1), max_value_current_year])
	autores = models.ManyToManyField(Autor)

	def __str__(self):
		return self.titulo


class Prestamo(models.Model):
	libro   = models.ForeignKey(Libro, on_delete=models.CASCADE)
	fecha   = models.DateField(default=timezone.now)
	usuario = models.CharField(max_length=100)

	def __str__(self):
		return self.usuario + ' -> ' + libro
