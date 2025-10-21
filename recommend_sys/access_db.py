import os
import re
import dotenv
import pandas as pd
import mysql.connector as conn

from mysql.connector.abstracts import MySQLCursorAbstract
from typing import Sequence, Iterable


dotenv.load_dotenv()

db = conn.connect(
    host=os.getenv("host"),
    user=os.getenv("user"),
    password=os.getenv("password"),
    database=os.getenv("database")
)

cursor = db.cursor()
_VALID_IDENTIFIER = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
_ALLOWED_OPERATORS = {'=', '!=', '>', '>=', '<', '<=', 'LIKE', 'IN'}
_ALLOWED_LOGICAL = {'AND', 'OR'}


def show_table_info(cursor: MySQLCursorAbstract, schema_name: str = "", *, show_columns=False):
    """List the table names and column names of all databases (schemas) and print them in the terminal.

    References:
        CREATE SCHEMA is a synonym for CREATE DATABASE as of MySQL 5.0.2.
        The documentation: https://dev.mysql.com/doc/refman/8.4/en/create-database.html

    Args:
        cursor: MySQL cursor object.
        schema_name: The name of the schema. If not provided, all schemas will be listed.
        show_columns: List all column names of the tables if it set to `True`.

    Returns:
        schema_info: The dictionary containing all databases,
                     each mapping to their respective tables and column names.

    Examples:
        ```
        >>> db = conn.connect(
        ...     host="localhost",
        ...     user="<username>",
        ...     password="<your password>",
        ...     database="<your database name>"
        ... )
        >>> cursor = db.cursor()
        >>> schama_info = show_table_info(cursor, show_columns=True)
        >>> schama_info
        ...
        ...
        # ... (output omitted)

        [Schema] world
            Table: city
                    Columns: CountryCode, District, ID, Name, Population

            Table: country
                    Columns: Capital, Code, Code2, Continent, GNP, GNPOld, GovernmentForm, HeadOfState, IndepYear, LifeExpectancy, LocalName, Name, Population, Region, SurfaceArea

            Table: countrylanguage
                    Columns: CountryCode, IsOfficial, Language, Percentage

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

        >>> schama_info
        {
            'world': {
                'city': ['CountryCode', 'District', 'ID', 'Name', 'Population'], 
                'country': ['Capital', 'Code', 'Code2', 'Continent', 'GNP', 'GNPOld', 
                            'GovernmentForm', 'HeadOfState', 'IndepYear', 'LifeExpectancy', 
                            'LocalName', 'Name', 'Population', 'Region', 'SurfaceArea'], 
                'countrylanguage': ['CountryCode', 'IsOfficial', 'Language', 'Percentage']
            },
            'recipes_ingredients': {
                'ingredients': ['ingredient_id', 'ingredient_name'], 
                'recipe_ratings': ['rating', 'recipe_id', 'user_id'], 
                'recipeingredients': ['ingredient_id', 'recipe_id'], 
                'recipes': ['cooking_step', 'recipe_id', 'recipe_info_url', 'recipe_name'], 
                'users': ['email', 'password', 'user_id', 'username']
            }
        }
        ```
    """
    # 取得所有 schema
    cursor.execute(f"""
                   SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA 
                   {f"WHERE SCHEMA_NAME = '{schema_name}'" if len(schema_name) > 0 else ""}
                   """)
    schemas = [row[0] for row in cursor]
    schema_info: dict[str, dict[str, list]] = {}

    for schema in schemas:
        print(f"[Schema] {schema}")

        # 取得該 schema 下所有 table
        cursor.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{schema}';")
        tables = [row[0] for row in cursor]
        schema_info[schema] = {}

        for table in tables:
            print(f"  Table: {table}")
            schema_info[schema][table] = []

            # 顯示該 table 的欄位名稱
            if show_columns:
                cursor.execute(f"""
                    SELECT COLUMN_NAME 
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{table}';
                """)
                columns = [row[0] for row in cursor]
                schema_info[schema][table] = columns
                print("\t Columns:", ", ".join(columns), "\n")

    return schema_info


