from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox,
    QPushButton, QHBoxLayout, QMessageBox
)
from database.db import Database


class LoginDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Login")
        self.resize(300, 150)

        layout = QFormLayout()

        # Inputs
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.role = QComboBox()
        self.role.addItems(["owner", "cashier"])

        layout.addRow("Username", self.username)
        layout.addRow("Password", self.password)
        layout.addRow("Role", self.role)

        # Buttons
        btn_layout = QHBoxLayout()
        login_btn = QPushButton("Login")
        cancel_btn = QPushButton("Cancel")

        login_btn.clicked.connect(self.try_login)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(login_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow(btn_layout)

        self.setLayout(layout)
        self.user = None

    def try_login(self):
        u = self.username.text().strip()
        p = self.password.text().strip()
        r = self.role.currentText()

        row = self.db.auth_user(u, p, r)
        if row:
            self.user = {"username": row[1], "role": row[3]}
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid credentials")
