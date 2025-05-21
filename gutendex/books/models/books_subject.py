from django.db import models

class BooksSubject(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256, null=False)

    class Meta:
        managed = False
        db_table = 'books_subject'
