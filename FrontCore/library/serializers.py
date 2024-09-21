from rest_framework import serializers
from .models import Book, NewUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'