def _select(cursor: MySQLCursorAbstract,
            tablename: str, 
            columns: Sequence[str] = None, 
            conditions: str = "",
            params: Sequence = ()) -> Sequence[tuple]:
    if columns is not None and len(columns) > 0:
        for col in columns:
            if not _VALID_IDENTIFIER.match(col):
                raise ValueError(f"Invalid column name: {col}")
        columns = ",".join([f"`{col}`" for col in columns])
    else:
        columns = "*"

    sql_script = f"SELECT {columns} FROM `{tablename}`"
    if conditions:
        sql_script += " WHERE " + conditions
    sql_script += ';'

    # print(sql_script, "\n", params)
    cursor.execute(sql_script, params)
    return [item for item in cursor]


def select(cursor: MySQLCursorAbstract,
           tablename: str,
           columns: Sequence[str] = None,
           conditions: Iterable[Sequence[str | int | float]] = None
           ) -> Sequence[tuple]:
    """Select command

    Args:
        cursor: MySQL cursor object.
        tablename: The name of the table.
        columns: A sequence of the columns to retrieve. If None, selects all.
        conditions: A sequence of WHERE conditions.
                [
                    [column, operator, value, (optional) logical operator], ...
                ]
    Returns:
        Sequence: Sequence of rows returned by the query.

    Examples:
        ```
        /* This is an example of a MySQL `SELECT` command. */
        SELECT * FROM `Ingredients`
        WHERE ingredient_name = '味精' OR ingredient_name LIKE '雞%' OR ingredient_name LIKE '蒜%';
        ```

        Convert the above MySQL command into the `select()` parameters.
        ```
        >>> db = conn.connect(
        ...     host="localhost",
        ...     user="<username>",
        ...     password="<your password>",
        ...     database="<your database name>"
        ... )
        >>> cursor = db.cursor()
        >>> 
        >>> tablename = "Ingredients"
        >>> conditions = [
        ...     ["ingredient_name", "=", "味精", "OR"],
        ...     ["ingredient_name", "LIKE", "雞%", "OR"],
        ...     ["ingredient_name", "LIKE", "蒜%"]
        ... ]
        >>> select(cursor, tablename=tablename, conditions=conditions)
        [(48, '味精'), (41, '蒜末'), (36, '蒜頭'), (31, '雞扒/雞排'), (50, '雞蛋')]
        ```
    """
    if columns is not None and (isinstance(columns, str) or not isinstance(columns, Sequence)):
        raise TypeError("TypeError - The argument `columns` must be a sequence.")

    if conditions is None or not conditions:
        return _select(cursor, tablename, columns, "")

    if not isinstance(conditions, Iterable):
        raise TypeError("TypeError - The argument `conditions` must be a iterable sequence.")

    parts = []
    params = []
    conditions_str = ""

    for i, cond in enumerate(conditions):
        if not (3 <= len(cond) <= 4):
            raise ValueError(
                f"Condition #{i + 1} must have 3 or 4 elements: [column, operator, value, (optional) logical_op]"
            )

        col, op, val = cond[0], cond[1], cond[2]
        op = op.upper().strip()
        logical_op = cond[3].upper() if len(cond) == 4 else "AND"

        if not _VALID_IDENTIFIER.match(col):
            raise ValueError(f"Invalid column name in condition: {col}")
        if op not in _ALLOWED_OPERATORS:
            raise ValueError(f"Invalid operator: '{op}' is not allowed.")
        if logical_op not in _ALLOWED_LOGICAL:
            raise ValueError(f"Invalid logical operator: {logical_op} is not allowed.")

        if op == "IN":
            if not isinstance(val, (list, tuple)) or len(val) == 0:
                raise ValueError("IN operator requires a non-empty list/tuple as value")

            placeholders = ",".join(["%s"] * len(val))
            expr = f"`{col}` IN ({placeholders})"
            params.extend(val)
        else:
            expr = f"`{col}` {op} %s"
            params.append(val)

        if i < len(conditions) - 1:
            expr += f" {logical_op}"
        parts.append(expr)

    conditions_str = " ".join(parts)
    return _select(cursor, tablename, columns, conditions_str, params)


