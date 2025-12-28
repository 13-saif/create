from PyQt5.QtWidgets import *
from db.mongo_db import MongoDB

class EmployeesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.db = MongoDB()
        layout = QVBoxLayout(self)

        form = QFormLayout()
        self.name = QLineEdit()
        self.job = QLineEdit()
        self.salary = QLineEdit()

        btn_add = QPushButton("➕ ")
        btn_add.clicked.connect(self.add_emp)

        form.addRow("isim", self.name)
        form.addRow("meslek", self.job)
        form.addRow("maaş", self.salary)
        form.addRow(btn_add)

        self.table = QTableWidget(0,4)
        self.table.setHorizontalHeaderLabels(
            ["isim","meslek","maaş","tarih ödeme"]
        )

        btn_del = QPushButton("🗑 sil")
        btn_del.clicked.connect(self.delete_emp)

        layout.addLayout(form)
        layout.addWidget(self.table)
        layout.addWidget(btn_del)

        self.load()

    def add_emp(self):
        self.db.employees.insert_one({
            "name": self.name.text(),
            "job": self.job.text(),
            "salary": float(self.salary.text()),
            "last_salary": ""
        })
        self.load()

    def delete_emp(self):
        row = self.table.currentRow()
        if row >= 0:
            name = self.table.item(row,0).text()
            self.db.employees.delete_one({"name":name})
            self.load()

    def load(self):
        self.table.setRowCount(0)
        for e in self.db.employees.find():
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setItem(r,0,QTableWidgetItem(e["name"]))
            self.table.setItem(r,1,QTableWidgetItem(e["job"]))
            self.table.setItem(r,2,QTableWidgetItem(str(e["salary"])))
            self.table.setItem(r,3,QTableWidgetItem(e["last_salary"]))
