# ============================================================
# DATA — local JSON storage (like localStorage)
# Replace this file with API calls later
# ============================================================

import json
import os
from datetime import datetime

DATA_FILE = "data.json"


def _load():
    if not os.path.exists(DATA_FILE):
        return {"users": [], "products": [], "transactions": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def _save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# USERS
def get_users():
    return _load()["users"]


def add_user(username, password):
    data = _load()
    data["users"].append({"username": username, "password": password})
    _save(data)


def find_user(username, password):
    for u in _load()["users"]:
        if u["username"] == username and u["password"] == password:
            return u
    return None


# PRODUCTS
def get_products():
    return _load()["products"]


def add_product(name, price, stock):
    data = _load()
    data["products"].append(
        {
            "id": str(len(data["products"]) + 1),
            "name": name,
            "price": price,
            "stock": stock,
        }
    )
    _save(data)


def update_product(id, name, price, stock):
    data = _load()
    for p in data["products"]:
        if p["id"] == id:
            p["name"] = name
            p["price"] = price
            p["stock"] = stock
    _save(data)


def delete_product(id):
    data = _load()
    data["products"] = [p for p in data["products"] if p["id"] != id]
    _save(data)


def deduct_stock(id, qty):
    data = _load()
    for p in data["products"]:
        if p["id"] == id:
            p["stock"] -= qty
    _save(data)


# TRANSACTIONS
def get_transactions():
    return _load()["transactions"]


def add_transaction(items, total):
    data = _load()
    data["transactions"].append(
        {
            "id": str(len(data["transactions"]) + 1),
            "items": items,
            "total": total,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )
    _save(data)
