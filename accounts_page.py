from PyQt5.QtWidgets import *
from db.mongo_db import MongoDB
from datetime import date

class AccountsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.db = MongoDB()
        layout = QVBoxLayout(self)

        self.type = QComboBox()
        self.type.addItems(["giler","gider"])
        self.amount = QLineEdit()
        self.desc = QLineEdit()

        btn = QPushButton("➕")
        btn.clicked.connect(self.add)

        self.table = QTableWidget(0,4)
        self.table.setHorizontalHeaderLabels(
            ["type","amount","desc","date"]
        )

        layout.addWidget(self.type)
        layout.addWidget(self.amount)
        layout.addWidget(self.desc)
        layout.addWidget(btn)
        layout.addWidget(self.table)

        self.load()

    def add(self):
        self.db.transactions.insert_one({
            "type": self.type.currentText(),
            "amount": float(self.amount.text()),
            "desc": self.desc.text(),
            "date": str(date.today())
        })
        self.load()

    def load(self):
        self.table.setRowCount(0)
        for t in self.db.transactions.find():
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setItem(r,0,QTableWidgetItem(t["type"]))
            self.table.setItem(r,1,QTableWidgetItem(str(t["amount"])))
            self.table.setItem(r,2,QTableWidgetItem(t["desc"]))
            self.table.setItem(r,3,QTableWidgetItem(t["date"]))
