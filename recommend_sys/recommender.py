# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# import torch.optim as optim


# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


import access_db
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity


cursor = access_db.cursor

recipes = access_db.select(cursor, tablename="Recipes")
ingredients = access_db.select(cursor, tablename="Ingredients")
recipes_ingreds = access_db.select(cursor, tablename="RecipeIngredients")    
recipe_ratings = access_db.select(cursor, tablename="recipe_ratings")

df_DB_R = pd.DataFrame(recipes, columns=["recipe_id", "recipe_name", "recipe_info_url", "cooking_step"])
df_DB_I = pd.DataFrame(ingredients, columns=["ingredient_id", "ingredient_name"])
df_DB_RI = pd.DataFrame(recipes_ingreds, columns=["recipe_id", "ingredient_id"])
df_DB_RRatings = pd.DataFrame(recipe_ratings, columns=["user_id", "recipe_id", "rating"])


def create_X(df: pd.DataFrame):
    """Generates a sparse matrix from ratings dataframe.

    Returns:
        X: a sparse matrix
        id_row_mapper: dict that maps row id's to row indices
        id_col_mapper: dict that maps column id's to column indices
        idx_row_mapper: dict that maps row indices to row id's
        idx_col_mapper: dict that maps column indices to column id's
    """
    row = "user_id"
    column = "recipe_id"
    M = df[row].nunique()
    N = df[column].nunique()

    id_row_mapper = dict(zip(np.unique(df[row]), list(range(M))))       # (row) id --> index
    id_col_mapper = dict(zip(np.unique(df[column]), list(range(N))))    # (column)
    idx_row_mapper = dict(zip(list(range(M)), np.unique(df[row])))      # (row) index --> id
    idx_col_mapper = dict(zip(list(range(N)), np.unique(df[column])))   # (column)

    row_indices = [id_row_mapper[i] for i in df[row]]
    col_indices = [id_col_mapper[i] for i in df[column]]
    X = csr_matrix((df["rating"], (row_indices, col_indices)), shape=(M, N))
    return X, id_row_mapper, id_col_mapper, idx_row_mapper, idx_col_mapper


# one-hot encoding
# df_onehot_RI = pd.crosstab(
#                     index=df_DB_RI['recipe_id'],        # row
#                     columns=df_DB_RI['ingredient_id']   # column
#                 ).astype(bool).astype("int8")

#    row: user_id
# column: recipe_id
# rating_matrix = df_DB_RRatings.pivot(index="user_id", columns="recipe_id", values="rating")

# print(df_onehot_RI)
# print(df_onehot_RI.shape)
# print()
# print(rating_matrix)
# print(rating_matrix.shape)

X, id_row_mapper, id_col_mapper, idx_row_mapper, idx_col_mapper = create_X(df_DB_RRatings)

# Evaluating sparsity
n_total = X.shape[0] * X.shape[1]
n_ratings = X.nnz                       # The number of stored non-empty elements
sparsity = n_ratings / n_total

print(f"Size of user-item matrix: {X.shape}")
print(f"         Matrix sparsity: {n_ratings} / {n_total} = {round(sparsity * 100, 2)}%")
print("\n")
print("user-item matrix:")
print(X)
print("\n")

n_ratings_per_user = X.getnnz(axis=1)
n_ratings_per_recipe = X.getnnz(axis=0)

print(f"Number of users rated: {len(n_ratings_per_user)}")
print(f"Number of recipes rated: {len(n_ratings_per_recipe)}")
print(f"Most active user rated {n_ratings_per_user.max()} recipes.")
print(f"Least active user rated {n_ratings_per_user.min()} recipes.")
print(f"Most rated recipe has {n_ratings_per_recipe.max()} ratings.")
print(f"Least rated recipe has {n_ratings_per_recipe.min()} ratings.")

plt.figure(figsize=(16,4))
plt.subplot(1,2,1)
sns.kdeplot(n_ratings_per_user, fill=True)
plt.xlim(0)
plt.title("Number of Ratings Per User", fontsize=14)
plt.xlabel("number of ratings per user")
plt.ylabel("density")

plt.subplot(1,2,2)
sns.kdeplot(n_ratings_per_recipe, fill=True)
plt.xlim(0)
plt.title("Number of Ratings Per Recipe", fontsize=14)
plt.xlabel("number of ratings per recipe")
plt.ylabel("density")


def find_similar_KNN(recipe_id: int, X: csr_matrix, recipe_idx_mapper: dict, recipe_id_mapper, k: int, metric='cosine'):
    """Finds k-nearest neighbours for a given recipe id. (Collaborative Filtering)

    Parameters
        - recipe_id: id of the recipe of interest
        - X: user-item utility matrix
        - recipe_idx_mapper: dict that maps recipe id's to recipe indices
        - recipe_id_mapper: dict that maps recipe indices to recipe id's
        - k: number of similar recipes to retrieve
        - metric: distance metric for kNN calculations

    Return: a list of k similar recipe ID's
    """
    X = X.T     # Each row vector represents a recipe with ratings from all users
    recipe_idx = recipe_idx_mapper[recipe_id]
    recipe_vec = X[recipe_idx]

    if isinstance(recipe_vec, (np.ndarray)):
        recipe_vec = recipe_vec.reshape(1, -1)

    # use k+1 since kNN output includes the `recipe_id` of interest
    kNN = NearestNeighbors(n_neighbors=(k + 1), metric=metric)
    kNN.fit(X)

    neighbor = kNN.kneighbors(recipe_vec, return_distance=False)
    neighbour_ids = [recipe_id_mapper[neighbor.item(i)] for i in range(k+1)]
    neighbour_ids.pop(0)
    return neighbour_ids


similar_recipes = find_similar_KNN(1, X, id_col_mapper, idx_col_mapper, 5)
print(similar_recipes)

plt.show()

