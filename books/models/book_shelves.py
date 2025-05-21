"""Models for the book shelves relationship application."""
from django.db import models
from .books import Books

class Bookshelves(models.Model):
    """Model for the book shelves relationship table."""
    id = models.IntegerField(primary_key=True)
    book = models.ForeignKey(Books, models.CASCADE, related_name='book_bookshelves')
    bookshelf = models.ForeignKey('Bookshelf', models.CASCADE)

    class Meta:
        """Meta class for Bookshelves model."""
        managed = False
        db_table = 'books_book_bookshelves'
        unique_together = (('book', 'bookshelf'),)
