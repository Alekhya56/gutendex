from django.db import models
from .books import Books

class BookSubjects(models.Model):
    id = models.IntegerField(primary_key=True)
    book = models.ForeignKey(Books, models.CASCADE)
    subject = models.ForeignKey('BooksSubject', models.CASCADE)

    class Meta:
        managed = False
        db_table = 'books_book_subjects'
        unique_together = (('book', 'subject'),)
