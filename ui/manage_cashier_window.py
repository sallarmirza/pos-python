from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QLabel, QTableWidget, QTableWidgetItem,
    QMessageBox
)
from database.db import Database

class ManageCashiersWindow(QWidget):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.setWindowTitle("Manage Cashiers")
        self.setGeometry(200, 200, 500, 400)

        self.init_ui()
        self.load_cashiers()

    def init_ui(self):
        layout = QVBoxLayout()

        # Table to display cashiers
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "Username"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # Add cashier section
        add_layout = QHBoxLayout()
        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Enter cashier username")
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Enter password")
        self.input_password.setEchoMode(QLineEdit.Password)
        self.btn_add = QPushButton("Add Cashier")
        self.btn_add.clicked.connect(self.add_cashier)

        add_layout.addWidget(QLabel("Username:"))
        add_layout.addWidget(self.input_username)
        add_layout.addWidget(QLabel("Password:"))
        add_layout.addWidget(self.input_password)
        add_layout.addWidget(self.btn_add)
        layout.addLayout(add_layout)

        # Delete selected cashier
        self.btn_delete = QPushButton("Delete Selected Cashier")
        self.btn_delete.clicked.connect(self.delete_cashier)
        layout.addWidget(self.btn_delete)

        self.setLayout(layout)

    def load_cashiers(self):
        self.table.setRowCount(0)
        cashiers = self.db.get_cashiers()
        for row_num, (cashier_id, username) in enumerate(cashiers):
            self.table.insertRow(row_num)
            self.table.setItem(row_num, 0, QTableWidgetItem(str(cashier_id)))
            self.table.setItem(row_num, 1, QTableWidgetItem(username))

    def add_cashier(self):
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "Error", "Username and password are required")
            return

        success = self.db.add_user(username, password, "cashier")
        if success:
            QMessageBox.information(self, "Success", f"Cashier '{username}' added!")
            self.input_username.clear()
            self.input_password.clear()
            self.load_cashiers()
        else:
            QMessageBox.warning(self, "Error", "Username already exists")

    def delete_cashier(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Error", "Select a cashier to delete")
            return
        cashier_id = int(self.table.item(selected, 0).text())
        confirm = QMessageBox.question(
            self, "Confirm Delete", "Are you sure you want to delete this cashier?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            if self.db.delete_cashier(cashier_id):
                QMessageBox.information(self, "Deleted", "Cashier deleted successfully")
                self.load_cashiers()
            else:
                QMessageBox.warning(self, "Error", "Failed to delete cashier")
