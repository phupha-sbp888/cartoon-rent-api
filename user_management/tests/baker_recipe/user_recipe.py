"""Recipe for mocking admin and normal user."""

from model_bakery.recipe import Recipe

from user_management.models.user_model import User

admin_user_recipe = Recipe(User, is_admin=True)
normal_user_recipe = Recipe(User, is_admin=False)
normal_user_recipe_2 = Recipe(User, is_admin=False)
