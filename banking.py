import random


class BankAccount:
    def __init__(self):
        self._customer_number = None
        self.card_number = None
        self.card_pin = None
        self.balance = 0

    def print_banner(self):
        print("""
1. Create an account
2. Log into account
0. Exit
    """)

    def print_banner_second_level(self):
        print("""
1. Balance
2. Log out
0. Exit
    """)

    def create_customer_number(self):
        self.customer_number = str(random.randint(1, 999999999)).zfill(9)
        return self.customer_number

    def create_card_number(self):
        self.card_number = "400000" + self.create_customer_number() + "8"
        return self.card_number

    def create_card_pin(self):
        self.card_pin = str(random.randint(0, 9999)).zfill(4)
        return self.card_pin


bank_account = BankAccount()

while True:
    breaker = False
    bank_account.print_banner()
    answer = int(input())

    if answer == 1:
        card_number = bank_account.create_card_number()
        pin_number = bank_account.create_card_pin()
        print("Your card has been created")
        print(f"Your card number:\n{card_number}")
        print(f"Your card PIN:\n{pin_number}")
        continue
    if answer == 2:
        print("Enter your card number:")
        entered_card = str(input())
        print("Enter your PIN:")
        entered_pin = str(input())
        if entered_card != card_number or entered_pin != pin_number:
            print("Wrong card number or PIN!")
            continue
        else:
            print("You have successfully logged in!")
            while True:
                bank_account.print_banner_second_level()
                answer_second_level = int(input())
                if answer_second_level == 1:
                    print(bank_account.balance)
                    continue
                if answer_second_level == 2:
                    print("You have successfully logged out!")
                    break
                if answer_second_level == 0:
                    breaker = True
                    break
    if answer == 0 or breaker == True:
        print("Bye!")
        break
