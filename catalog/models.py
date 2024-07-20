from django.db import models
from django.urls import reverse # Utilizado para generar URLs invirtiendo los patrones de URL
import uuid

# Create your models here.
class Genre(models.Model):
    name = models.CharField(
        max_length=200, 
        help_text='Ingrese el nombre del género (p. ej. Ciencia Ficción, Terror, etc)'
    )
    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    title = models.CharField(
        max_length=200
    )
    author = models.ForeignKey(
        'Author', # Es un string, en vez de un objeto, porque la clase Author aún no ha sido declarada.
        on_delete=models.SET_NULL, # Pondrá en null el campo si el registro del autor relacionado
        null=True
    )
    sumary = models.TextField(
        max_length=1000,
        help_text='Ingrese una breve descripción del libro'
    )
    isbn = models.CharField(
        'IBSN',
        max_length=13,
        help_text='13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'
    )
    genre = models.ManyToManyField(
        Genre,
        help_text = 'Seleccione un género para este libro'
    )
    language = models.ForeignKey(
        'Language',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        # Devuelve el URL a una instancia particular de Book
        return reverse('book-detail', args=[str(self.id)])

'''
El método get_absoulte_url() devuelve un URL que puede ser usado para acceder al 
detalle de un registro particular (para que esto funcione, debemos definir un mapeo
de URL que tenga el nombre book-detail y una vista y una plantilla asociadas a él)
'''


class BookInstance(models.Model):
# Representa una copia específica de un libro que alguien pueda pedir prestado
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        help_text='ID único para este libro particular en toda la biblioteca'
    )
    book = models.ForeignKey(
        'Book', on_delete=models.SET_NULL,
        null=True
    )
    imprint = models.CharField(
        max_length=200
    )
    due_back = models.DateField(
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=1,
        blank=True,
        default='m',
        help_text = 'Disponibilidad del libro'
    )

    class Meta:
        ordering = ['due_back']
    
    def __str__(self):
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    first_name = models.CharField(
        max_length=100
    )
    last_name = models.CharField(
        max_length=100
    )
    date_of_birth = models.DateField(
        null=True, 
        blank=True
    )
    date_of_death = models.DateField(
        'Died', 
        null=True, 
        blank=True
    )

    def get_absolute_url(self):
        # Retorna la url para acceder a una instancia particular de un autor.
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Language(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='Ingrese un lenguaje'
    )
    def __str__(self) -> str:
        return self.name
