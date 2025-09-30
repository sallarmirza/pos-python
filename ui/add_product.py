from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QSpinBox,
    QPushButton, QHBoxLayout, QMessageBox
)

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

    def add_product(self):
        sku = self.sku.text().strip()
        name = self.name.text().strip()
        try:
            price = float(self.price.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid price value")
            return

        stock = self.stock.value()
        alert = self.alert.value()

        if not sku or not name:
            QMessageBox.warning(self, "Error", "All fields are required")
            return

        if self.db.add_product(sku, name, price, stock, alert):
            QMessageBox.information(self, "Success", "Product added successfully!")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "SKU already exists!")
