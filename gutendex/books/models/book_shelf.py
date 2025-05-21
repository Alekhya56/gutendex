"""Models for the book shelves application."""
from django.db import models

class Bookshelf(models.Model):
    """Model for the book shelves table."""
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=64)

    class Meta:
        """Meta class for Bookshelf model."""
        managed = False
        db_table = 'books_bookshelf'
