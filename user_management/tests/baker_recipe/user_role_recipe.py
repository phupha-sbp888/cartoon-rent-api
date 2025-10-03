"""Recipe for mocking user role test data."""

from model_bakery.recipe import Recipe

from user_management.models.user_role_model import UserRole

manager_role_recipe = Recipe(UserRole, name="Manager", description="Store manager role.")
client_role_recipe = Recipe(UserRole, name="Client", description="Client")