def insert(cursor: MySQLCursorAbstract,
           tablename: str,
           columns: Sequence[str] = None,
           values: Sequence[Sequence[str | int | float]] = []):
    """Insert command

    Args:
        cursor: MySQL cursor object.
        tablename: The name of the table.
        columns: A sequence of the columns to insert into the table. If None, all columns will be used.
        values: 
            An iterable containing the values to be inserted into the table. 
            Each item in the iterable should represent one row of values, 
            with the values in the same order as the columns specified (or the table's column order if no columns are specified).
            For example:
                - When `columns` is provided: `values` should be a sequence of tuples or lists, where each tuple/list corresponds to 
                  one row of values to insert.
                - When `columns` is not provided: `values` should be an iterable of values in the same order as the table's columns.
    """
    if columns is not None and not isinstance(columns, Sequence):
        raise TypeError("TypeError - The argument `columns` must be a Sequence.")
    if values is not None and not isinstance(values, Sequence):
        raise TypeError("TypeError - The argument `values` must be a sequence.")
    if len(values) < 1:
        raise ValueError("ValueError - The argument `values` must at least one item.")
    if len(columns) > 0:
        for col in columns:
            if not _VALID_IDENTIFIER.match(col):
                raise ValueError(f"Invalid column name: {col}")
        column_names = "(" + ",".join([f"`{col}`" for col in columns]) + ")"
    else:
        column_names = ""

    column_params = "(" + ", ".join(["%s"] * len(columns)) + ")"
    sql_script = f"INSERT IGNORE INTO `{tablename}` {column_names} VALUES {column_params};"
    # print(sql_script, "\n", values)
    cursor.executemany(sql_script, values)
    db.commit()    # Commits current transaction.


def update(cursor: MySQLCursorAbstract,
           tablename: str,
           new_values: dict[str, str | int | float],
           conditions: Iterable[Sequence[str | int | float]] = None):
    """Update command

    Args:
        cursor: MySQL cursor object.
        tablename: The name of the table.
        new_values: The dictionary of the columns and new values to update into the table.
        conditions: A sequence of WHERE conditions.
                [
                    [column, operator, value, (optional) logical operator], ...
                ]
    Examples:
        ```
        /* This is an example of a MySQL UPDATE command. */
        UPDATE `Recipes` SET 
        `cooking_step` = '.....2. 起油鍋爆香蒜頭..........', `recipe_info_url` = 'owie4fjiwejfwejf.coom' 
        WHERE `recipe_name` LIKE '%肉%' OR `recipe_name` LIKE '%蛋';
        ```

        Convert the above MySQL command into the update() parameters.
        ```
        >>> db = conn.connect(
        ...     host="localhost",
        ...     user="<username>",
        ...     password="<your password>",
        ...     database="<your database name>"
        ... )
        >>> cursor = db.cursor()
        >>> 
        >>> new_values = {
        ...     "cooking_step": ".....2. 起油鍋爆香蒜頭..........",
        ...     "recipe_info_url": "owie4fjiwejfwejf.coom"
        ... }
        >>> conditions = [
        ...     ["recipe_name", "LIKE", "%肉%", "OR"],
        ...     ["recipe_name", "LIKE", "%蛋", "OR"]
        ... ]
        >>> update(cursor, tablename="Recipes", new_values=new_values, conditions=conditions)
        ```
    """
    sql_script = f"UPDATE `{tablename}` SET "
    params = []

    for col, val in new_values.items():
        params.append(val)        
        sql_script += f"`{col}` = %s, "
    sql_script = sql_script[:-2]

    if conditions is not None:
        if not isinstance(conditions, Iterable):
            raise TypeError("TypeError - The argument `conditions` must be a iterable sequence.")

        parts = []
        cond_params = []
        conditions_str = ""

        for i, cond in enumerate(conditions):
            if not (3 <= len(cond) <= 4):
                raise ValueError(
                    f"Condition #{i + 1} must have 3 or 4 elements: [column, operator, value, (optional) logical_op]"
                )

            col, op, val = cond[0], cond[1], cond[2]
            op = op.upper()
            logical_op = cond[3].upper() if len(cond) == 4 else "AND"

            if not _VALID_IDENTIFIER.match(col):
                raise ValueError(f"Invalid column name in condition: {col}")
            if op not in _ALLOWED_OPERATORS:
                raise ValueError(f"Invalid operator: '{op}' is not allowed.")
            if logical_op not in _ALLOWED_LOGICAL:
                raise ValueError(f"Invalid logical operator: {logical_op} is not allowed.")

            if op == "IN":
                if not isinstance(val, (list, tuple)) or len(val) == 0:
                    raise ValueError("IN operator requires a non-empty list/tuple as value")

                placeholders = ",".join(["%s"] * len(val))
                expr = f"`{col}` IN ({placeholders})"
                params.extend(val)
            else:
                expr = f"`{col}` {op} %s"
                params.append(val)

            if i < len(conditions) - 1:
                expr += f" {logical_op}"
            parts.append(expr)

        conditions_str = " ".join(parts)

    sql_script += " WHERE " + conditions_str
    sql_script += ';'
    params.extend(cond_params)

    # print(sql_script, f"\n{params} ")
    cursor.executemany(sql_script, [params])
    db.commit()


