from PyQt5.QtWidgets import *
from ui.dashboard import Dashboard
from ui.employees_page import EmployeesPage
from ui.salaries_page import SalariesPage
from ui.leaves_page import LeavesPage
from ui.accounts_page import AccountsPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("porsnel izin ve maaş yönetimi")
        self.resize(1200, 650)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)

        # القائمة الجانبية
        menu = QVBoxLayout()

        # الصفحات (ننشئها مرة واحدة فقط)
        self.dashboard = Dashboard()
        self.employees = EmployeesPage()
        self.salaries = SalariesPage()
        self.leaves = LeavesPage()
        self.accounts = AccountsPage()

        self.stack = QStackedWidget()
        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.employees)
        self.stack.addWidget(self.salaries)
        self.stack.addWidget(self.leaves)
        self.stack.addWidget(self.accounts)

        buttons = [
            ("📊 kontrol paneli", 0),
            ("👨‍💼 çalışanlar", 1),
            ("💰 maaşlar", 2),
            ("🏖 izinler", 3),
            ("📒 hesaplar", 4),
        ]

        for text, index in buttons:
            btn = QPushButton(text)
            btn.setFixedHeight(40)
            btn.clicked.connect(lambda _, i=index: self.change_page(i))
            menu.addWidget(btn)

        menu.addStretch()

        layout.addLayout(menu, 1)
        layout.addWidget(self.stack, 5)

    def change_page(self, index):
        page = self.stack.widget(index)

        # تحديث  حسب الصفحة
        if hasattr(page, "load"):
            page.load()

        if hasattr(page, "load_emps"):
            page.load_emps()

        if hasattr(page, "refresh"):
            page.refresh()

        self.stack.setCurrentIndex(index)
