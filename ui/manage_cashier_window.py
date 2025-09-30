from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from database.db import Database

class ManageCashiersWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Manage Cashier Accounts")
        self.setGeometry(450, 250, 500, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input fields for new cashier
        input_layout = QHBoxLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.add_btn = QPushButton("Add Cashier")
        self.add_btn.clicked.connect(self.add_cashier)

        input_layout.addWidget(self.username_input)
        input_layout.addWidget(self.password_input)
        input_layout.addWidget(self.add_btn)

        layout.addLayout(input_layout)

        # Table to display cashiers
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "Username"])
        layout.addWidget(self.table)

        # Delete button
        self.delete_btn = QPushButton("Delete Selected Cashier")
        self.delete_btn.clicked.connect(self.delete_cashier)
        layout.addWidget(self.delete_btn)

        self.setLayout(layout)
        self.load_cashiers()

    def load_cashiers(self):
        cashiers = self.db.get_cashiers()
        self.table.setRowCount(len(cashiers))
        for row_idx, cashier in enumerate(cashiers):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(cashier[0])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(cashier[1]))

    def add_cashier(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password")
            return

        success = self.db.add_user(username, password, "cashier")
        if success:
            QMessageBox.information(self, "Success", "Cashier added successfully!")
            self.username_input.clear()
            self.password_input.clear()
            self.load_cashiers()
        else:
            QMessageBox.warning(self, "Error", "Username already exists")

    def delete_cashier(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a cashier to delete")
            return
        cashier_id = int(self.table.item(selected_row, 0).text())
        confirm = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this cashier?")
        if confirm == QMessageBox.Yes:
            self.db.delete_cashier(cashier_id)
            QMessageBox.information(self, "Deleted", "Cashier deleted successfully")
            self.load_cashiers()
