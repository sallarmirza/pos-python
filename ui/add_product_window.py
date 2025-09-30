import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFormLayout, QSpinBox, QDoubleSpinBox
)
from database.db import Database

class AddProductWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Add Product")
        self.setGeometry(400, 200, 400, 300)

        layout = QFormLayout()

        # Input fields
        self.sku_input = QLineEdit()
        self.name_input = QLineEdit()
        
        self.price_input = QDoubleSpinBox()
        self.price_input.setMaximum(100000)
        self.price_input.setPrefix("$ ")
        self.price_input.setDecimals(2)

        self.stock_input = QSpinBox()
        self.stock_input.setMaximum(100000)

        self.alert_input = QSpinBox()
        self.alert_input.setMaximum(1000)
        self.alert_input.setValue(5)

        # Add product button
        self.add_btn = QPushButton("Add Product")
        self.add_btn.clicked.connect(self.add_product)

        # Add widgets to layout
        layout.addRow("SKU:", self.sku_input)
        layout.addRow("Name:", self.name_input)
        layout.addRow("Price:", self.price_input)
        layout.addRow("Stock:", self.stock_input)
        layout.addRow("Alert Level:", self.alert_input)
        layout.addRow(self.add_btn)

        self.setLayout(layout)

    def add_product(self):
        sku = self.sku_input.text().strip()
        name = self.name_input.text().strip()
        price = self.price_input.value()
        stock = self.stock_input.value()
        alert = self.alert_input.value()

        if not sku or not name:
            QMessageBox.warning(self, "Error", "SKU and Name are required!")
            return

        success = self.db.add_product(sku, name, price, stock, alert)

        if success:
            QMessageBox.information(self, "Success", f"Product '{name}' added successfully!")
            # Clear fields
            self.sku_input.clear()
            self.name_input.clear()
            self.price_input.setValue(0)
            self.stock_input.setValue(0)
            self.alert_input.setValue(5)
        else:
            QMessageBox.warning(self, "Error", "SKU already exists!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddProductWindow()
    window.show()
    sys.exit(app.exec_())