def add_recipe_info(df: pd.DataFrame):
    """Add the multiple informations of recipes by `pandas.DataFrame`.
    Execute the `insert()` to insert these informations for 'Recipes', 'Ingredients', and 'RecipeIngredients' tables, respectively.

    Args:
        df: A `pandas.DataFrame` contains the recipe informations such as recipe name, cooking step, reference URL, and ingredients.
    """
    columns = ["食譜名", "食材", "料理步驟", "食譜網站資訊"]

    if len(columns) != len(df.columns) or not all([col in df.columns for col in columns]):
        raise Exception(f"It must contains: {columns} column name")

    #TODO: Check it !
    table_cols_mp = {
        "Recipes": ["cooking_step", "recipe_info_url", "recipe_name"],
        "Ingredients": ["ingredient_name"],
        "RecipeIngredients": ["recipe_id", "ingredient_id"]
    }
    insert_recipes = []
    ingredient_set = set()
    recipe_ingred_mp = {}   # Name of recipe --> list of ingredients

    for idx, row in df.iterrows():
        r_name = row["食譜名"]
        ingredients = [i_name.strip() for i_name in row["食材"].split(",")]
        ingredient_set.update(ingredients)
        insert_recipes.append([row["料理步驟"], row["食譜網站資訊"], r_name])
        recipe_ingred_mp[r_name] = ingredients
    insert_ingredients = list(ingredient_set)

    insert(cursor,
           tablename="Recipes",
           columns=table_cols_mp["Recipes"],
           values=insert_recipes)
    insert(cursor,
           tablename="Ingredients",
           columns=table_cols_mp["Ingredients"],
           values=[insert_ingredients])

    r_names = df["食譜名"].unique().tolist()
    i_names = list(ingredient_set)
    recipe_res = select(cursor,
                        tablename="Recipes",
                        columns=["recipe_id", "recipe_name"],
                        conditions=[["recipe_name", "IN", r_names]])
    ingred_res = select(cursor,
                        tablename="Ingredients",
                        conditions=[["ingredient_name", "IN", i_names]])

    recipe_id_mp = {name: r_id for r_id, name in recipe_res}    # recipe name --> recipe_id
    ingred_id_mp = {name: i_id for i_id, name in ingred_res}    # ingredient name --> ingredient_id
    insert_recipe_ingredients = []

    for recipe_name, ingredient_names in recipe_ingred_mp.items():
        r_id = recipe_id_mp.get(recipe_name)
        if r_id is None:
            continue

        for i_name in ingredient_names:
            i_id = ingred_id_mp.get(i_name)
            if i_id is None:
                continue

            insert_recipe_ingredients.append([r_id, i_id])

    insert(cursor,
           tablename="RecipeIngredients",
           columns=table_cols_mp["RecipeIngredients"],
           values=insert_recipe_ingredients)

    print("Done !")


