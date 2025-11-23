import access_db
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
# from sklearn.metrics.pairwise import cosine_similarity
# from cache_radis import RedisClient


# redis_client = RedisClient.get_instance()
cursor = access_db.cursor

"""
#TODO: Cache data structure

user_id: from current_user.id

{
    "recipe_id": id, "score": similarity_score
}

"""


def create_userItem_matrix(df: pd.DataFrame):
    """Generates a sparse matrix from ratings dataframe.

    Returns
        - X: a sparse matrix
        - idx_row_mapper: dict that maps row id's to row indices
        - idx_col_mapper: dict that maps column id's to column indices
        - id_row_mapper: dict that maps row indices to row id's
        - id_col_mapper: dict that maps column indices to column id's
    """
    row = "user_id"
    column = "recipe_id"
    M = df[row].nunique()
    N = df[column].nunique()

    idx_row_mapper = dict(zip(np.unique(df[row]), list(range(M))))      # (row) id --> index
    idx_col_mapper = dict(zip(np.unique(df[column]), list(range(N))))   # (column)
    id_row_mapper = dict(zip(list(range(M)), np.unique(df[row])))       # (row) index --> id
    id_col_mapper = dict(zip(list(range(N)), np.unique(df[column])))    # (column)

    row_indices = [idx_row_mapper[id] for id in df[row]]
    col_indices = [idx_col_mapper[id] for id in df[column]]
    X = csr_matrix((df["rating"], (row_indices, col_indices)), shape=(M, N))
    return X, idx_row_mapper, idx_col_mapper, id_row_mapper, id_col_mapper


def create_itemItem_matrix(df_RI: pd.DataFrame):
    """Generates a sparse matrix from item-item dataframe

    Args:
        df_RI: tablename = "RecipeIngredients"

    Returns:
        X: a sparse matrix
        idx_row_mapper: dict that maps row id's to row indices
        idx_col_mapper: dict that maps column id's to column indices
        id_row_mapper: dict that maps row indices to row id's
        id_col_mapper: dict that maps column indices to column id's
    """
    unique_recipes = df_RI["recipe_id"].unique()
    unique_ingredients = df_RI["ingredient_id"].unique()
    M = len(unique_recipes)
    N = len(unique_ingredients)

    idx_row_mapper = dict(zip(unique_recipes, list(range(M))))        # (row) id --> index
    idx_col_mapper = dict(zip(unique_ingredients, list(range(N))))    # (column)
    id_row_mapper = dict(zip(list(range(M)), unique_recipes))         # (row) index --> id
    id_col_mapper = dict(zip(list(range(N)), unique_ingredients))     # (column)

    row_indices = df_RI["recipe_id"].map(idx_row_mapper)
    col_indices = df_RI["ingredient_id"].map(idx_col_mapper)
    data = np.ones(len(df_RI))  # one-hot encoding

    matrix = csr_matrix((data, (row_indices, col_indices)), shape=(M, N))

    return matrix, idx_row_mapper, idx_col_mapper, id_row_mapper, id_col_mapper


def find_similar_KNN(recipe_id: int,
                     X: csr_matrix,
                     recipe_idx_mapper: dict,
                     recipe_id_mapper: dict,
                     k: int,
                     metric='cosine'):
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
    model = NearestNeighbors(n_neighbors=(k + 1), metric=metric)
    model.fit(X)

    neighbor = model.kneighbors(recipe_vec, return_distance=False)
    neighbour_ids = [recipe_id_mapper[neighbor.item(i)] for i in range(k+1)]
    # neighbour_ids.pop(0)
    return neighbour_ids



def get_recommend(recipe_id: int, k: int):
    recipe_ratings = access_db.select(cursor, tablename="recipe_ratings")
    df_DB_RRatings = pd.DataFrame(recipe_ratings, columns=["user_id", "recipe_id", "rating"])

    X, _, idx_col_mapper, _, id_col_mapper = create_userItem_matrix(df_DB_RRatings)
    recommend_recipe_ids = find_similar_KNN(recipe_id, X, idx_col_mapper, id_col_mapper, k)

    return recommend_recipe_ids, idx_col_mapper, id_col_mapper


