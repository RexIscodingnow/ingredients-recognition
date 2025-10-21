"""
[Schema] recipes_ingredients
  Table: ingredients
         Columns: ingredient_id, ingredient_name

  Table: recipe_ratings
         Columns: rating, recipe_id, user_id

  Table: recipeingredients
         Columns: ingredient_id, recipe_id

  Table: recipes
         Columns: cooking_step, recipe_id, recipe_info_url, recipe_name

  Table: users
         Columns: email, password, user_id, username
"""

class RecipeIngredients:
    """
    The intermediary table for Ingredients and Recipes
    """
    def __init__(self, recipe_id, ingredient_id):
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id


class RecipeRatings:
    """
    The intermediary table for Users and Recipes.
    In order for the recommendation system to retrieve the rating score of a recipe
    based on users' relative preferences.
    """
    def __init__(self, rating, user_id, recipe_id):
        self.rating = rating
        self.user_id = user_id
        self.recipe_id = recipe_id


class Recipe:
    def __init__(self, recipe_id, recipe_name, cooking_step, recipe_info_url):
        self.recipe_id = recipe_id
        self.recipe_name = recipe_name
        self.cooking_step = cooking_step
        self.recipe_info_url = recipe_info_url


class Ingredient:
    def __init__(self, ingredient_id, ingredient_name):
        self.ingredient_id = ingredient_id
        self.ingredient_name = ingredient_name


