from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Book, NewUser
from .serializers import BookSerializer, UserSerializer
from .producer import publish


class BookViewSet(viewsets.ViewSet):
    def list(self, request):  # books that are unavailable and their available dates
        unavailable_books = Book.objects.filter(is_available=False)
        result = []
        for book in unavailable_books:
            result.append({
                'id': book.id,
                'title': book.title,
                'available_date': book.available_date,
            })
        return Response(result)

    def create(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('book created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        book = Book.objects.get(id=pk)
        book.delete()
        publish('book_deleted', pk)
        return Response(status=status.HTTP_200_OK)

    def borrowed_books(self, request):  # List users and the books they’ve borrowed
        borrowed_books = Book.objects.filter(is_available=False)
        user_books = {}
        for book in borrowed_books:
            if book.user in user_books:
                user_books[book.user].append(book.title)
            else:
                user_books[book.user] = [book.title]

        result = [{"user": user, "books": books} for user, books in user_books.items()]

        return Response(result, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        users = NewUser.objects.all()  # borrowed_books books
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
