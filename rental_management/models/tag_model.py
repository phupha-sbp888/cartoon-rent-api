"""Tag model fir categorizing books in rental service system."""

from django.db import models

from user_management.models.user_model import User


class Tag(models.Model):
    """Model for defining tags for books."""

    tag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, unique=True, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        """Set up default ordering on query tag model."""

        ordering = ["-created_date"]
