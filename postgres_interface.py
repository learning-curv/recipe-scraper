import psycopg2
import psycopg2.extras
import json
from uuid import uuid4


def connect():
    conn = psycopg2.connect(
        database="recipedb",
        host="recipe-db",
        user="postgres",
        password="admin",
        port="5432",
    )

    cursor = conn.cursor()

    return conn, cursor


# name_Table            = "news_stories"

# # Create table statement
# sqlCreateTable = "create table "+name_Table+" (id bigint, title varchar(128), summary varchar(256), story text);"

# # Create a table in PostgreSQL database
# cursor.execute(sqlCreateTable)

# postgresConnection.commit()

# # Get the updated list of tables
# sqlGetTableList = "SELECT table_schema,table_name FROM information_schema.tables where table_schema='test' ORDER BY table_schema,table_name ;"
# #sqlGetTableList = "\dt"

# # Retrieve all the rows from the cursor
# cursor.execute(sqlGetTableList)
# tables = cursor.fetchall()

# # Print the names of the tables
# for table in tables:
#     print(table)


def save_recipes(recipes):
    conn, cursor = connect()

    data = list(map(lambda r: (str(uuid4()), json.dumps(r)), recipes))
    insert_query = 'insert into "recipe-schema".recipes(id, recipe_data) values %s;'
    psycopg2.extras.execute_values(
        cursor, insert_query, data, template=None, page_size=100
    )
    conn.commit()
