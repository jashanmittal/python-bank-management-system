import time
import datetime
import json
import random

accounts = []


def save():
    data = []

    for acc in accounts:
        data.append({
            "name": acc.name,
            "password": acc.password,
            "acc_num": acc.acc_num,
            "balance": acc.balance,
            "transactions": acc.transactions
        })

    with open("bank.json", "w") as file:
        json.dump(data, file, indent=4)


def load():
    global accounts

    try:
        with open("bank.json", "r") as file:
            data = json.load(file)

        accounts = []

        for item in data:
            acc = Account(
                item["name"],
                item["password"],
                item["acc_num"],
                item["balance"]
            )
            acc.transactions = item["transactions"]
            accounts.append(acc)

    except FileNotFoundError:
        accounts = []

    except json.JSONDecodeError:
        accounts = []


class Account():
    def __init__(self, name="", password="", acc_num=0, balance=0):
        self.transactions = []
        self.balance = balance
        self.name = name
        self.password = password
        self.acc_num = acc_num

    def create_acc(self):
        self.name = input("Enter the name: ")
        self.password = input("Enter the password: ")
        while True:
            number = random.randint(1000, 9999)

            found = False
            for acc in accounts:
                if acc.acc_num == number:
                    found = True
                    break

            if not found:
                self.acc_num = number
                break
        print(f"Your Account Number is {self.acc_num}")
        time.sleep(1)


    def login(self):
        login_password = input("Enter the password: ")
        
        if login_password == self.password:
            print("Successfully Logged In")
            time.sleep(1)
            return True
        else:
            print("Invalid Login Details")
            time.sleep(1)
            return False
    
    def change_password(self):
        new_pass = (input("Enter the new password: "))
        self.password = new_pass
        print("Password Successfully Changed!")
        save()
        time.sleep(1)

    
def menu():
    load()
    while True:
        print("Which feature would you like to use: ")
        print("1. Create Account\n" \
        "2. Login\n" \
        "3. Exit")
        try:
            choice = int(input())
        except ValueError:
            print("Please enter a number.")
            time.sleep(1)
            continue

        if choice == 1:
            new_acc = Account()
            new_acc.create_acc()
            accounts.append(new_acc)
            save()

        elif choice == 2:
            try:
                acc_num = int(input("Enter Account Number: "))
            except ValueError:
                print("Please enter a valid account number.")
                time.sleep(1)
                continue
            found = False

            for acc in accounts:
                if acc.acc_num == acc_num:
                    found = True
                    if acc.login():
                        main(acc)
                    break

            if not found:
                print("Account Not Found")
                time.sleep(1)

        elif choice == 3:
            exit()
        
        else:
            print("Invalid Command")
            time.sleep(1)


def transfer(current_account):
    try:
        rec_acc_num = int(input("Enter Reciever's Account Number: "))
    except ValueError:
            print("Please enter a number.")
            time.sleep(1)
            return

    if rec_acc_num == current_account.acc_num:
        print("You cannot transfer money to yourself.")
        return
    
    found = False

    for acc in accounts:
        if acc.acc_num == rec_acc_num:
            found = True
            amount = float(input("Enter Amount To Transfer: "))
            if amount > current_account.balance:
                print("Insufficient Balance")
                return
            current_account.balance -= amount
            acc.balance += amount
            current_account.transactions.append(f"Transfered {amount} to {acc.name} on {datetime.datetime.now()}")
            acc.transactions.append(f"Recieved {amount} from {current_account.name} on {datetime.datetime.now()}")
            print(f"{amount} successfully transfered to {rec_acc_num}")
            save()
            time.sleep(1)
            break

    if not found:
        print("Account Number Not Found")


def main(current_account):
    while True:
        print("Which feature would you like to use: ")
        print("1. Deposit\n" \
        "2. Withdraw\n" \
        "3. Check Balance\n" \
        "4. Transfer Money\n" \
        "5. Check Account Details\n" \
        "6. Check Transactions\n" \
        "7. Change Password\n" \
        "8. Logout")

        try:
            choice = int(input())
        except ValueError:
            print("Please enter a number.")
            time.sleep(1)
            continue

        if choice == 1:
            deposit_amount = float(input("Enter amount to deposit: "))

            if deposit_amount > 0:
                current_account.balance += deposit_amount
                current_account.transactions.append(f"Deposited {deposit_amount} on {datetime.datetime.now()}")
                print(f"Successfully deposited {deposit_amount} to account")
                save()
                time.sleep(1)
            else:
                print("Enter valid amount")
                time.sleep(1)

        elif choice == 2:
            withdraw_amount = float(input("Enter amount to withdraw: "))

            if 0 < withdraw_amount <= current_account.balance:
                current_account.balance -= withdraw_amount
                current_account.transactions.append(f"Withdrawn {withdraw_amount} on {datetime.datetime.now()}")
                print(f"Successfully withdrawn {withdraw_amount} from account")
                save()
                time.sleep(1)
            else:
                print("Enter valid amount")
                time.sleep(1)

        elif choice == 3:
            print(f"Your balance is {current_account.balance}")
            time.sleep(1)

        elif choice == 4:
            transfer(current_account)

        elif choice == 5:
            print(f"""
--------------------------------------------------------
Name : {current_account.name}
Password : {current_account.password}
Account Number : {current_account.acc_num}
--------------------------------------------------------""")
            time.sleep(1)

        elif choice == 6:
            if not current_account.transactions:
                print("No Transactions Yet")
            else:
                for transaction in current_account.transactions:
                    print(f"""
---------------------------------------
{transaction}
---------------------------------------""")
                time.sleep(0.5)

        elif choice == 7:
            current_account.change_password()

        elif choice == 8:
            print("Successfully Logout")
            time.sleep(0.7)
            return

        else:
            print("Invalid Command")


menu()
