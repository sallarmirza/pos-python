from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
    QPushButton, QSpinBox, QTableWidget, QTableWidgetItem,
    QMessageBox
)

TAX_RATE = 0.15
DISCOUNT_RATE = 0.10

class SaleWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.cart = []

        self.setWindowTitle("New Sale")
        self.setGeometry(300, 200, 700, 400)

        layout = QVBoxLayout()

        # Add Product
        input_layout = QHBoxLayout()
        self.sku_input = QLineEdit()
        self.sku_input.setPlaceholderText("Enter SKU")
        self.qty_input = QSpinBox()
        self.qty_input.setMinimum(1)
        self.add_btn = QPushButton("Add to Cart")
        self.add_btn.clicked.connect(self.add_to_cart)
        input_layout.addWidget(QLabel("SKU:"))
        input_layout.addWidget(self.sku_input)
        input_layout.addWidget(QLabel("Qty:"))
        input_layout.addWidget(self.qty_input)
        input_layout.addWidget(self.add_btn)
        layout.addLayout(input_layout)

        # Cart Table
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(4)
        self.cart_table.setHorizontalHeaderLabels(["SKU", "Name", "Price", "Qty"])
        layout.addWidget(self.cart_table)

        # Total & Checkout
        total_layout = QHBoxLayout()
        self.total_label = QLabel("Total: $0.00")
        self.checkout_btn = QPushButton("Checkout")
        self.checkout_btn.clicked.connect(self.checkout)
        total_layout.addWidget(self.total_label)
        total_layout.addWidget(self.checkout_btn)
        layout.addLayout(total_layout)

        self.setLayout(layout)

    def add_to_cart(self):
        sku = self.sku_input.text().strip()
        qty = self.qty_input.value()
        if not sku:
            QMessageBox.warning(self, "Input Error", "Enter SKU")
            return

        self.db.cur.execute("SELECT sku, name, price, stock FROM products WHERE sku=?", (sku,))
        product = self.db.cur.fetchone()
        if not product:
            QMessageBox.warning(self, "Error", "SKU not found")
            return
        if qty > product[3]:
            QMessageBox.warning(self, "Error", f"Only {product[3]} items in stock")
            return

        self.cart.append((product[0], product[1], product[2], qty))
        self.load_cart()
        self.sku_input.clear()
        self.qty_input.setValue(1)

    def calculate_total(self):
        total = sum(price * qty for _, _, price, qty in self.cart)
        discount = total * DISCOUNT_RATE if total > 100 else 0
        tax = (total - discount) * TAX_RATE
        final_total = total - discount + tax
        return final_total, discount, tax

    def load_cart(self):
        self.cart_table.setRowCount(len(self.cart))
        total, discount, tax = self.calculate_total()
        for row_idx, item in enumerate(self.cart):
            sku, name, price, qty = item
            self.cart_table.setItem(row_idx, 0, QTableWidgetItem(sku))
            self.cart_table.setItem(row_idx, 1, QTableWidgetItem(name))
            self.cart_table.setItem(row_idx, 2, QTableWidgetItem(f"${price:.2f}"))
            self.cart_table.setItem(row_idx, 3, QTableWidgetItem(str(qty)))
        self.total_label.setText(f"Total: ${total:.2f} (Discount: ${discount:.2f}, Tax: ${tax:.2f})")

    def checkout(self):
        if not self.cart:
            QMessageBox.warning(self, "Error", "Cart is empty")
            return

        total, discount, tax = self.calculate_total()
        for sku, _, _, qty in self.cart:
            self.db.cur.execute("UPDATE products SET stock = stock - ? WHERE sku=?", (qty, sku))
        self.db.conn.commit()

        QMessageBox.information(self, "Success", f"Transaction Completed!\nTotal: ${total:.2f}\nDiscount: ${discount:.2f}\nTax: ${tax:.2f}")
        self.cart = []
        self.load_cart()
