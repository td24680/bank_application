from bank import Customer, Account, Bank, InsufficientBalanceException, BankException

# Create bank, customers and accounts
b = Bank('SGH Bank')
c1 = b.create_customer('John', 'Smith')
c2 = b.create_customer('Anne', 'Brown')
a1 = b.create_account(c1, 'USD')
a2 = b.create_account(c2, 'USD')
a3 = b.create_account(c1, 'USD')
a4 = b.create_account(c2, 'USD')
print(b)

# Task 1: Deposit and withdraw
a1.deposit(200)
a1.withdraw(100)

# Test insufficient balance
try:
    a1.withdraw(300)
except InsufficientBalanceException as e:
    print(e)

# Test negative deposit:
try:
    a1.deposit(-100)
except BankException as e:
    print(e)

# Test negative withdraw:
try:
    a1.withdraw(-100)
except BankException as e:
    print(e)

# Task 2: Transfer money
a1.deposit(200)
b.transfer_money(a1.id, a2.id, 100)

print("\nAfter transfer:")
print(b)

# Test transfer to the same account
try:
    b.transfer_money(a1.id, a1.id, 100)
except BankException as e:
    print(e)

# Test transfer to a non-existing account
try:
    b.transfer_money(a1.id, 9999, 100)
except BankException as e:
    print(e)

# Test transfer with insufficient balance
try:
    b.transfer_money(a1.id, a2.id, 999999)
except InsufficientBalanceException as e:
    print(e)

# Task 3: Simulate daily interest for 3 days
a1.deposit(10000)

for day in range(1, 4):
    b.run_daily_interest_updater()
    print(f"Day {day}: {a1}")

# Task 4: Transaction history
a1.deposit(500)
a1.withdraw(100)
b.transfer_money(a1.id, a2.id, 200)
b.run_daily_interest_updater()

for account in [a1, a2]:
    print(f"\nAccount {account.id} - {account.customer.first_name} {account.customer.last_name}")
    for transaction in account.transactions:
        print(transaction)

# Task 5: Bank state
print(b)