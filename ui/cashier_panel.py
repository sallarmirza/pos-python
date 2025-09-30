from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel
)
from database.db import Database

class CashierDashboard(QWidget):
    def __init__(self, db, username):
        super().__init__()
        self.db = db
        self.username = username
        self.cart = []  # list of tuples: (sku, name, price, qty)

        self.setWindowTitle(f"Cashier Dashboard - {username}")
        self.setGeometry(200, 200, 700, 500)

        layout = QVBoxLayout()
        welcome_label = QLabel(f"Welcome, {username} (Cashier)")
        layout.addWidget(welcome_label)

        # Buttons
        self.btn_sale = QPushButton("Start New Sale")
        self.btn_sale.clicked.connect(self.open_sale_window)
        layout.addWidget(self.btn_sale)

        self.btn_search = QPushButton("Search Product / Scan SKU")
        self.btn_receipt = QPushButton("Print Receipt (Coming Soon)")
        self.btn_history = QPushButton("Transaction History")
        self.btn_history.clicked.connect(self.open_transaction_history)  # <--- connect inside class

        layout.addWidget(self.btn_search)
        layout.addWidget(self.btn_receipt)
        layout.addWidget(self.btn_history)

        self.setLayout(layout)

    def open_sale_window(self):
        from ui.sale_window import SaleWindow
        self.sale_window = SaleWindow(self.db)
        self.sale_window.show()

    def open_transaction_history(self):
        from ui.transaction_history_window import TransactionHistoryWindow
        self.trans_window = TransactionHistoryWindow(self.db)
        self.trans_window.show()
