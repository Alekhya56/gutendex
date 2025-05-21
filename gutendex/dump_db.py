# dumpdata_utf8.py
import io
import os
import django
# Set the settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gutendex.settings")  # Replace 'gutendex' if your settings module is named differently

# Setup Django
django.setup()
from django.core.management import call_command

with io.open('db2.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', 'books.BookAuthors', 'books.BookLanguages', 'books.Bookshelves', 'books.BookSubjects', stdout=f, indent=2)

