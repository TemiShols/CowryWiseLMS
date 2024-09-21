import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Book, NewUser
from .serializers import BookSerializer, UserSerializer


class BookViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = NewUser.objects.create(username='testuser', email='test@cowrytest.com')
        self.book1 = Book.objects.create(title='Book 1', is_available=False, user=self.user.username, author='Author 1',
                                         publisher='Publisher 1', category='Category 1', available_date='2013-01-29')
        self.book2 = Book.objects.create(title='Book 2', is_available=True, user='Adekunle', author='Author 1',
                                         publisher='Publisher 1', category='Category 1', available_date='2013-01-29')

    def test_list_unavailable_books(self):
        url = reverse('books-unavailable')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        books = Book.objects.filter(is_available=False)
        result = [
            {
                'id': book.id,
                'title': book.title,
                'available_date': book.available_date,
            }
            for book in books
        ]
        self.assertEqual(response.data, result)

    def test_create_book(self):
        url = reverse('book-new')
        data = {
            'title': 'New Book',
            'author': 'John Boswick',
            'publisher': 'Test Publisher',
            'category': 'Test Category',
            'user': 'Drogba',
            'available_date': '2013-01-29'
        }
        response = self.client.post(url, data)
        serializer = BookSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

        created_book = Book.objects.last()
        created_serializer = BookSerializer(created_book)
        self.assertEqual(response.data, created_serializer.data)

    def test_delete_book(self):
        url = reverse('book-delete', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.count(), 1)

    def test_borrowed_books(self):
        url = reverse('books-borrowed')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = [{'user': self.user.username, 'books': ['Book 1']}]
        self.assertEqual(response.data, expected_data)


class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = NewUser.objects.create(username='user1', email='user1@cowrytest.com')
        self.user2 = NewUser.objects.create(username='user2', email='user2@cowrytest.com')

    def test_list_users(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        users = NewUser.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
