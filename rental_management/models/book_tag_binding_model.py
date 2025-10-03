"""Book tag model dinition for rental service system."""

from django.db import models

from rental_management.models.book_model import Book
from rental_management.models.tag_model import Tag


class BookTagBinding(models.Model):
    """Model for defining book tag entity."""

    book_tag_binding_id = models.AutoField(primary_key=True)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
