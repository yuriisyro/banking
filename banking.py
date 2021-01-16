import random


class BankAccount:
    def __init__(self):
        self._customer_number = None
        self.card_number = None
        self.card_pin = None
        self.entered_card_number = None
        self.entered_card_pin = None
        self.answer = None
        self.balance = 0

    @staticmethod
    def print_main_banner():
        print("1. Create an account\n2. Log into account\n0. Exit")

    @staticmethod
    def print_second_banner():
        print("1. Balance\n2. Log out\n0. Exit")

    def create_card_number(self):
        self._customer_number = str(random.randint(1, 999999999)).zfill(9)
        self.card_number = "400000" + self._customer_number + str(random.randint(1, 9))

    def create_card_pin(self):
        self.card_pin = str(random.randint(0, 9999)).zfill(4)

    def enter_card_details(self):
        print("Enter your card number:")
        self.entered_card_number = str(input())
        print("Enter your PIN:")
        self.entered_card_pin = str(input())

    def main_menu(self):
        self.print_main_banner()
        self.answer = int(input())

        if self.answer == 1:
            self.create_card_number()
            self.create_card_pin()
            print("Your card has been created")
            print(f"Your card number:\n{self.card_number}")
            print(f"Your card PIN:\n{self.card_pin}")
            self.main_menu()
        elif self.answer == 2:
            self.enter_card_details()
            if self.entered_card_number == self.card_number and self.entered_card_pin == self.card_pin:
                print("You have successfully logged in!")
                self.account_menu()
            else:
                print("Wrong card number or PIN!")
                self.main_menu()
        elif self.answer == 0:
            print("Bye!")
        else:
            self.main_menu()

    def account_menu(self):
        self.print_second_banner()
        self.answer = int(input())
        if self.answer == 1:
            print(f"Balance: {self.balance}")
            self.account_menu()
        elif self.answer == 2:
            print("You have successfully logged out!")
            self.main_menu()
        elif self.answer == 0:
            print("Bye!")
        else:
            self.account_menu()


bank_account = BankAccount()
bank_account.main_menu()
