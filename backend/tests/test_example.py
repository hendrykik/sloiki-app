import pytest
from sqlalchemy.sql.functions import user


def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1

class Student:
    def __init__(self, username: str, password: str, number: int):
        self.username =username
        self.password = password
        self.number = number

@pytest.fixture
def default_employee():
     return Student('jan', 'bart', 23)

def test_student(default_employee):
    assert default_employee.username == 'jan', 'imie'
    assert default_employee.password == 'bart', 'haslo'
    assert default_employee.number == 23, 'numer'
