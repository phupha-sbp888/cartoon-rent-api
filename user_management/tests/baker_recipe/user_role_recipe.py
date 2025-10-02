"""Recipe for mocking user role test data."""

from model_bakery.recipe import Recipe

from user_management.models.user_role_model import UserRole

user_role_recipe = Recipe(UserRole, name="Manager", description="Store manager role.")
