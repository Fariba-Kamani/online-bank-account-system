# Dependencies to use the Google Sheets API
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

"""
Grants permission to view and manage your Google Sheets files.
Grants access to view and manage Google Drive files and folders that you have opened or created with the app.
Provides full access to Google Drive.
"""
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Bank_account')

class BankAccount:
    """
    Bank account class
    """
   
    def __init__(self, first_name, surname, pin_code, id_number, account_number, row_number, balance=0):
        # Creates an instance of bank account
        self.first_name = first_name
        self.surname = surname
        self.pin_code = pin_code
        self.id_number = id_number
        self.account_number = account_number
        self.balance = round(balance, 2)
        self.row_number = row_number
        self.transactions = []
    
    def welcome_message(self):
        print(f"Welcome to your account {self.first_name} {self.surname}!")
        print(f"Account number: {self.account_number}\n")
        print("For menu press 1, to log out press 2")
        condition = True
        while condition:
            response = input()
            print()
            if response == "1":
                self.show_menu()
                condition = False
            elif response == "2":
                print("EXIT")
                condition = False
            else:
                print("Invalid response! Please answer only 1 for menu or 2 to log out.")

    def show_menu(self):
        print("Check balance: press 1, Deposit: press 2, Withdrawal: press 3, Transactions history: press 4, Log out: press 5")
        menu_response = input()
        print()
        if menu_response == "1":
            self.check_balance()
        elif menu_response == "2":
            self.deposit()
        elif menu_response == "3":
            self.withdra()
        elif menu_response == "4":
            print("transactions")
        elif menu_response == "5":
            print("Exit")
        else:
            print("Invalid value! Please choose a value from the menu.")
            self.show_menu()

    def check_balance(self):
        print(f"Your balance is {self.balance} sek.\n") 
        self.show_menu()  

    def deposit(self):
        try:
            amount = float(input("Please enter the amount you want to deposit to your account here:\n"))
            print()
            if amount > 0:
                self.balance += round(amount, 2)
                time = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.transactions.append([int(self.account_number), "Deposit", round(amount, 2), time])
                self.update_transactions()
                self.update_balance()
            else:
                print("Please enter an amount greater than 0 sek.")
                self.deposit()
        except ValueError:
            print("Invalid input, please enter a valid number.")
            self.deposit()


    def withdra(self):
        try:
            amount = float(input("Please enter the amount you want to withdra from your account here:\n"))
            print()
            if amount > 0 and amount <= self.balance:
                self.balance -= round(amount, 2)
                time = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.transactions.append([int(self.account_number), "Withdrawal", round(amount,2), time])
                self.update_transactions()
                self.update_balance()
            elif amount < 0:
                print("Please enter an amount greater than 0 sek.")
                self.withdra()
            else:
                print("Not enough bank account balance for this request. Please enter a valid value.")
                self.withdra()
        except ValueError:
            print("Invalid input, please enter a valid number.")
            self.withdra()
    
    def update_transactions(self):
        transactions = self.transactions[0]
        SHEET.worksheet("transactions").append_row(transactions)
    
    def update_balance(self):
        SHEET.worksheet("user_details").update_cell(self.row_number, 6, f"{self.balance:.2f}")
        print(f"Transaction successful. Current Balance: {self.balance:.2f} sek")





class NewAccount(BankAccount):
    """
    Creates a new account for a user if they don’t already have one.
    """
    def __init__(self, pin_code, id_number ):
        condition = True
        while condition:
            name = input("Please enter your first name here:").strip().capitalize()
            surname = input("Please enter your surname here:").strip().capitalize()
            print()
            try:
                if name == "" or surname == "":
                    raise ValueError(
                        "Name or surname is missing. Required data"
                    )
                elif not name.isalpha() or not surname.isalpha():
                    raise ValueError(
                        "Name and surname should contain only letters"
                    )
            except ValueError as e:
                print(f"Invalid data: {e}. Please try again")
                condition = False
            condition = True
            self.name = name
            self.surname = surname
            break
        account_number = int(SHEET.worksheet('user_details').col_values(5)[-1]) + 1
        super().__init__(name, surname, pin_code, id_number, account_number, balance=0)
        self.add_new_account()
        self.confirmation_new_account()
    
    def add_new_account(self):
        new_account_data = [self.name, self.surname, self.pin_code, self.id_number, self.account_number, self.balance]
        SHEET.worksheet("user_details").append_row(new_account_data)

    def confirmation_new_account(self):
        print(f"Congratulations! A new account has been successfully created.\n{self.name} {self.surname}\npersonal ID number: {self.id_number}\naccount number: {self.account_number}\nPIN code: {self.pin_code}\nInitial balance amount: {self.balance} sek")
        print("Please login with your personal ID number and PIN code to access your account.")
        

        
                

def get_login_inputs():
    """
    Checks if the user has entered exactly 10 digits for personal ID number,
    and exactly 6 digits for the PIN code.
    Checks if the user has an account,
    and if they have entered the right PIN code.
    If the account is found but user has entered the wrong PIN code, asks for the correct PIN code.
    If the user doesn't have an account asks if the they want to create an account.
    """
    print("_______________________WELCOME!_______________________\n")
    print(" Please enter your personal ID number and your PIN code to login.")
    print(" -Personal ID number should be 10 digits. Example: 8909091234, format: YYMMDD****")
    print(" -PIN code should be exactly 6 digits. Example: 123456")
    print("______________________________________________________")
    while True:
        personal_ID = input("Enter your personal ID number here, 10 digits:\n")
        pin_code = input("Enter your PIN code here, 6 digits:\n")
        print()
        if login_validation(personal_ID, pin_code):
            break
    account_validation(personal_ID, pin_code)

def login_validation(personal_ID, pin_code):
    try:
        if not personal_ID.isdigit() or not pin_code.isdigit():
            raise ValueError(
                "Your personal ID and PIN code should only include digits!"
            )
        elif len(personal_ID) != 10 or len(pin_code) != 6:
            raise ValueError(
                "Your personal ID number should be exactly 10 digits, \nand your PIN code should be exactly 6 digits."
            )
    except ValueError as e:
        print(f"Invalid data: {e} Please try again.\n")
        return False
    return True

def account_validation(personal_ID, pin_code):  
    user_details = SHEET.worksheet('user_details')
    try:
        cell = user_details.find(personal_ID)
        data = user_details.row_values(cell.row)
        row_number = cell.row
        if data[2] == pin_code:
            costumer = BankAccount(data[0], data[1], data[2], data[3], data[4], row_number, float(data[5]))
            costumer.welcome_message()
        else:
            print("Wrong PIN code.")   
    except gspread.exceptions.CellNotFound:
        print("Account doesn't exist. Would you like to create a new account? (yes/no)")
        response = input().strip().lower()
        if response == "yes":
            NewAccount(pin_code, personal_ID)
        else:
            print("Exit app")
    except Exception as e:
        print(f"An error occurred: {e}")


get_login_inputs()
