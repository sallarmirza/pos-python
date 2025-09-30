import sqlite3

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

    def close(self):
        self.conn.close()
