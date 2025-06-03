# books/views.py

from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.db.models import Q, Prefetch
from rest_framework.pagination import PageNumberPagination
from .models import Books
from .serializers import BookSerializer


class StandardResultsSetPagination(PageNumberPagination):
    """
    Custom pagination class for the BookListAPIView.
    
    This class extends the PageNumberPagination class to provide custom pagination
    behavior for the BookListAPIView. It allows for setting a default page size and
    a maximum page size.
    """
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

class BookListAPIView(ListAPIView):
    serializer_class = BookSerializer
    pagination_class = StandardResultsSetPagination
    
    def _filter_by_book_ids(self, queryset, book_id_params):
        """
        Filter the queryset by book IDs.
        
        Args:
            queryset: The base queryset of Books objects
            book_id_params: A comma-separated string of book IDs
        
        Returns:
            A filtered queryset of Books objects
        
        Raises:
            ValidationError: If invalid book_id format is provided
        """
        try:
            book_ids = [int(id.strip()) for id in book_id_params.split(',')]
            return queryset.filter(id__in=book_ids)
        except ValueError:
            raise ValidationError("Invalid book_id format. Please provide valid integer IDs.") 

    def _filter_by_language(self, queryset, language_param):
        """
        Filter the queryset by language codes.
        
        Args:
            queryset: The base queryset of Books objects
            language_param: A comma-separated string of language codes
        
        Returns:
            A filtered queryset of Books objects
        
        """
        if not language_param:
            return queryset
        language_codes = [code.strip() for code in language_param.split(',')]
        return queryset.filter(languages__code__in=language_codes)

    def _filter_by_mime_type(self, queryset, mime_type_param):
        """
        Filter the queryset by MIME types.
        
        Args:
            queryset: The base queryset of Books objects
            mime_type_param: A comma-separated string of MIME types
        
        Returns:
            A filtered queryset of Books objects
        
        """
        if not mime_type_param:
            return queryset
        mime_types = [t.strip() for t in mime_type_param.split(',')]
        return queryset.filter(formats__mime_type__in=mime_types).distinct()

    def _filter_by_topic(self, queryset, topic_params):
        """
        Filter the queryset by topics.
        
        Args:
            queryset: The base queryset of Books objects
            topic_params: A comma-separated string of topics
        
        Returns:
            A filtered queryset of Books objects
        
        """
        if not topic_params:
            return queryset
        topics = [t.strip() for t in topic_params.split(',')]
        topic_filter = Q()
        for topic in topics:
            topic_filter |= Q(subjects__name__icontains=topic)
            topic_filter |= Q(bookshelves__name__icontains=topic)
        return queryset.filter(topic_filter).distinct()

    def _filter_by_author(self, queryset, author_params):
        """
        Filter the queryset by author names.
        
        Args:
            queryset: The base queryset of Books objects
            author_params: A comma-separated string of author names 
        
        Returns:
            A filtered queryset of Books objects
        
        """
        if not author_params:
            return queryset
        author_names = [name.strip() for name in author_params.split(',')]
        author_filter = Q()
        for author in author_names:
            author_filter |= Q(authors__name__icontains=author)
        return queryset.filter(author_filter).distinct()

    def _filter_by_title(self, queryset, title_params):
        """
        Filter the queryset by title.
        
        Args:
            queryset: The base queryset of Books objects
                title_params: A comma-separated string of titles
        
        Returns:
            A filtered queryset of Books objects
        
        """
        if not title_params:
            return queryset
        titles = [t.strip() for t in title_params.split(',')]
        title_filter = Q()
        for title in titles:
            title_filter |= Q(title__icontains=title)
        return queryset.filter(title_filter).distinct()

    def get_queryset(self):
        """
        Get the queryset of books with filtering and pagination.
        
        Returns a queryset of Books objects, filtered based on URL query parameters:
        - book_id: Comma-separated list of book IDs
        - language: Comma-separated list of language codes
        - mime_type: Comma-separated list of mime types
        - topic: Comma-separated list of topics to search in subjects and bookshelves
        - author: Comma-separated list of author names to search
        - title: Comma-separated list of titles to search
        - page_size: Number of results per page (default 25, max 100)
        - page: Page number for pagination
        
        Raises:
            ValidationError: If invalid query parameters are provided
        """

        try:
            
            request = self.request
            ALLOWED_QUERY_PARAMS = {'book_id', 'language', 'mime_type', 'topic', 'author', 'title', 'page_size', 'page'}
            # Validate query parameters

            if invalid_params := set(request.GET.keys()) - ALLOWED_QUERY_PARAMS:
                raise ValidationError(detail=f"Invalid filter parameter(s): {', '.join(invalid_params)}. Choose from {', '.join(ALLOWED_QUERY_PARAMS)}")

            queryset = Books.objects.all().order_by('-download_count')
            queryset = queryset.prefetch_related(
            'authors', 'subjects', 'bookshelves', 'formats', 'languages'
        )
            # Apply filters
            if request.GET.get('book_id'):
                queryset = self._filter_by_book_ids(queryset, request.GET.get('book_id'))
            queryset = self._filter_by_language(queryset, request.GET.get('language'))
            queryset = self._filter_by_mime_type(queryset, request.GET.get('mime_type'))
            queryset = self._filter_by_topic(queryset, request.GET.get('topic'))
            queryset = self._filter_by_author(queryset, request.GET.get('author'))
            queryset = self._filter_by_title(queryset, request.GET.get('title'))
            return queryset.distinct()
        except Exception as e:
            raise ValidationError(detail=f"error: {str(e)}. ")
        
