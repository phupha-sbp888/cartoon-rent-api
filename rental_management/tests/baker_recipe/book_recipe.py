"""Recipe for mocking book."""

from model_bakery.recipe import Recipe

from rental_management.enums.book_status_type import BookStatusType
from rental_management.models.book_model import Book

available_book_recipe = Recipe(Book, status=BookStatusType.AVAILABLE.value)
rented_book_recipe = Recipe(Book, status=BookStatusType.RENTED.value)
out_of_service_book_recipe = Recipe(Book, status=BookStatusType.OUT_OF_SERVICE.value)
