import os
import re
import dotenv
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
_ALLOWED_OPERATORS = {'=', '!=', '>', '>=', '<', '<=', 'LIKE', 'IN', 'NOT IN', 'IS', 'IS NOT'}
_ALLOWED_LOGICAL = {'AND', 'OR'}


def show_table_info(cursor: MySQLCursorAbstract, schema_name: str = "", *, show_columns=False):
    """
    List the table names and column names of all databases (schema) and print on the terminal.

    References:
        CREATE SCHEMA is a synonym for CREATE DATABASE as of MySQL 5.0.2.
        The documentation: https://dev.mysql.com/doc/refman/8.4/en/create-database.html

    Args:
        cursor: MySQL cursor object.
        schema_name: The name of the schema. If not provided, all schemas will be listed.
        show_columns: List all columns name of the tables if it set to `True`.

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
        ... (The schema information above has been omitted.)

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
            params: Sequence = ()) -> Sequence:
    if columns is not None and len(columns) > 0:
        for col in columns:
            if not _VALID_IDENTIFIER.match(col):
                raise ValueError(f"Invalid column name: {col}")
        columns = "(" + ",".join([f"`{col}`" for col in columns]) + ")"
    else:
        columns = "*"

    sql_script = f"SELECT {columns} FROM `{tablename}`"
    if conditions:
        sql_script += " WHERE " + conditions
    sql_script += ';'

    print(sql_script, "\n", params)
    cursor.execute(sql_script, params)
    return [item for item in cursor]


def select(cursor: MySQLCursorAbstract,
           tablename: str,
           columns: Sequence[str] = None,
           conditions: Iterable[Sequence[str | int | float]] = None
           ) -> Sequence:
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
        /* This is an example of a MySQL SELECT command. */
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
    if columns is not None and not isinstance(columns, Sequence):
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
        op = op.upper()
        logical_op = cond[3].upper() if len(cond) == 4 else "AND"

        if not _VALID_IDENTIFIER.match(col):
            raise ValueError(f"Invalid column name in condition: {col}")
        if op not in _ALLOWED_OPERATORS:
            raise ValueError(f"Invalid operator: '{op}' is not allowed.")
        if logical_op not in _ALLOWED_LOGICAL:
            raise ValueError(f"Invalid logical operator: {logical_op} is not allowed.")

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
           values: Iterable[str | int | float] = []):
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
    sql_script = f"""
                 INSERT INTO `{tablename}` {column_names} VALUES {column_params};
                 """
    # print(sql_script, values)
    cursor.executemany(sql_script, [values])
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

            expr = f"`{col}` {op} %s"
            cond_params.append(val)
            if i < len(conditions) - 1:
                expr += f" {logical_op}"
            parts.append(expr)

        conditions_str = " ".join(parts)

    sql_script += " WHERE " + conditions_str
    sql_script += ';'
    params.extend(cond_params)

    print(sql_script, f"\n{params} ")
    cursor.executemany(sql_script, [params])
    db.commit()


if __name__ == "__main__":
    schama_info = show_table_info(cursor, schema_name="recipes_ingredients", show_columns=True)

    # import pandas as pd

    # recipe_info = pd.read_csv("未命名的試算表 - 工作表1.csv")
    # r_names = recipe_info["食譜名"]
    # r_ingredients = recipe_info["食材"]
    # cooking_step = recipe_info["料理步驟"]
    # r_url = recipe_info["食譜網站資訊"]

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
    # recipe_ids = []
    # insert_data: dict[str, list] = {}

    # for r in recipe_name:
    #     id = _select(cursor, 
    #                 tablename="Recipes", 
    #                 columns="recipe_id", 
    #                 conditions=f"`recipe_name` = '{r}'")
    #     id = id[0][0]
    #     recipe_ids.append(id)

    #     insert_data[id] = []
    #     for ingredient in recipe[r]:
    #         ingredient_id = _select(cursor, 
    #                                tablename="Ingredients", 
    #                                columns="ingredient_id", 
    #                                conditions=f"`ingredient_name`='{ingredient}'")
    #         ingredient_id = ingredient_id[0][0]
    #         insert_data[id].append(ingredient_id)

    # print(insert_data)

    # for recipe_id, ingredient_ids in insert_data.items():
    #     values = []

    #     for i_id in ingredient_ids:
    #         values.append([recipe_id, i_id])

    #     insert(cursor, tablename="RecipeIngredients", columns=("recipe_id", "ingredient_id"), values=values)


