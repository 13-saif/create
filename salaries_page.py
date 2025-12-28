from PyQt5.QtWidgets import *
from db.mongo_db import MongoDB
from datetime import date

class SalariesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.db = MongoDB()
        layout = QVBoxLayout(self)

        self.combo = QComboBox()
        self.load_emps()

        btn = QPushButton("💰 maaş ödemesi ")
        btn.clicked.connect(self.pay)

        self.table = QTableWidget(0,3)
        self.table.setHorizontalHeaderLabels(
            ["çalışan","amount","date"]
        )

        layout.addWidget(self.combo)
        layout.addWidget(btn)
        layout.addWidget(self.table)

        self.load()

    def load_emps(self):
        self.emps = list(self.db.employees.find())
        self.combo.clear()
        for e in self.emps:
            self.combo.addItem(e["name"])

    def pay(self):
        emp = self.emps[self.combo.currentIndex()]
        today = str(date.today())

        if self.db.salaries.find_one(
            {"emp_id": emp["_id"], "date": today}
        ):
            QMessageBox.warning(self,"uyarı",
                "Bu çalışanın maaşı bugün ödendi")
            return

        self.db.salaries.insert_one({
            "emp_id": emp["_id"],
            "name": emp["name"],
            "amount": emp["salary"],
            "date": today
        })

        self.db.transactions.insert_one({
            "type":"gelir",
            "amount": emp["salary"],
            "desc": f"maaş {emp['name']}",
            "date": today
        })

        self.db.employees.update_one(
            {"_id": emp["_id"]},
            {"$set":{"last_salary":today}}
        )

        self.load()

    def load(self):
        self.table.setRowCount(0)
        for s in self.db.salaries.find():
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setItem(r,0,QTableWidgetItem(s["name"]))
            self.table.setItem(r,1,QTableWidgetItem(str(s["amount"])))
            self.table.setItem(r,2,QTableWidgetItem(s["date"]))
