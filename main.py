import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from database.db import Database
from ui.login import LoginDialog
from ui.owner_panel import OwnerDashboard
from ui.cashier_panel import CashierDashboard

def main():
    app = QApplication(sys.argv)

    db = Database()
    login = LoginDialog(db)

    if login.exec_() == LoginDialog.Accepted:
        user = login.user
        role = user['role']

        # Redirect based on role
        if role == "owner":
            dashboard = OwnerDashboard(db,user)
            dashboard.show()
        else:
            dashboard = CashierDashboard(db,user['username'])

        dashboard.show()
        app.exec_()
    else:
        QMessageBox.information(None, "Exit", "Application closed.")

    db.close()
    sys.exit()

if __name__ == "__main__":
    main()
