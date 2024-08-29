def add(a: int, b: int) -> int:
    return a + b


def mul(a: int, b: int) -> int:
    return a * b


def bebra(a, b):
    return 999

class Aboba(Exception):
    pass

class Bank:
    def __init__(self, amount=0):
        self.cash = amount


    def deposit(self, amount):
        self.cash += amount

    def withdraw(self, amount):
        if self.cash >= amount:
            self.cash -= amount
        else:
            raise Aboba('you don\'t have such money')

    def collect_interest(self):
        self.cash *= 1.1