from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox,
    QPushButton, QMessageBox
)

class EditProductWindow(QDialog):
    def __init__(self, db, product):
        super().__init__()
        self.db = db
        self.product = product  # (sku, name, price, stock, alert)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Edit Product - {self.product[1]}")

        layout = QFormLayout()

        self.sku = QLineEdit(self.product[0])
        self.sku.setReadOnly(True)

        self.name = QLineEdit(self.product[1])

        self.price = QDoubleSpinBox()
        self.price.setMaximum(100000)
        self.price.setDecimals(2)
        self.price.setValue(self.product[2])

        self.stock = QSpinBox()
        self.stock.setMaximum(100000)
        self.stock.setValue(self.product[3])

        self.alert = QSpinBox()
        self.alert.setMaximum(1000)
        self.alert.setValue(self.product[4])

        save_btn = QPushButton("Save Changes")
        save_btn.clicked.connect(self.save_changes)

        layout.addRow("SKU", self.sku)
        layout.addRow("Name", self.name)
        layout.addRow("Price", self.price)
        layout.addRow("Stock", self.stock)
        layout.addRow("Alert Level", self.alert)
        layout.addRow(save_btn)

        self.setLayout(layout)

    def save_changes(self):
        sku = self.sku.text()
        name = self.name.text().strip()
        price = self.price.value()
        stock = self.stock.value()
        alert = self.alert.value()

        if not name:
            QMessageBox.warning(self, "Error", "Name cannot be empty")
            return

        updated = self.db.update_product(sku, name, price, stock, alert)
        if updated:
            QMessageBox.information(self, "Success", "Product updated successfully!")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Failed to update product")
