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
                                         publisher='Publisher A', category='Fiction', available_date='2013-01-29')
        self.book2 = Book.objects.create(title='Book 2', is_available=True, user='Adekunle', author='Author 1',
                                         publisher='Publisher B', category='Fiction', available_date='2013-01-29')

    def test_filter_books(self):
        url = reverse('book-filter')
        response = self.client.get(url, {'publisher': 'Publisher A', 'category': 'Fiction'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book 1')

    def test_list_books(self):
        url = reverse('books-list')
        response = self.client.get(url)
        books = Book.objects.filter(is_available=True)
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_book(self):
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Book 1')

    def test_borrow_book(self):
        url = reverse('book-borrow', kwargs={'pk': self.book1.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        updated_book = Book.objects.get(pk=self.book1.pk)
        self.assertFalse(updated_book.is_available)


class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        url = reverse('user-new')
        data = {'username': 'Temi', 'email': 'temi@cowrytest.com', 'password': 'testpass123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NewUser.objects.count(), 1)
        self.assertEqual(NewUser.objects.get().username, 'Temi')