def update_multiRecipes(data: pd.DataFrame):
    #TODO: Complete the function
    if len(columns) != len(data.columns) or not all([col in data.columns for col in columns]):
        raise Exception(f"data-type: {type(data)}. It must contains: {columns} columns names.")

    recipe_ingred_mp = {}
    columns = ["食譜名", "食材", "料理步驟", "食譜網站資訊"]

    for idx, row in data.iterrows():
        r_name = row["食譜名"]
        ingredients = [i_name.strip() for i_name in row["食材"].split(",")]
        recipe_ingred_mp[r_name] = {
            "ingredients": ingredients,
            "cooking_step": row["料理步驟"],
            "recipe_url": row["食譜網站資訊"]
        }

    # empty: doing noting
    # non-empty: updating data
    for r_name, values in recipe_ingred_mp:
        pass


def get_abspath_files(path: str):
    path = os.path.abspath(path)
    return [os.path.abspath(entry.path) for entry in os.scandir(path) if entry.is_file()]


# @functools.cache
def merge_csv_to_df(files: Iterable[str]) -> pd.DataFrame:
    """
    Concatenate multiple `pandas.Dataframe` objects from a list of csv file paths.
    
    Parameter:
        - files: a sequence of relative/absolute paths.
    """
    df_lst = [pd.read_csv(csv_file) for csv_file in files]    
    df_merged = pd.concat(df_lst, ignore_index=True)
    return df_merged


