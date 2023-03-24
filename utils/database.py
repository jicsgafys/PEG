import sqlite3


def execute_db_query1(db_filename, query, parameters=()):
    with sqlite3.connect(db_filename) as conn:
        cur = conn.cursor()
        query_result = cur.execute(query, parameters)
        conn.commit()
    return query_result


def execute_db_query2(db_connection, query, parameters=()):
    cur = db_connection.cursor()
    query_results = cur.execute(query, parameters)
    return query_results