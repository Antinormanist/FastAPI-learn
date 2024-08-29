import pytest
from cryptography.exceptions import InvalidKey

from app.calcs import add, mul, bebra, Bank, Aboba


@pytest.fixture
def zero_amount():
    return Bank()

@pytest.fixture
def amount():
    return Bank(500)

@pytest.mark.parametrize('a, b, e', [(1, 2, 3), (-1, -2, -3), (7, 4, 11), (4, 4, 8)])
def test_ok(a, b, e):
    assert add(a, b) == e

def test_hyinya():
    assert mul(1, 2) == 2

def test_he():
    assert bebra(1, 2) == 999


def test_bank_set_initial_amount(amount):
    assert amount.cash == 500

def test_bank_deposit(amount):
    amount.deposit(100)
    assert amount.cash == 600

def test_bank_withdraw(amount):
    amount.withdraw(55)
    assert amount.cash == 445

def test_bank_income(amount):
    amount.collect_interest()
    assert amount.cash == 550.00

@pytest.mark.parametrize('minus, plus, exp', [
    (100, 100, 0),
    (0, 555, 555)
])
def test_bank_transaction(zero_amount, minus, plus, exp):
    zero_amount.deposit(plus)
    zero_amount.withdraw(minus)
    assert zero_amount.cash == exp

def test_fail(zero_amount):
    with pytest.raises(Aboba):
        zero_amount.withdraw(1)