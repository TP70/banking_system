import Database
import NewAccount


class Account:
    def __init__(self, first_name: str, last_name: str, gender: str, ask_income: int, current_balance: int,
                 set_overdraft: int, defined_password: str):
        self._user_first_name = first_name
        self._user_last_name = last_name
        self._user_gender = gender
        self._income = ask_income
        self._balance = current_balance
        self._OVERDRAFT_LIMIT = set_overdraft
        self._overdraft_balance = set_overdraft
        self._password = defined_password

    @property
    def get_loans(self):
        return self._get_loans

    @get_loans.setter
    def get_loans(self, value):
        self._get_loans = value

    @property
    def overdraft_limit(self):
        return self._OVERDRAFT_LIMIT

    @property
    def overdraft_balance(self):
        return self._overdraft_balance

    @overdraft_balance.setter
    def overdraft_balance(self, value):
        self._overdraft_balance = value

    @property
    def income(self):
        return self._income

    @property
    def user_full_name(self):
        return self._user_first_name + ' ' + self._user_last_name

    @property
    def user_last_name(self):
        return self._user_last_name

    @property
    def password(self):
        return self._password

    @property
    def account_number(self):
        return self._account_number

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        self._balance = value


