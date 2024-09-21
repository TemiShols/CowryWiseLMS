from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer, UserSerializer
from .producer import publish


class BookViewSet(viewsets.ViewSet):
    def filter(self, request):
        # Get query parameters
        publisher = request.query_params.get('publisher', None)
        category = request.query_params.get('category', None)
        books = Book.objects.all()

        # Filter by publisher if provided
        if publisher:
            books = books.filter(publisher__iexact=publisher)

        # Filter by category if provided
        if category:
            books = books.filter(category__iexact=category)

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def list(self, request):
        books = Book.objects.filter(is_available=True)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        book = Book.objects.get(id=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def borrow(self, request, pk=None):
        book = Book.objects.get(pk=pk)
        book.is_available = False
        book.save()
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('new user created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

