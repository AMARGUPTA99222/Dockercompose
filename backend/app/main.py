import os
import mysql.connector
from fastapi import FastAPI
from elasticsearch import Elasticsearch

app = FastAPI(title="E-Commerce API")

def mysql_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "mysql"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        database=os.getenv("MYSQL_DATABASE", "ecommerce"),
        user=os.getenv("MYSQL_USER", "appuser"),
        password=os.getenv("MYSQL_PASSWORD", "")
    )

es = Elasticsearch(os.getenv("ELASTICSEARCH_URL", "http://elasticsearch:9200"))

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/products")
def products():
    conn = mysql_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, name, price, category, stock FROM products")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.get("/search")
def search(q: str):
    result = es.search(
        index="products",
        query={"multi_match": {"query": q, "fields": ["name", "category"]}}
    )
    return [hit["_source"] for hit in result["hits"]["hits"]]

@app.post("/products")
def create_product(name: str, price: float, category: str, stock: int):
    conn = mysql_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (name, price, category, stock) VALUES (%s, %s, %s, %s)",
        (name, price, category, stock)
    )
    product_id = cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()

    document = {
        "id": product_id,
        "name": name,
        "price": price,
        "category": category,
        "stock": stock
    }
    es.index(index="products", id=product_id, document=document, refresh=True)
    return document
