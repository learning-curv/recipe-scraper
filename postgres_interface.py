import psycopg2
import psycopg2.extras
import json
from uuid import uuid4

conn = psycopg2.connect(
    database="recipe-app",
    host="recipe-db",
    user="postgres",
    password="admin",
    port="5432",
)

cursor = conn.cursor()


def save_recipes(recipes):
    data = list(map(lambda r: (str(uuid4()), json.dumps(r)), recipes))
    insert_query = "insert into recipe_schema.recipes(id, recipe_data) values %s;"
    psycopg2.extras.execute_values(
        cursor, insert_query, data, template=None, page_size=100
    )
    conn.commit()
