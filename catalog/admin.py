from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

# Register your models here.
admin.site.register(Genre)
admin.site.register(Language)

class BookInline(admin.TabularInline):
    # lista encadenada para ver las libros
    model = Book
    extra = 0



class AuthorAdmin(admin.ModelAdmin):
    # fields lista solo los campos que se van a desplegar en el formulario, en orden
    # Se desplegarán en horizontal si los agrupas en una tupla
    # exclude =  ['first_name']
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')] 
    inlines = [BookInline] # Lista encadenada

admin.site.register(Author, AuthorAdmin)



class BooksInstanceInline(admin.TabularInline):
    #lista encadenada para ver BookInstance
    model = BookInstance
    extra = 0



@admin.register(Book) 
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline] # Lista encadenada




@admin.register(BookInstance)
class BookInstance(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back')
    list_filter = ('status', 'due_back')
    # Configurando secciones en admin
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )

'''
La expresión @register para registrar los modelos ( hace exactamente lo mismo que admin.site.register() )
'''