"""Status type for keep track of rent history availability."""

from django.db import models


class RentStatusType(models.TextChoices):
    """Enumeration for rent status types."""

    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    OVERDUE = 'OVERDUE'
