from django.db import models
from .authors import Authors
from .books import Books

class BookAuthors(models.Model):
    book = models.ForeignKey(Books, models.CASCADE)
    author = models.ForeignKey(Authors, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'books_book_authors'
        unique_together = (('book', 'author'),)
