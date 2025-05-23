# books/views.py

from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Books
from .serializers import BookSerializer


class BookListAPIView(APIView):
    def _filter_by_book_ids(self, queryset, book_id_params):
        try:
            book_ids = [int(id.strip()) for id in book_id_params.split(',')]
            return queryset.filter(id__in=book_ids)
        except ValueError:
            raise ValidationError("Invalid book_id format. Please provide valid integer IDs.") 

    def _filter_by_language(self, queryset, language_param):
        if not language_param:
            return queryset
        language_codes = [code.strip() for code in language_param.split(',')]
        return queryset.filter(languages__code__in=language_codes)

    def _filter_by_mime_type(self, queryset, mime_type_param):
        if not mime_type_param:
            return queryset
        mime_types = [t.strip() for t in mime_type_param.split(',')]
        return queryset.filter(formats__mime_type__in=mime_types).distinct()

    def _filter_by_topic(self, queryset, topic_params):
        if not topic_params:
            return queryset
        topics = [t.strip() for t in topic_params.split(',')]
        topic_filter = Q()
        for topic in topics:
            topic_filter |= Q(subjects__name__icontains=topic)
            topic_filter |= Q(bookshelves__name__icontains=topic)
        return queryset.filter(topic_filter).distinct()

    def _filter_by_author(self, queryset, author_params):
        if not author_params:
            return queryset
        author_names = [name.strip() for name in author_params.split(',')]
        author_filter = Q()
        for author in author_names:
            author_filter |= Q(authors__name__icontains=author)
        return queryset.filter(author_filter).distinct()

    def _filter_by_title(self, queryset, title_params):
        if not title_params:
            return queryset
        titles = [t.strip() for t in title_params.split(',')]
        title_filter = Q()
        for title in titles:
            title_filter |= Q(title__icontains=title)
        return queryset.filter(title_filter).distinct()

    def get(self, request):
        """Handle GET request to list books with optional filtering and pagination."""
        try:
            ALLOWED_QUERY_PARAMS = {'book_id', 'language', 'mime_type', 'topic', 'author', 'title', 'page'}
            # Validate query parameters
            if invalid_params := set(request.GET.keys()) - ALLOWED_QUERY_PARAMS:
                raise ValidationError(detail=f"Invalid filter parameter(s): {', '.join(invalid_params)}. Choose from {', '.join(ALLOWED_QUERY_PARAMS)}")

            queryset = Books.objects.all().order_by('-download_count')
            
            # Apply filters
            if request.GET.get('book_id'):
                queryset = self._filter_by_book_ids(queryset, request.GET.get('book_id'))
            queryset = self._filter_by_language(queryset, request.GET.get('language'))
            queryset = self._filter_by_mime_type(queryset, request.GET.get('mime_type'))
            queryset = self._filter_by_topic(queryset, request.GET.get('topic'))
            queryset = self._filter_by_author(queryset, request.GET.get('author'))
            queryset = self._filter_by_title(queryset, request.GET.get('title'))

            # Pagination
            total = queryset.count()
            page = int(request.GET.get('page', 1))
            page_size = 25
            start = (page - 1) * page_size
            end = start + page_size

            books = queryset[start:end]
            serializer = BookSerializer(books, many=True)

            return Response({
                'total': total,
                'results': serializer.data
            })
        except ValidationError as ve:
            return Response({"error": str(ve)}, status=400)
        except Exception as e:
            return Response({"error": f"Internal server error: {str(e)}"}, status=500)

