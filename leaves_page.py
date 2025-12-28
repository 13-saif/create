from PyQt5.QtWidgets import *
from db.mongo_db import MongoDB

class LeavesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.db = MongoDB()
        layout = QVBoxLayout(self)

        self.combo = QComboBox()
        self.load_emps()

        self.f = QLineEdit()
        self.t = QLineEdit()

        btn = QPushButton("➕  izin ekle")
        btn.clicked.connect(self.add)

        self.table = QTableWidget(0,4)
        self.table.setHorizontalHeaderLabels(
            ["employee","from","to","status"]
        )

        layout.addWidget(self.combo)
        layout.addWidget(self.f)
        layout.addWidget(self.t)
        layout.addWidget(btn)
        layout.addWidget(self.table)

        self.load()

    def load_emps(self):
        self.emps = list(self.db.employees.find())
        self.combo.clear()
        for e in self.emps:
            self.combo.addItem(e["name"])

    def add(self):
        emp = self.emps[self.combo.currentIndex()]
        self.db.leaves.insert_one({
            "emp_id": emp["_id"],
            "name": emp["name"],
            "from": self.f.text(),
            "to": self.t.text(),
            "status":"Approval"
        })
        self.load()

    def load(self):
        self.table.setRowCount(0)
        for l in self.db.leaves.find():
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setItem(r,0,QTableWidgetItem(l["name"]))
            self.table.setItem(r,1,QTableWidgetItem(l["from"]))
            self.table.setItem(r,2,QTableWidgetItem(l["to"]))
            self.table.setItem(r,3,QTableWidgetItem(l["status"]))
