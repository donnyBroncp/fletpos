# ============================================================
# DATA — local JSON storage with error trapping
# ============================================================

import json
import os
from datetime import datetime

DATA_FILE = "data.json"


def _load():
    try:
        if not os.path.exists(DATA_FILE):
            return {"users": [], "products": [], "transactions": []}
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"[ERROR] Failed to load data: {e}")
        return {"users": [], "products": [], "transactions": []}


def _save(data):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"[ERROR] Failed to save data: {e}")
        raise Exception("Failed to save data. Please try again.")


# USERS
def get_users():
    try:
        return _load()["users"]
    except Exception as e:
        print(f"[ERROR] get_users: {e}")
        return []


def add_user(username, password):
    try:
        data = _load()
        data["users"].append({"username": username, "password": password})
        _save(data)
    except Exception as e:
        raise Exception(f"Failed to register user: {e}")


def find_user(username, password):
    try:
        for u in _load()["users"]:
            if u["username"] == username and u["password"] == password:
                return u
        return None
    except Exception as e:
        print(f"[ERROR] find_user: {e}")
        return None


# PRODUCTS
def get_products():
    try:
        return _load()["products"]
    except Exception as e:
        print(f"[ERROR] get_products: {e}")
        return []


def add_product(name, price, stock):
    try:
        data = _load()
        data["products"].append(
            {
                "id": str(len(data["products"]) + 1),
                "name": name,
                "price": float(price),
                "stock": int(stock),
            }
        )
        _save(data)
    except ValueError:
        raise Exception("Invalid price or stock value.")
    except Exception as e:
        raise Exception(f"Failed to add product: {e}")


def update_product(id, name, price, stock):
    try:
        data = _load()
        for p in data["products"]:
            if p["id"] == id:
                p["name"] = name
                p["price"] = float(price)
                p["stock"] = int(stock)
        _save(data)
    except ValueError:
        raise Exception("Invalid price or stock value.")
    except Exception as e:
        raise Exception(f"Failed to update product: {e}")


def delete_product(id):
    try:
        data = _load()
        data["products"] = [p for p in data["products"] if p["id"] != id]
        _save(data)
    except Exception as e:
        raise Exception(f"Failed to delete product: {e}")


def deduct_stock(id, qty):
    try:
        data = _load()
        for p in data["products"]:
            if p["id"] == id:
                if p["stock"] < qty:
                    raise Exception(f"Not enough stock for {p['name']}")
                p["stock"] -= qty
        _save(data)
    except Exception as e:
        raise Exception(f"Failed to deduct stock: {e}")


# TRANSACTIONS
def get_transactions():
    try:
        return _load()["transactions"]
    except Exception as e:
        print(f"[ERROR] get_transactions: {e}")
        return []


def add_transaction(items, total):
    try:
        data = _load()
        data["transactions"].append(
            {
                "id": str(len(data["transactions"]) + 1),
                "items": items,
                "total": float(total),
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
        _save(data)
    except Exception as e:
        raise Exception(f"Failed to save transaction: {e}")


def get_users():
    try:
        return _load()["users"]
    except Exception as e:
        print(f"[ERROR] get_users: {e}")
        return []


def add_user(username, password):
    try:
        data = _load()
        data["users"].append({"username": username, "password": password})
        _save(data)
    except Exception as e:
        raise Exception(f"Failed to register user: {e}")


def find_user(username, password):
    try:
        for u in _load()["users"]:
            if u["username"] == username and u["password"] == password:
                return u
        return None
    except Exception as e:
        print(f"[ERROR] find_user: {e}")
        return None


def update_user(username, new_password):
    try:
        data = _load()
        for u in data["users"]:
            if u["username"] == username:
                u["password"] = new_password
        _save(data)
    except Exception as e:
        raise Exception(f"Failed to update user: {e}")


def delete_user(username):
    try:
        data = _load()
        data["users"] = [u for u in data["users"] if u["username"] != username]
        _save(data)
    except Exception as e:
        raise Exception(f"Failed to delete user: {e}")
