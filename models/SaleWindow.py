from ui.receipt_window import ReceiptWindow


def checkout(self):
    if not self.cart:
        QMessageBox.warning(self, "Error", "Cart is empty")
        return

    total, discount, tax = self.calculate_total()

    # Update stock
    for sku, _, _, qty in self.cart:
        self.db.cur.execute("UPDATE products SET stock = stock - ? WHERE sku=?", (qty, sku))
    self.db.conn.commit()

    # Show receipt
    self.receipt_window = ReceiptWindow(self.cart, total, discount, tax)
    self.receipt_window.show()

    # Clear cart
    self.cart = []
    self.load_cart()
