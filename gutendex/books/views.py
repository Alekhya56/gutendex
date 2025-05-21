# books/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Books
from .serializers import BookSerializer

class BookListAPIView(APIView):
    def get(self, request):
        """Handle GET request to list books with optional filtering and pagination."""
        queryset = Books.objects.all().order_by('-download_count')
        
        # --- Filtering ---
        book_id_params = request.GET.get('book_id')
        if book_id_params:
            book_ids = [int(id.strip()) for id in book_id_params.split(',')]
            queryset = queryset.filter(id__in=book_ids)

        language_param = self.request.GET.get('language')
        if language_param:
            language_codes = [code.strip() for code in language_param.split(',')]
            queryset = queryset.filter(languages__code__in=language_codes)

        mime_type_param = request.GET.get('mime_type')
        if mime_type_param:
            mime_types = [t.strip() for t in mime_type_param.split(',')]
            queryset = queryset.filter(formats__mime_type__in=mime_types).distinct()

        topic_params = request.GET.get('topic')
        if topic_params:
            topics = [t.strip() for t in topic_params.split(',')]
            topic_filter = Q()
            for topic in topics:
                topic_filter |= Q(subjects__name__icontains=topic)
                topic_filter |= Q(bookshelves__name__icontains=topic)
            queryset = queryset.filter(topic_filter).distinct()

        author_params = request.GET.get('author')
        if author_params:
            author_names = [name.strip() for name in author_params.split(',')]
            author_filter = Q()
            for author in author_names:
                author_filter |= Q(authors__name__icontains=author)
            queryset = queryset.filter(author_filter).distinct()

        title_params = request.GET.get('title')
        if title_params:
            titles = [t.strip() for t in title_params.split(',')]
            title_filter = Q()
            for title in titles:
                title_filter |= Q(title__icontains=title)
            queryset = queryset.filter(title_filter).distinct()

        # --- Pagination ---
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
