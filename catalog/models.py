from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name='books')
    total_quantity = models.PositiveIntegerField(default=0)
    available_quantity = models.PositiveIntegerField(default=0)
    room_no = models.CharField(max_length=50)
    shelf_no = models.CharField(max_length=50)
    row = models.CharField(max_length=50)
    column = models.CharField(max_length=50)

    def __str__(self):
        return self.name
