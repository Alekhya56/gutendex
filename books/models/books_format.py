from django.db import models
from .books import Books

class BooksFormat(models.Model):
    id = models.IntegerField(primary_key=True)
    mime_type = models.CharField(max_length=32, null= False)
    url = models.CharField(max_length=256, null= False)
    book = models.ForeignKey(Books, models.CASCADE,related_name='formats')

    class Meta:
        managed = False
        db_table = 'books_format'

