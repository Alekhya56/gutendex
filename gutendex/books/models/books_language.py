from django.db import models

class BooksLanguage(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(unique=True, max_length=4)

    class Meta:
        managed = False
        db_table = 'books_language'

