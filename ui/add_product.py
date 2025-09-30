from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QSpinBox,
    QPushButton, QHBoxLayout, QMessageBox
)
import sqlite3

class AddProductDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Add Product")
        self.resize(300, 250)

        layout = QFormLayout()

        self.sku = QLineEdit()
        self.name = QLineEdit()
        self.price = QLineEdit()
        self.stock = QSpinBox()
        self.stock.setRange(0, 10000)

        self.alert = QSpinBox()
        self.alert.setRange(1, 1000)
        self.alert.setValue(5)

        layout.addRow("SKU", self.sku)
        layout.addRow("Name", self.name)
        layout.addRow("Price", self.price)
        layout.addRow("Stock", self.stock)
        layout.addRow("Alert Level", self.alert)

        # Buttons
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add")
        cancel_btn = QPushButton("Cancel")

        add_btn.clicked.connect(self.add_product)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow(btn_layout)

        self.setLayout(layout)

def add_product(self, sku, name, price, stock, alert_level=5):
    try:
        self.cur.execute(
            "INSERT INTO products(sku, name, price, stock, alert_level) VALUES (?, ?, ?, ?, ?)",
            (sku, name, price, stock, alert_level)
        )
        self.conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