if __name__ == "__main__":
    # recipes = access_db.select(cursor, tablename="Recipes")
    # ingredients = access_db.select(cursor, tablename="Ingredients")
    # recipes_ingreds = access_db.select(cursor, tablename="RecipeIngredients")
    # recipe_ratings = access_db.select(cursor, tablename="recipe_ratings")

    # df_DB_R = pd.DataFrame(recipes, columns=["recipe_id", "recipe_name", "recipe_info_url", "cooking_step"])
    # df_DB_I = pd.DataFrame(ingredients, columns=["ingredient_id", "ingredient_name"])
    # df_DB_RI = pd.DataFrame(recipes_ingreds, columns=["recipe_id", "ingredient_id"])
    # df_DB_RRatings = pd.DataFrame(recipe_ratings, columns=["user_id", "recipe_id", "rating"])
    # df_DB_I.to_csv("ingredients.csv", index=False)

    #    row: user_id
    # column: recipe_id
    # rating_matrix = df_DB_RRatings.pivot(index="user_id", columns="recipe_id", values="rating")

    # print(df_onehot_RI)
    # print(df_onehot_RI.shape)
    # print()
    # print(rating_matrix)
    # print(rating_matrix.shape)

    # X: user-item matrix
    # X, idx_row_mapper, idx_col_mapper, id_row_mapper, id_col_mapper = create_userItem_matrix(df_DB_RRatings)

    # Evaluating sparsity
    # n_total = X.shape[0] * X.shape[1]
    # n_ratings = X.nnz                       # The number of stored non-empty elements
    # sparsity = n_ratings / n_total

    # print(f"Size of user-item matrix: {X.shape}")
    # print(f"         Matrix sparsity: {n_ratings} / {n_total} = {round(sparsity * 100, 2)}%")
    # print("\n")
    # print("user-item matrix:")
    # print(X)
    # print("\n")

    # n_ratings_per_user = X.getnnz(axis=1)
    # n_ratings_per_recipe = X.getnnz(axis=0)

    # print(f"Number of users rated: {len(n_ratings_per_user)}")
    # print(f"Number of recipes rated: {len(n_ratings_per_recipe)}")
    # print(f"Most active user rated {n_ratings_per_user.max()} recipes.")
    # print(f"Least active user rated {n_ratings_per_user.min()} recipes.")
    # print(f"Most rated recipe has {n_ratings_per_recipe.max()} ratings.")
    # print(f"Least rated recipe has {n_ratings_per_recipe.min()} ratings.")


    # plt.figure(figsize=(16,4))
    # plt.subplot(1,2,1)
    # sns.kdeplot(n_ratings_per_user, fill=True)
    # plt.xlim(0)
    # plt.title("Number of Ratings Per User", fontsize=14)
    # plt.xlabel("number of ratings per user")
    # plt.ylabel("density")

    # plt.subplot(1,2,2)
    # sns.kdeplot(n_ratings_per_recipe, fill=True)
    # plt.xlim(0)
    # plt.title("Number of Ratings Per Recipe", fontsize=14)
    # plt.xlabel("number of ratings per recipe")
    # plt.ylabel("density")

    # idx = 0
    # cosine_sim = cosine_similarity(X.T, X.T)
    # sim_scores = list(enumerate(cosine_sim[idx]))
    # sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # print(cosine_sim)
    # print(sim_scores)

    # similar_recipes = find_similar_KNN(1, X, id_col_mapper, idx_col_mapper, k=5)
    # print(similar_recipes)


    # I2I_matrix, idx_row_mapper, idx_col_mapper, id_row_mapper, id_col_mapper = create_itemItem_matrix(df_RI=df_DB_RI)

    # # Evaluating sparsity
    # n_total = I2I_matrix.shape[0] * I2I_matrix.shape[1]
    # n_ratings = I2I_matrix.nnz                       # The number of stored non-empty elements
    # sparsity = n_ratings / n_total
    # print(f"Size of item-item matrix: {I2I_matrix.shape}")
    # print(f"         Matrix sparsity: {n_ratings} / {n_total} = {round(sparsity * 100, 2)}%")
    # print("\n")
    # print("Item-item matrix:")
    # print(I2I_matrix)
    # print("\n")

    # similar_recipes = find_similar_KNN(1, I2I_matrix, idx_row_mapper, id_row_mapper, k=5)
    # print(similar_recipes)

    recommend_ls, idx_row_mapper, idx_col_mapper, id_row_mapper, id_col_mapper = get_recommend(1, 10)
    print(recommend_ls)

    plt.show()

