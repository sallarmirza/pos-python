def add_transaction(self, cashier, items, discount=0, tax=0):
    """
    items: list of tuples (sku, name, price, qty)
    """
    total = sum(price * qty for _, _, price, qty in items)
    total_after = total - discount + tax
    self.cur.execute(
        "INSERT INTO transactions(cashier, total, discount, tax) VALUES (?, ?, ?, ?)",
        (cashier, total_after, discount, tax)
    )
    transaction_id = self.cur.lastrowid

    for sku, name, price, qty in items:
        self.cur.execute(
            "INSERT INTO transaction_items(transaction_id, sku, name, price, quantity) VALUES (?, ?, ?, ?, ?)",
            (transaction_id, sku, name, price, qty)
        )
        # Update inventory
        self.cur.execute(
            "UPDATE products SET stock = stock - ? WHERE sku=?",
            (qty, sku)
        )
    self.conn.commit()
    return transaction_id
