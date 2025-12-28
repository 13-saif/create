from pymongo import MongoClient

class MongoDB:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["personel"]

        self.employees = self.db.employees
        self.salaries = self.db.salaries
        self.leaves = self.db.leaves
        self.transactions = self.db.transactions
