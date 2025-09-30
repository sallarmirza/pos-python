# ui/owner_dashboard.py
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from ui.add_product_window import AddProductWindow
from ui.inventory_window import InventoryWindow  
from ui.manage_cashier_window import ManageCashiersWindow
from ui.manage_cashier_window import ManageCashiersWindow


class OwnerDashboard(QWidget):
    def __init__(self, db, user):
        super().__init__()
        self.db = db
        self.user = user
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Owner Dashboard - {self.user['username']}")
        self.setGeometry(350, 200, 400, 300)

        layout = QVBoxLayout()

        # Add Product
        self.add_product_btn = QPushButton("Add Product")
        self.add_product_btn.clicked.connect(self.open_add_product)
        layout.addWidget(self.add_product_btn)

        # View Inventory
        self.view_inventory_btn = QPushButton("View Inventory")
        self.view_inventory_btn.clicked.connect(self.open_inventory)
        layout.addWidget(self.view_inventory_btn)

        self.setLayout(layout)
        self.manage_cashiers_btn = QPushButton("Manage Cashier Accounts")
        self.manage_cashiers_btn.clicked.connect(self.open_manage_cashiers)
        layout.addWidget(self.manage_cashiers_btn)

    def open_add_product(self):
        self.add_window = AddProductWindow()
        self.add_window.show()

    def open_inventory(self):
        self.inventory_window = InventoryWindow(self.db)
        self.inventory_window.show()
        
    def open_manage_cashiers(self):
        self.cashier_window = ManageCashiersWindow(self.db)
        self.cashier_window.show()
