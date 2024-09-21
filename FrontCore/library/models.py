from django.db import models
from django.contrib.auth.models import User


class NewUser(User):

    class Meta:
        app_label = 'library'

    def __str__(self):
        return self.username


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    available_date = models.DateField(null=True, blank=True)  # When book will be available if borrowed
    user = models.CharField(max_length=55)

    class Meta:
        app_label = 'library'

    def __str__(self):
        return self.title
