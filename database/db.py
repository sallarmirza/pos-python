import sqlite3
import json
from datetime import datetime
DB = "pos.db"

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB)
        self.cur = self.conn.cursor()
        self.setup()

    def setup(self):
        # Users table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT CHECK(role IN ('owner','cashier'))
            )
        """)
        # Ensure default owner exists
        self.cur.execute("SELECT COUNT(*) FROM users WHERE role='owner'")
        if self.cur.fetchone()[0] == 0:
            self.add_user("owner", "owner", "owner")

        # Products table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS products(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sku TEXT UNIQUE,
                name TEXT,
                price REAL,
                stock INTEGER,
                alert_level INTEGER DEFAULT 5
            )
        """)
        # Transactions table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS transactions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cashier TEXT,
                date_time TEXT,
                items TEXT,
                subtotal REAL,
                discount REAL,
                tax REAL,
                total REAL
            )
        """)
        self.conn.commit()

    def add_user(self, username, password, role):
        try:
            self.cur.execute(
                "INSERT INTO users(username,password,role) VALUES (?,?,?)",
                (username, password, role)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def auth_user(self, username, password, role):
        self.cur.execute(
            "SELECT * FROM users WHERE username=? AND password=? AND role=?",
            (username, password, role)
        )
        return self.cur.fetchone()
    def get_all_products(self):
        """
        Returns a list of all products as tuples: (id, sku, name, price, stock, alert_level)
        """
        self.cur.execute("SELECT id, sku, name, price, stock, alert_level FROM products")
        return self.cur.fetchall()


    def add_product(self, sku, name, price, stock, alert_level=5):
        try:
            self.cur.execute(
                "INSERT INTO products(sku,name,price,stock,alert_level) VALUES (?,?,?,?,?)",
                (sku, name, price, stock, alert_level)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def update_product(self, sku, name, price, stock, alert_level):
        """
        Update a product by SKU.
        Returns True if successful, False otherwise.
        """
        try:
            self.cur.execute(
                "UPDATE products SET name=?, price=?, stock=?, alert_level=? WHERE sku=?",
                (name, price, stock, alert_level, sku)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print("Update product error:", e)
            return False

    def delete_product(self, sku):
        """
        Delete a product by SKU.
        Returns True if a row was deleted, False otherwise.
        """
        try:
            self.cur.execute("DELETE FROM products WHERE sku=?", (sku,))
            self.conn.commit()
            return self.cur.rowcount > 0
        except Exception as e:
            print("Delete product error:", e)
            return False
    def get_cashiers(self):
        """
        Returns a list of all cashiers as tuples: (id, username)
        """
        self.cur.execute("SELECT id, username FROM users WHERE role='cashier'")
        return self.cur.fetchall()
    def delete_cashier(self, cashier_id):
        """
        Deletes a cashier by ID.
        Returns True if deleted, False otherwise.
        """
        try:
            self.cur.execute("DELETE FROM users WHERE id=? AND role='cashier'", (cashier_id,))
            self.conn.commit()
            return self.cur.rowcount > 0
        except Exception as e:
            print("Delete cashier error:", e)
            return False
    def setup_transactions(self):
        # Transactions table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cashier TEXT,
                total REAL,
                discount REAL,
                tax REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Items in each transaction
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS transaction_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id INTEGER,
                sku TEXT,
                name TEXT,
                price REAL,
                quantity INTEGER,
                FOREIGN KEY(transaction_id) REFERENCES transactions(id)
            )
        """)
        self.conn.commit()

    def close(self):
        self.conn.close()


    def add_transaction(self, cashier, cart, discount=0, tax=0):
        """
        Add a transaction and update inventory.

        cart: list of tuples (sku, name, price, quantity)
        """
        try:
            # Calculate subtotal and total
            subtotal = sum(price * qty for _, _, price, qty in cart)
            total = subtotal - discount + tax
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Insert into transactions table
            self.cur.execute(
                "INSERT INTO transactions(cashier, total, discount, tax, timestamp) VALUES (?,?,?,?,?)",
                (cashier, total, discount, tax, timestamp)
            )
            transaction_id = self.cur.lastrowid

            # Insert items for this transaction
            for sku, name, price, qty in cart:
                self.cur.execute(
                    "INSERT INTO transaction_items(transaction_id, sku, name, price, quantity) VALUES (?,?,?,?,?)",
                    (transaction_id, sku, name, price, qty)
                )
                # Update inventory
                self.cur.execute("UPDATE products SET stock = stock - ? WHERE sku=?", (qty, sku))

            self.conn.commit()
            return transaction_id
        except Exception as e:
            print("Add transaction error:", e)
            return None

    def get_transactions(self):
        """
        Retrieve all transactions with their items.
        Returns a list of dictionaries.
        """
        self.cur.execute("SELECT id, cashier, total, discount, tax, timestamp FROM transactions ORDER BY id DESC")
        transactions = []
        for tid, cashier, total, discount, tax, timestamp in self.cur.fetchall():
            self.cur.execute("SELECT sku, name, price, quantity FROM transaction_items WHERE transaction_id=?", (tid,))
            items = [{"sku": sku, "name": name, "price": price, "qty": qty} for sku, name, price, qty in self.cur.fetchall()]
            transactions.append({
                "id": tid,
                "cashier": cashier,
                "items": items,
                "discount": discount,
                "tax": tax,
                "total": total,
                "timestamp": timestamp
            })
        return transactions
