# books/serializers.py
from rest_framework import serializers
from .models import Books, Authors, Bookshelf, BooksSubject, BooksLanguage

class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for the Authors model."""
    class Meta:
        """Meta class for AuthorSerializer."""
        model = Authors
        fields = ['name', 'birth_year', 'death_year']

class SubjectSerializer(serializers.ModelSerializer):
    """Serializer for the BooksSubject model."""
    class Meta:
        """Meta class for SubjectSerializer."""
        model = BooksSubject
        fields = ['name']

class BookshelfSerializer(serializers.ModelSerializer):
    """Serializer for the Bookshelf model."""
    class Meta:
        """Meta class for BookshelfSerializer."""
        model = Bookshelf
        fields = ['name']
        
class LanguageSerializer(serializers.ModelSerializer):
    """Serializer for the BooksLanguage model."""
    class Meta:
        """Meta class for LanguageSerializer."""
        model = BooksLanguage
        fields = ['code']
from .models import BooksFormat
class FormatSerializer(serializers.ModelSerializer):
    """Serializer for the BooksFormat model."""
    class Meta:
        """Meta class for FormatSerializer."""
        model = BooksFormat
        fields = ['mime_type', 'url']

class BookSerializer(serializers.ModelSerializer):
    """Serializer for the Books model."""
    authors = AuthorSerializer(many=True, read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)
    bookshelves = BookshelfSerializer(many=True, read_only=True)
    formats = FormatSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)

    class Meta:
        """Meta class for BookSerializer."""
        model = Books
        fields = [
            'id', 'title', 'languages', 'download_count',
            'authors', 'subjects', 'bookshelves', 'formats'
        ]
