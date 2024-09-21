from django.contrib import admin
from django.urls import path
from .views import BookViewSet, UserViewSet

urlpatterns = [
    path('books/', BookViewSet.as_view({
        'get': 'list',
    }), name='books-list'),
    path('books/<int:pk>/', BookViewSet.as_view({
        'get': 'retrieve',
    }), name='book-detail'),
    path('users/', UserViewSet.as_view({
        'post': 'create',
    }),name='user-new'),
    path('books/<int:pk>/borrow/', BookViewSet.as_view({
        'post': 'borrow',
    }),name='book-borrow'),
    path('books/filter/', BookViewSet.as_view({
        'get': 'filter',
    }), name='book-filter'),
]
