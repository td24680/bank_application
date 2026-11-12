from datetime import datetime

class Customer:
    last_id = 0
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        Customer.last_id = Customer.last_id + 1
        self.id = Customer.last_id

    def __repr__(self):
        return f"C({self.id}, {self.first_name}, {self.last_name})"

class Account:
    last_id = 1000
    yearly_interest_rate = 0.02  # TODO - will be used to update the interest rate

    def __init__(self, customer, currency='PLN'):
        self.customer = customer
        self._balance = 0
        Account.last_id += 1
        self.id = Account.last_id
        self.currency = currency
        self.transactions = []

    def deposit(self, amount, transaction_type = 'DEPOSIT', related_account_id=None):
        # TODO - as part of the home assignment please extend this method
        if type(amount) not in (int, float) or not 0 < amount < float("inf"):
            raise BankException("Invalid amount")
        new_balance = self._balance + amount
        if not new_balance < float('inf'):
            raise BankException("Balance overflow")
        self._balance = new_balance
        self.transactions.append(AccountTransaction(transaction_type, amount, self._balance, related_account_id))
        print(f"Deposited {amount} to {self}")

    # code for creating withdraw method
    def withdraw(self, amount, transaction_type='WITHDRAW', related_account_id=None):
        # TODO - as part of the home assignment please extend this method
        if type(amount) not in (int, float) or not 0 < amount < float("inf"):
            raise BankException("Invalid amount")
        if amount > self._balance:
            raise InsufficientBalanceException("Insufficient balance")
        self._balance -= amount
        self.transactions.append(AccountTransaction(transaction_type, amount, self._balance, related_account_id))
        print(f"Withdrew {amount} from {self}")

    def __repr__(self):
        return f"A({self.id}, {self.customer.last_name}, {self._balance:.2f} {self.currency})"


class Bank:
    def __init__(self, name):
        self.name = name
        self.customers = []
        self.accounts = []

    def create_customer(self, first_name, last_name):
        customer = Customer(first_name, last_name)
        self.customers.append(customer)
        return customer

    def create_account(self, customer, currency = 'PLN'):
        account = Account(customer, currency)
        self.accounts.append(account)
        return account

    def find_account(self, account_id):
        for account in self.accounts:
            if account.id == account_id:
                return account
        return None

    def transfer_money(self, from_account_id, to_account_id, amount):
        # TODO - as part of the home assignment please implement this method - as names suggest the input parameters are
        # ids of the accounts to transfer money from and to and amount to transfer. You may need a helper method to find
        # those accounts based on their ids.
        if type(from_account_id) != int or type(to_account_id) != int:
            raise BankException("Invalid Account ID")

        if from_account_id == to_account_id:
            raise BankException("Cannot transfer money to the same account")

        from_account = self.find_account(from_account_id)
        to_account = self.find_account(to_account_id)

        if from_account is None or to_account is None:
            raise BankException("Account not found")

        if from_account.currency != to_account.currency:
            raise BankException("Incorrect currency")

        if type(amount) not in (int, float) or not 0 < amount < float("inf"):
            raise BankException("Invalid amount")

        if amount > from_account._balance:
            raise InsufficientBalanceException("Insufficient balance")

        if not to_account._balance + amount < float("inf"):
            raise BankException("Balance overflow")

        from_account.withdraw(amount, "TRANSFER_OUT", to_account_id)
        to_account.deposit(amount, "TRANSFER_IN", from_account_id)

    def run_daily_interest_updater(self):
        # TODO - as part of the home assignment please implement this method
        for account in self.accounts:
            interest = account._balance * account.yearly_interest_rate/365
            new_balance = account._balance + interest

            if not new_balance < float("inf"):
                raise BankException("Balance overflow")

            account._balance = new_balance
            account.transactions.append(AccountTransaction("INTEREST", interest, account._balance))

    def __repr__(self):
        return f"B({self.name}, \n{self.customers}, \n{self.accounts})"

class BankException(Exception):
    pass

class InsufficientBalanceException(BankException):
    pass

class AccountTransaction:
    def __init__(self, transaction_type, amount, balance, related_account_id=None):
        self.transaction_type = transaction_type
        self.amount = amount
        self.balance = balance
        self.related_account_id = related_account_id
        self.timestamp = datetime.now()

    def __repr__(self):
        details = f"{self.timestamp} | {self.transaction_type} | {self.amount:.2f} | Balance: {self.balance:.2f}"
        if self.related_account_id is not None:
            details += f" | Related Account ID: {self.related_account_id}"
        return details