from django.contrib import admin
from django.urls import path
from .views import BookViewSet, UserViewSet

urlpatterns = [
    path('books/', BookViewSet.as_view({
        # 'get': 'list',
        'post': 'create'
    }), name='book-new'),
    path('books/<int:pk>/', BookViewSet.as_view({
        'delete':'destroy'
    }),name='book-delete'),
    path('users/', UserViewSet.as_view({
        'get': 'list',
    }),name='user-list'),
    path('borrowed_books/', BookViewSet.as_view({
        'get': 'borrowed_books',
    }),name='books-borrowed'),
    path('unavailable_books/', BookViewSet.as_view({
        'get': 'list',
    }),name='books-unavailable'),
]
