import random
import sqlite3


class BankAccount:
    def __init__(self):
        self.card_number = None
        self.card_pin = None
        self.entered_card_number = None
        self.entered_card_pin = None
        self.answer = None
        self.conn = sqlite3.connect('card.s3db')
        self.cur = self.conn.cursor()
        self.checksum = 0
        self.current_balance = None
        self.money = 0
        self.card_data = None

    @staticmethod
    def print_main_banner():
        print("1. Create an account\n2. Log into account\n0. Exit")

    @staticmethod
    def print_second_banner():
        print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")

    def create_table(self):
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, pin TEXT, 
            balance INTEGER DEFAULT 0);"""
        )
        self.conn.commit()

    def close_db(self):
        self.conn.close()

    def luhn_algorithm(self):
        self.checksum = 0
        for element, number in enumerate(self.card_number[:15], 1):
            number = int(number)
            if element % 2 != 0:
                number *= 2
                if number > 9:
                    number -= 9
                    self.checksum += number
                else:
                    self.checksum += number
            else:
                self.checksum += number
        self.checksum = str([0 if self.checksum % 10 == 0 else 10 - self.checksum % 10][0])
        if self.card_number[15:] == "":
            self.card_number += self.checksum
        elif len(self.card_number) == 16 and self.card_number[15:] == self.checksum:
            self.rcv_card_existence()
        else:
            print("Probably you made a mistake in the card number. Please try again!")
            self.account_menu()

    def create_card(self):
        self.card_number = "400000" + str(random.randint(1, 999999999)).zfill(9)
        self.luhn_algorithm()
        self.card_pin = str(random.randint(0, 9999)).zfill(4)
        self.cur.execute("INSERT INTO card (number, pin) VALUES (?, ?);", (self.card_number, self.card_pin))
        self.conn.commit()
        print("Your card has been created")
        print(f"Your card number:\n{self.card_number}")
        print(f"Your card PIN:\n{self.card_pin}")

    def enter_card_details(self):
        print("Enter your card number:")
        self.entered_card_number = str(input())
        print("Enter your PIN:")
        self.entered_card_pin = str(input())

    def verify_card(self):
        self.cur.execute("SELECT number, pin FROM card WHERE number = ? AND pin = ?;",
                         (self.entered_card_number, self.entered_card_pin))
        self.card_data = self.cur.fetchone()
        if self.card_data is None:
            print("Wrong card number or PIN!")
            self.main_menu()
        else:
            print("You have successfully logged in!")
            self.account_menu()

    def fetch_balance(self):
        self.cur.execute("SELECT balance FROM card WHERE number = ?;", [self.entered_card_number])
        return self.cur.fetchone()[0]

    def show_balance(self):
        print(self.fetch_balance())

    def add_income(self):
        self.current_balance = self.fetch_balance()
        print("Enter income:")
        self.current_balance += int(input())
        self.cur.execute("UPDATE card SET balance = ? WHERE number = ?;",
                         (self.current_balance, self.entered_card_number))
        self.conn.commit()
        print("Income was added!")

    def do_transfer(self):
        print("Enter card number:")
        self.card_number = str(input())
        self.transfer_card_verification()

    def transfer_card_verification(self):
        if self.card_number == self.entered_card_number:
            print("You can't transfer money to the same account!")
            self.account_menu()
        else:
            self.luhn_algorithm()

    def rcv_card_existence(self):
        self.cur.execute("SELECT number FROM card WHERE number = ?;", [self.card_number])
        if self.cur.fetchone() is None:
            print("Such a card does not exist.")
            self.account_menu()
        else:
            print("Enter how much money you want to transfer:")
            self.money = int(input())
            self.money_transfer()

    def money_transfer(self):
        if self.money > self.fetch_balance():
            print("Not enough money!")
            self.account_menu()
        else:
            self.cur.execute("UPDATE card SET balance = balance - ? WHERE number = ?;",
                             (self.money, self.entered_card_number))
            self.cur.execute("UPDATE card SET balance = balance + ? WHERE number = ?;",
                             (self.money, self.card_number))
            self.conn.commit()
            print("Success!")
            self.account_menu()

    def close_account(self):
        self.cur.execute("DELETE FROM card WHERE number = ?", [self.entered_card_number])
        self.conn.commit()
        print("The Account has been closed!")

    def main_menu(self):
        self.create_table()
        self.print_main_banner()
        self.answer = int(input())

        if self.answer == 1:
            self.create_card()
            self.main_menu()
        elif self.answer == 2:
            self.enter_card_details()
            self.verify_card()
        elif self.answer == 0:
            self.close_db()
            print("Bye!")
        else:
            self.main_menu()

    def account_menu(self):
        self.print_second_banner()
        self.answer = int(input())
        if self.answer == 1:
            self.show_balance()
            self.account_menu()
        elif self.answer == 2:
            self.add_income()
            self.account_menu()
        elif self.answer == 3:
            self.do_transfer()
        elif self.answer == 4:
            self.close_account()
            self.main_menu()
        elif self.answer == 5:
            print("You have successfully logged out!")
            self.main_menu()
        elif self.answer == 0:
            self.close_db()
            print("Bye!")
        else:
            self.account_menu()


bank_account = BankAccount()
bank_account.main_menu()
