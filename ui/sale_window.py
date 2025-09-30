from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QSpinBox,
    QMessageBox
)
from PyQt5.QtCore import Qt

class SaleWindow(QWidget):
    def __init__(self, db, cashier_name):
        super().__init__()
        self.db = db
        self.cashier_name = cashier_name
        self.cart = []  # List of tuples: (sku, name, price, qty)

        self.setWindowTitle("New Sale")
        self.setGeometry(250, 250, 800, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Product entry
        product_layout = QHBoxLayout()
        self.sku_input = QLineEdit()
        self.sku_input.setPlaceholderText("Enter SKU")
        self.qty_input = QSpinBox()
        self.qty_input.setRange(1, 1000)
        add_btn = QPushButton("Add to Cart")
        add_btn.clicked.connect(self.add_to_cart)

        product_layout.addWidget(QLabel("SKU:"))
        product_layout.addWidget(self.sku_input)
        product_layout.addWidget(QLabel("Qty:"))
        product_layout.addWidget(self.qty_input)
        product_layout.addWidget(add_btn)
        layout.addLayout(product_layout)

        # Cart table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["SKU", "Name", "Price", "Quantity"])
        layout.addWidget(self.table)

        # Discount, Tax, Total
        self.discount_input = QLineEdit("0")
        self.tax_input = QLineEdit("0")
        self.total_label = QLabel("Total: 0.00")

        layout.addWidget(QLabel("Discount:"))
        layout.addWidget(self.discount_input)
        layout.addWidget(QLabel("Tax:"))
        layout.addWidget(self.tax_input)
        layout.addWidget(self.total_label)

        # Finalize Sale button
        finalize_btn = QPushButton("Finalize Sale")
        finalize_btn.clicked.connect(self.finalize_sale)
        layout.addWidget(finalize_btn)

        self.setLayout(layout)

    def add_to_cart(self):
        sku = self.sku_input.text().strip()
        qty = self.qty_input.value()

        if not sku:
            QMessageBox.warning(self, "Error", "SKU cannot be empty")
            return

        # Fetch product from database
        products = self.db.get_all_products()
        product = next((p for p in products if p[1] == sku), None)

        if not product:
            QMessageBox.warning(self, "Error", "Product not found")
            return

        if qty > product[4]:
            QMessageBox.warning(self, "Error", f"Only {product[4]} items in stock")
            return

        # Add to cart
        self.cart.append((product[1], product[2], product[3], qty))
        self.refresh_cart()

    def refresh_cart(self):
        self.table.setRowCount(len(self.cart))
        total = 0
        for row, (sku, name, price, qty) in enumerate(self.cart):
            self.table.setItem(row, 0, QTableWidgetItem(sku))
            self.table.setItem(row, 1, QTableWidgetItem(name))
            self.table.setItem(row, 2, QTableWidgetItem(f"{price:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(str(qty)))
            total += price * qty

        try:
            discount = float(self.discount_input.text())
        except:
            discount = 0
        try:
            tax = float(self.tax_input.text())
        except:
            tax = 0

        self.total_label.setText(f"Total: {total - discount + tax:.2f}")

    def finalize_sale(self):
        if not self.cart:
            QMessageBox.warning(self, "Error", "Cart is empty")
            return

        try:
            discount = float(self.discount_input.text())
        except:
            discount = 0
        try:
            tax = float(self.tax_input.text())
        except:
            tax = 0

        transaction_id = self.db.add_transaction(self.cashier_name, self.cart, discount, tax)
        if transaction_id:
            QMessageBox.information(self, "Success", f"Sale completed. Transaction ID: {transaction_id}")
            self.cart.clear()
            self.refresh_cart()
        else:
            QMessageBox.warning(self, "Error", "Failed to record transaction")
