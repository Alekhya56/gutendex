"""Models for the authors application."""
from django.db import models

class Authors(models.Model):
    """Model for the authors table."""
    id = models.IntegerField(primary_key=True)
    birth_year = models.SmallIntegerField(blank=True, null=True)
    death_year = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=128,null=False)

    class Meta:
        """Meta class for Authors model."""
        managed = False
        db_table = 'books_author'
