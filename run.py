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
   
    def __init__(self, first_name, surname, pin_code, id_number, account_number, balance=0):
        # Creates an instance of bank account
        self.first_name = first_name
        self.surname = surname
        self.pin_code = pin_code
        self.id_number = id_number
        self.account_number = account_number
        self.balance = balance
        self.transactions = []

    def check_balance(self):
        print(f"Account number: {self.account_number}")
        print(f"Welcome to your account {self.first_name} {self.surname}!")
        print(f"Your balance is {self.balance} sek.\n") 
        print("For deposit, press 1")
        print("For Withdrawal, press 2")
        print("To check your transactions history, press 3")
        print("To log out, press 4\n")   

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append("Deposit", amount)


    def withdra(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.transactions.append("Withdrawal", amount)

        

def login_validation():
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
    personal_ID = input("Enter your personal ID number here, 10 digits:\n")
    pin_code = input("Enter your PIN code here, 6 digits:\n")
    print()
    try:
        if not personal_ID.isdigit() or not pin_code.isdigit():
            raise ValueError(
                f"Your personal ID and PIN code should only include digits!"
            )
        elif len(personal_ID) != 10 or len(pin_code) != 6:
            raise ValueError(
                f"Your personal ID number should be exactly 10 digits, \nand your PIN code should be exactly 6 digits."
            )
    except ValueError as e:
        print(f"Invalid data: {e} Please try again.\n")
    
    user_details = SHEET.worksheet('user_details')
    cell = user_details.find(personal_ID)
    data = user_details.row_values(cell.row)
    if cell and data[2] == pin_code:
        costumer = BankAccount(data[0], data[1], data[2], data[3], data[4], data[5] )
        print(costumer.check_balance())
    elif not cell:
        print("account doesn't exist")
    elif data[cell.row - 1][2] != pin_code:
        print("Wrong PIN code.")
        



login_validation()
