"""Status type for keep track of book availability."""

from django.db import models


class BookStatusType(models.TextChoices):
    """Enumeration for book status types."""

    AVAILABLE = 'AVAILABLE'
    RENTED = 'RENTED'
    OUT_OF_SERVICE = 'OUT_OF_SERVICE'
