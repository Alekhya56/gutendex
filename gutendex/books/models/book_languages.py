"""Models for the book languages application."""
from django.db import models
from .books import Books

class BookLanguages(models.Model):
    """Model for the book languages relationship table."""
    id = models.IntegerField(primary_key=True)
    book = models.ForeignKey('Books', models.CASCADE)
    language = models.ForeignKey('BooksLanguage', models.CASCADE)

    class Meta:
        """Meta class for BookLanguages model."""
        managed = False
        db_table = 'books_book_languages'
        unique_together = (('book', 'language'),)