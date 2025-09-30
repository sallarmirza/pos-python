from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class ReceiptWindow(QWidget):
    def __init__(self, cart, total, discount, tax):
        super().__init__()
        self.cart = cart
        self.total = total
        self.discount = discount
        self.tax = tax

        self.setWindowTitle("Receipt")
        self.setGeometry(400, 200, 400, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)

        self.save_btn = QPushButton("Save Receipt")
        self.save_btn.clicked.connect(self.save_receipt)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)
        self.generate_receipt_text()

    def generate_receipt_text(self):
        lines = []
        lines.append("======== STORE RECEIPT ========")
        lines.append("Items:")
        lines.append(f"{'SKU':<10}{'Name':<20}{'Qty':<5}{'Price':<10}")
        for sku, name, price, qty in self.cart:
            lines.append(f"{sku:<10}{name:<20}{qty:<5}${price*qty:<10.2f}")
        lines.append("------------------------------")
        lines.append(f"Discount: ${self.discount:.2f}")
        lines.append(f"Tax: ${self.tax:.2f}")
        lines.append(f"TOTAL: ${self.total:.2f}")
        lines.append("==============================")
        self.text_area.setText("\n".join(lines))

    def save_receipt(self):
        try:
            with open("receipt.txt", "w") as f:
                f.write(self.text_area.toPlainText())
            QMessageBox.information(self, "Saved", "Receipt saved as receipt.txt")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not save receipt: {str(e)}")
