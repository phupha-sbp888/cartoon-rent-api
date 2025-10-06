"""Recipe for mocking tag."""

from model_bakery.recipe import Recipe

from rental_management.models.tag_model import Tag

tag_1_recipe = Recipe(Tag, name="Education")
tag_2_recipe = Recipe(Tag, name="Comedy")
