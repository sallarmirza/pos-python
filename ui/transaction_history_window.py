from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
import json

class TransactionHistoryWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Transaction History")
        self.setGeometry(400, 200, 600, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Date/Time", "Items", "Subtotal", "Discount", "Total"])
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.load_transactions()

    def load_transactions(self):
        self.db.cur.execute("SELECT date_time, items, subtotal, discount, total FROM transactions ORDER BY id DESC")
        transactions = self.db.cur.fetchall()
        self.table.setRowCount(len(transactions))
        for row_idx, trans in enumerate(transactions):
            date_time, items_json, subtotal, discount, total = trans
            items_list = json.loads(items_json)
            items_str = ", ".join([f"{name}({qty})" for _, name, _, qty in items_list])
            self.table.setItem(row_idx, 0, QTableWidgetItem(date_time))
            self.table.setItem(row_idx, 1, QTableWidgetItem(items_str))
            self.table.setItem(row_idx, 2, QTableWidgetItem(f"${subtotal:.2f}"))
            self.table.setItem(row_idx, 3, QTableWidgetItem(f"${discount:.2f}"))
            self.table.setItem(row_idx, 4, QTableWidgetItem(f"${total:.2f}"))