if __name__ == "__main__":
    schama_info = show_table_info(cursor, schema_name="recipes_ingredients", show_columns=True)

    # recipe_info = pd.read_csv("recipes (1).csv")
    # add_recipe_info(recipe_info)

    """
    # Check that all recipes and ingredients have been correctly inserted into the DB.
    reci = select(cursor, 
                  tablename="Recipes", 
                  columns=["recipe_id", "recipe_name"])
    ingr = select(cursor, 
                  tablename="Ingredients")
    re_in = select(cursor, 
                   tablename="RecipeIngredients")    
    df_DB_R = pd.DataFrame(reci, columns=["recipe_id", "recipe_name"])
    df_DB_I = pd.DataFrame(ingr, columns=["ingredient_id", "ingredient_name"])
    df_DB_RI = pd.DataFrame(re_in, columns=["recipe_id", "ingredient_id"])

    df_recipe_info = merge_csv_to_df([f"recipes_{i}.csv" for i in range(6)])
    df_recipe_info = df_recipe_info.drop_duplicates(subset=['食譜名'])
    
    ingredient_set = set()
    recipe_ingred_mp = {}   # Name of recipe --> list of ingredients
    for idx, row in df_recipe_info.iterrows():
        r_name = row["食譜名"]
        ingredients = [i_name.strip() for i_name in row["食材"].split(",")]
        ingredient_set.update(ingredients)
        recipe_ingred_mp[r_name] = ingredients

    r_names = [name for name in recipe_ingred_mp.keys()]
    i_names = list(ingredient_set)

    print(all(r in r_names for r in df_DB_R["recipe_name"].tolist()))
    print(all(i in ingredient_set for i in df_DB_I["ingredient_name"].tolist()))
    """


    # r_names = recipe_info["食譜名"].tolist()
    # r_ingredients = recipe_info["食材"].tolist()
    # cooking_step = recipe_info["料理步驟"].tolist()
    # r_url = recipe_info["食譜網站資訊"].tolist()

    # recipe_cols = ["cooking_step", "recipe_info_url", "recipe_name"]
    # recipe_values = []
    # for i in range(len(r_names)):
    #     recipe_values.append([cooking_step[i], r_url[i], r_names[i]])

    # s = set()
    # for i in range(len(r_ingredients)):
    #     s.update(r_ingredients[i].split(', '))

    # s.remove('雞蛋')
    # s.remove('胡椒')
    # s.remove('香油')
    # s.remove('醬油')
    # s.remove('蔥')
    # ingredients = [[i] for i in s]
    # print(ingredients)
    # insert(cursor, tablename="Recipes", columns=recipe_cols, values=recipe_values)
    # insert(cursor, tablename="Ingredients", columns=["ingredient_name"], values=ingredients)

    # for name in r_names:
    #     r_step = recipe_info[recipe_info["食譜名"] == name]["料理步驟"].to_string(index=False)
    #     new_recipe_info = {
    #         "cooking_step": r_step
    #     }
    #     conditions = [
    #         ["recipe_name", "=", name]
    #     ]
    #     update(cursor, 
    #            tablename="Recipes",
    #            new_values=new_recipe_info,
    #            conditions=conditions)


    # new_values = {
    #     "cooking_step": ".....2. 起油鍋爆香蒜頭..........",
    #     "recipe_info_url": "owie4fjiwejfwejf.cooom"
    # }
    # conditions = [
    #     ["recipe_name", "LIKE", "%肉%", "OR"],
    #     ["recipe_name", "LIKE", "%蛋", "OR"]
    # ]
    # print(update(cursor, tablename="Recipes", new_values=new_values, conditions=conditions))
    # update(cursor, "Recipes", new_values=new_values, conditions=conditions)
    
    # conditions = [
    #     ["ingredient_name", "=", "味精", "OR"],
    #     ["ingredient_name", "LIKE", "雞%", "OR"],
    #     ["ingredient_name", "=", "1=1", "OR"],
    #     ["ingredient_name", "LIKE", "蒜%"]
    # ]
    # print(select(cursor, tablename="Recipes", conditions=conditions))
    # print(select(cursor, tablename="Recipes"))

    # recipe = {
    #     "台式三杯雞": ["雞扒/雞排", "麻油", "醬油", "米酒", "糖", "蒜頭", "薑", "九層塔"],
    #     "酸甜涼拌川耳(五辛素)": ["川耳(泡發)", "小黃瓜", "蒜末", "大辣椒", "白芝麻", "醬油膏", "香油", "白醋", "砂糖", "味精"],
    #     "番茄炒蛋": ["蕃茄", "雞蛋", "糖", "蕃茄醬", "蔥花", "鹽巴"],
    #     "蔥爆豬五花": ["豬五花","蔥","大蒜","鹽巴","胡椒","醬油","米酒","糖","香油"],
    #     "青椒炒肉絲": ["青椒", "蒜頭", "豬肉絲", "醬油", "鹽巴"]
    # }

    # recipe_name = [name for name in recipe.keys()]
    # recipe_name = r_names
    # recipe_ids = []
    # insert_data: dict[str, list] = {}
    # tmp_ingredients = set()

    # for r in recipe_name:
    #     recipe_query = select(cursor, 
    #                           tablename="Recipes", 
    #                           columns=["recipe_id"], 
    #                           conditions=[["recipe_name", "=", r]])
    #     id = recipe_query[0][0]
    #     recipe_ids.append(id)
    #     ingredients = recipe_info[recipe_info["食譜名"] == r]["食材"].to_string(index=False)

    #     if id not in insert_data.keys():
    #         insert_data[id] = []

    #     for ingredient in ingredients.split(', '):
    #         ingredient_id = select(cursor, 
    #                                tablename="Ingredients", 
    #                                columns=["ingredient_id"], 
    #                                conditions=[["ingredient_name", "=", ingredient]])
    #         if len(ingredient_id) > 0:
    #             ingredient_id = ingredient_id[0][0]
    #             insert_data[id].append(ingredient_id)
    #         else:
    #             tmp_ingredients.add(ingredient)

    # print(insert_data)

    # for recipe_id, ingredient_ids in insert_data.items():
    #     values = []

    #     for i_id in ingredient_ids:
    #         values.append([recipe_id, i_id])

    #     print(values)

    #     try:
    #         insert(cursor, tablename="RecipeIngredients", columns=("recipe_id", "ingredient_id"), values=values)

    #     except Exception as e:
    #         print(f"Insert error: {e}")

