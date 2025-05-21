"""Models for the books application."""
from django.db import models
from .books_language import BooksLanguage
from .books_subject import BooksSubject
from .authors import Authors
from .book_shelf import Bookshelf


class Books(models.Model):
    """Model for the books table."""
    id = models.IntegerField(primary_key=True)
    download_count = models.IntegerField(blank=True, null=True)
    gutenberg_id = models.IntegerField(unique=True, null = False)
    media_type = models.CharField(max_length=16, null = False)
    title = models.CharField(max_length=1024, blank=True, null=True)

    authors = models.ManyToManyField('Authors', through='BookAuthors', related_name='books')
    languages = models.ManyToManyField('BooksLanguage', through='BookLanguages', related_name='books')
    subjects = models.ManyToManyField('BooksSubject', through='BookSubjects', related_name='books')
    bookshelves = models.ManyToManyField('BookShelf', through='BookShelves', related_name='books')
    # formats = models.ManyToManyField('BooksFormat', related_name='books')

    class Meta:
        """Meta class for Books model."""
        managed = False
        db_table = 'books_book'
