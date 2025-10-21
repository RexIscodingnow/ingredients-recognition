from recommend_sys.access_db import cursor, select, insert, update


def query(tablename: str,
          target: dict[str, int | float | str] = {},
          columns: list = [],
          fuzzy_search: bool = False):
    conditions = []
    for col, val in target.items():
        if fuzzy_search:
            conditions.append([col, "LIKE", val])
        else:
            conditions.append([col, "=", val])

    return select(cursor=cursor,
                  tablename=tablename,
                  columns=columns,
                  conditions=conditions)


def insert_data(tablename: str, data: dict[str, int | float | str]):
    columns = []
    values = []
    for col, val in data.items():
        columns.append(col)
        values.append(val)

    insert(cursor=cursor,
           tablename=tablename,
           columns=columns,
           values=[values])


def update_data(tablename: str, data: dict[str, int | float | str], target: dict[str, int | float | str]):
    conditions = []
    for col, val in target.items():
        conditions.append([col, "=", val])

    update(cursor=cursor,
           tablename=tablename,
           new_values=data,
           conditions=conditions)

