#!/usr/bin/python3
from collections import deque
from datetime import datetime

class Account:
    def __init__(self, pin, balance):
        self.pin = pin
        self.balance = balance
        self.transactions = deque(maxlen=100)

    def check_pin(self, p):
        return self.pin == p

    def changepin(self, new):
        self.pin = new

    def withdraw(self, amount):
        if amount > self.balance or amount <= 0:
            return False
        self.balance -= amount
        self.transactions.appendleft((datetime.now(), "WITHDRAW", amount))
        return True

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.appendleft((datetime.now(), "DEPOSIT", amount))

    def ministatement(self, n):
        return list(self.transactions)[:n]

