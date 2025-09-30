import sqlite3

DB = 'pos.db'

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB)
        self.cur = self.conn.cursor()
        self.setup()

    def setup(self):
        # Users table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT CHECK (role IN ('owner','cashier'))
        )""")
        self.conn.commit()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE,
            name TEXT,
            price REAL,
            stock INTEGER,
            alert_level INTEGER DEFAULT 5
        )""")
        self.conn.commit()
        # Ensure at least one owner exists
        self.cur.execute("SELECT COUNT(*) FROM users WHERE role='owner'")
        if self.cur.fetchone()[0] == 0:
            self.add_user("owner", "owner", "owner")  # default owner

    def add_user(self, username, password, role):
        try:
            self.cur.execute(
                "INSERT INTO users(username, password, role) VALUES (?, ?, ?)",
                (username, password, role)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_cashiers(self):
        self.cur.execute("SELECT id, username FROM users WHERE role='cashier'")
        return self.cur.fetchall()

    def delete_cashier(self, cashier_id):
        self.cur.execute("DELETE FROM users WHERE id=? AND role='cashier'", (cashier_id,))
        self.conn.commit()
    def auth_user(self, username, password, role):
        self.cur.execute(
            "SELECT * FROM users WHERE username=? AND password=? AND role=?",
            (username, password, role)
        )
        return self.cur.fetchone()
    def get_all_products(self):
        self.cur.execute("SELECT id, sku, name, price, stock, alert_level FROM products")
        return self.cur.fetchall()

    def close(self):
        self.conn.close()
