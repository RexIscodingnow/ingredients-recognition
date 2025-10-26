from recommend_sys.access_db import cursor, select, insert, update


def query(tablename: str,
          target: dict[str, int | float | str | list | tuple] = {},
          columns: list = [],
          fuzzy_search: bool = False):
    """Retrieve the data from the specific table.

    Args:
        tablename: The name of the table.
        target: A `dict` mapping column names to their corresponding target values for filtering data.
                Multiple key-value pairs can be used to match multiple columns.

        columns: A sequence of the columns to retrieve. If None, selects all.
        fuzzy_search: Execute the `LIKE` operator if set `True`. Defaults to `False`.

    Returns:
        Sequence[tuple]: Sequence of rows returned by the query.
    """
    conditions = []
    for col, val in target.items():
        if isinstance(val, (list, tuple)):
            conditions.append([col, "IN", val])
        else:
            if fuzzy_search:
                conditions.append([col, "LIKE", val])
            else:
                conditions.append([col, "=", val])

    return select(cursor=cursor,
                  tablename=tablename,
                  columns=columns,
                  conditions=conditions)


def insert_data(tablename: str, data: dict[str, int | float | str]):
    """Insert data into the specific table.

    Args:
        tablename: The name of the table.
        data: A `dict` mapping column names to their corresponding target values for inserting data.
    """
    columns = []
    values = []
    for col, val in data.items():
        columns.append(col)
        values.append(val)

    insert(cursor=cursor,
           tablename=tablename,
           columns=columns,
           values=[values])


def update_data(tablename: str,
                data: dict[str, int | float | str],
                target: dict[str, int | float | str | list | tuple]):
    """Update the data in the specific table.

    Args:
        tablename: The name of the table.
        data: A `dict` mapping column names to their corresponding target values for updating data.

        target: A `dict` mapping column names to their corresponding target values for filtering data.
                Multiple key-value pairs can be used to match multiple columns.
    """
    conditions = []
    for col, val in target.items():
        if isinstance(val, (list, tuple)):
            conditions.append([col, "IN", val])
        else:
            conditions.append([col, "=", val])

    update(cursor=cursor,
           tablename=tablename,
           new_values=data,
           conditions=conditions)

