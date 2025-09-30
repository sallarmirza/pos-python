from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QColor
from ui.edit_product_window import EditProductWindow
from database.db import Database

class InventoryWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Inventory")
        self.setGeometry(450, 250, 700, 500)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["SKU", "Name", "Price", "Stock", "Alert Level"])
        layout.addWidget(self.table)

        # Buttons
        btn_layout = QHBoxLayout()
        self.edit_btn = QPushButton("Edit Product")
        self.delete_btn = QPushButton("Delete Product")

        self.edit_btn.clicked.connect(self.edit_product)
        self.delete_btn.clicked.connect(self.delete_product)

        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        self.table.setRowCount(0)
        products = self.db.get_all_products()
        for row_num, product in enumerate(products):
            # product is (id, sku, name, price, stock, alert_level)
            _id, sku, name, price, stock, alert = product

            self.table.insertRow(row_num)
            self.table.setItem(row_num, 0, QTableWidgetItem(sku))
            self.table.setItem(row_num, 1, QTableWidgetItem(name))
            self.table.setItem(row_num, 2, QTableWidgetItem(f"{price:.2f}"))
            self.table.setItem(row_num, 3, QTableWidgetItem(str(stock)))
            self.table.setItem(row_num, 4, QTableWidgetItem(str(alert)))

    def get_selected_product(self):
        row = self.table.currentRow()
        if row == -1:
            return None
        return (
            self.table.item(row, 0).text(),   # SKU
            self.table.item(row, 1).text(),   # Name
            float(self.table.item(row, 2).text().replace("$", "")), # Price
            int(self.table.item(row, 3).text()), # Stock
            int(self.table.item(row, 4).text())  # Alert Level
        )

    def edit_product(self):
        product = self.get_selected_product()
        if not product:
            QMessageBox.warning(self, "Error", "Select a product to edit")
            return

        dialog = EditProductWindow(self.db, product)
        if dialog.exec_():
            self.load_data()  # Refresh after update

    def delete_product(self):
        product = self.get_selected_product()
        if not product:
            QMessageBox.warning(self, "Error", "Select a product to delete")
            return

        sku = product[0]
        confirm = QMessageBox.question(
            self, "Confirm Delete", f"Are you sure you want to delete SKU {sku}?"
        )
        if confirm == QMessageBox.Yes:
            deleted = self.db.delete_product(sku)
            if deleted:
                QMessageBox.information(self, "Deleted", "Product deleted successfully")
                self.load_data()
            else:
                QMessageBox.warning(self, "Error", "Failed to delete product")
