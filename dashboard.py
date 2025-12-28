from PyQt5.QtWidgets import *
from db.mongo_db import MongoDB

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.db = MongoDB()
        layout = QVBoxLayout(self)

        title = QLabel("📊  kontrol paneli")
        title.setStyleSheet("font-size:22px;font-weight:bold;")
        layout.addWidget(title)

        self.emp = QLabel()
        self.income = QLabel()
        self.expense = QLabel()
        self.balance = QLabel()

        for l in [self.emp, self.income, self.expense, self.balance]:
            l.setStyleSheet("font-size:16px;")
            
            
            layout.addWidget(l)

        self.refresh()

    def refresh(self):
        emp = self.db.employees.count_documents({})
        income = sum(x["amount"] for x in self.db.transactions.find({"type":"giler"}))
        expense = sum(x["amount"] for x in self.db.transactions.find({"type":"gider"}))

        self.emp.setText(f"çalışan sayısı :  {emp}")
        self.income.setText(f"toplam gelir : {income}")
        self.expense.setText(f"toplam gider : {expense}")
        self.balance.setText(f"Bakiye : {income-expense}")
