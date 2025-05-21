# books/admin.py
from django.contrib import admin
from .models.books import Books
from .models.authors import Authors
from .models.book_authors import BookAuthors
from .models.book_shelf import Bookshelf
from .models.book_shelves import Bookshelves
from .models.books_language import BooksLanguage
from .models.book_languages import BookLanguages
from .models.books_subject import BooksSubject
from .models.book_subjects import BookSubjects
from .models.books_format import BooksFormat


admin.site.register(Books)
admin.site.register(Authors)
admin.site.register(Bookshelf)
admin.site.register(BooksLanguage)
admin.site.register(BookLanguages)
admin.site.register(BookSubjects)
admin.site.register(BooksFormat)
admin.site.register(BookAuthors)
admin.site.register(Bookshelves)    
admin.site.register(BooksSubject)

# Register your models here.
