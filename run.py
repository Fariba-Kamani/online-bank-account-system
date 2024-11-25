# Dependencies to use the Google Sheets API
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from tabulate import tabulate

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
        self.show_menu()

    def show_menu(self):
        while True:
            menu_options = [[1, "Check balance"], [2, "Deposit"], [3, "Withdrawal"], [4, "Transfer"], [5, "Transactions history"], [6, "Log out"]]
            headers = ["Press", "Action"]
            print(tabulate(menu_options, headers=headers, tablefmt="pretty"))
            menu_response = input("Select a number from the menu above (1-6):\n").strip()
            print()
            if menu_response == "1":
                self.check_balance()
            elif menu_response == "2":
                self.deposit()
            elif menu_response == "3":
                self.withdraw()
            elif menu_response == "4":
                self.transfer()
            elif menu_response == "5":
                self.transactions_history()
            elif menu_response == "6":
                self.log_out()
                # Stop further execution of the menu after logging out.
                break
            else:
                print("Invalid value! Please choose a value from the menu.")

    def check_balance(self):
        print(f"Your balance is {self.balance:.2f} sek.\n")   

    def deposit(self):
        try:
            amount = float(input("Please enter the amount you want to deposit to your account here:\n"))
            print()
            if 0 < amount <= 5000:
                self.balance += round(amount, 2)
                time = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.transactions.append([int(self.account_number), "Deposit", round(amount, 2), time, int(self.account_number)])
                self.update_transactions()
                self.update_balance()
                print(f"Deposit was successful. Current Balance: {self.balance:.2f} sek")
                print()
            elif amount > 5000:
                print("You are not authorized to deposit more than 5000 sek.")
                self.deposit()
            else:
                print("The amount should be greater than 0 sek.")
                self.deposit()
        except ValueError:
            print("Invalid input, please enter a valid number.")
            self.deposit()

    def withdraw(self):
        try:
            amount = float(input("Please enter the amount you want to withdraw from your account here:\n"))
            print()
            if amount > 0 and amount <= self.balance:
                self.balance -= round(amount, 2)
                time = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.transactions.append([int(self.account_number), "Withdrawal", round(amount,2), time, int(self.account_number)])
                self.update_transactions()
                self.update_balance()
                print(f"Withdrawal was successful. Current balance: {self.balance:.2f} sek")
                print()
            elif amount <= 0:
                print("Please enter an amount greater than 0 sek.")
                self.withdraw()
            else:
                print("Not enough bank account balance for this request. Please enter a valid value.")
                self.withdraw()
        except ValueError:
            print("Invalid input, please enter a valid number.")
            self.withdraw()
    
    def update_transactions(self):
        last_transaction = self.transactions[-1]
        SHEET.worksheet("transactions").append_row(last_transaction)
    
    def update_balance(self):
        SHEET.worksheet("user_details").update_cell(self.row_number, 6, f"{self.balance:.2f}")
    
    def transactions_history(self):
        transactions_worksheet = SHEET.worksheet("transactions")
        matched_cells = [cell for cell in transactions_worksheet.findall(self.account_number) if cell.col == 1]
        if not matched_cells:
            print(f"No transactions found for account {self.account_number}.\n")
            return
        transactions_history_list = []
        for cell in matched_cells:
            data = transactions_worksheet.row_values(cell.row)
            transactions_history_list.append([data[1], data[2], data[3], data[4]])
        print("Your transaction history is as follows:")
        headers = ["Type", "Amount(sek)", "Date & Time", "Destination account"]
        print(tabulate(transactions_history_list, headers=headers, tablefmt="pretty", maxcolwidths= [11, 11, 15, 6]))
    
    def transfer_validation(self):
        user_details = SHEET.worksheet("user_details")
        while True:
            transfer_account = input("Please enter the account number you want to transfer balance to:\n")
            if transfer_account == self.account_number:
                print("You cannot transfer money to your own account. Please enter a different account number.")
                continue
            matched_cell = user_details.find(transfer_account)    
            if not matched_cell:
                print("This account doesn't exist.")
                while True:
                    response = input("To try again press 1, to go back to menu press 2. Please enter your selection (1-2):\n").strip()
                    if response == "1":
                        break     
                    elif response == "2":
                        return None
                    else:
                        print("Invalid selection!")
                        continue
            else:
                # Valid account found
                break

        # Loop for validating transfer amount
        while True:
            try:
                transfer_amount = float(input("Please enter the amount you want to transfer:\n"))
                if transfer_amount <= 0:
                    print("Amount must be greater than 0. Please try again.")
                elif transfer_amount > self.balance:
                    print("Not enough balance for this transfer. Please enter a lower amount.")
                else:
                    # Valid amount, exit loop
                    break
            except ValueError:
                print("Invalid input, please enter a valid number.")
        return [transfer_account, transfer_amount, matched_cell]

        
    def transfer(self):
        inputs = self.transfer_validation()
        # Check if transfer_validation returned None (user opted to go back to menu)
        if inputs is None:
            # Exit transfer and return to menu
            return
        transfer_account = inputs[0]
        transfer_amount = inputs[1]
        matched_cell = inputs[2]
        user_details = SHEET.worksheet("user_details")
        target_data = user_details.row_values(matched_cell.row)
        target_account = BankAccount(target_data[0], target_data[1], target_data[2], target_data[3], target_data[4], matched_cell.row, float(target_data[5]))
        # Proceed with the transfer if the amount is valid
        self.balance -= round(transfer_amount, 2)
        time = datetime.now().strftime("%Y-%m-%d %H:%M")
        # Update sender's transactions
        self.transactions.append([int(self.account_number), "Transfered", round(transfer_amount,2), time, int(target_account.account_number)])
        self.update_transactions()
        self.update_balance()
        print(f"Transfer was successful. Current balance: {self.balance:.2f} sek")
        print()
        # Update recipient's transactions
        target_account.balance += round(transfer_amount, 2)
        target_account.transactions.append([int(target_account.account_number), "Received", round(transfer_amount,2), time, int(self.account_number)])
        target_account.update_transactions()
        target_account.update_balance()       

    def log_out(self):
        print("Thanks for using your online bank account service.\nLooking forward to seeing you soon.")

class NewAccount(BankAccount):
    """
    Creates a new account for a user if they don’t already have one.
    """
    
    def __init__(self, pin_code, id_number ):
        while True:
            name = input("Please enter your first name here:\n").strip().capitalize()
            print()
            if self.validate_new_account_input(name, "name"):
                self.name = name
                break
        while True:
            surname = input("Please enter your surname here:\n").strip().capitalize()
            print()
            if self.validate_new_account_input(surname, "surname"):
                self.surname = surname
                break
        account_number = int(SHEET.worksheet('user_details').col_values(5)[-1]) + 1
        row_number = len(SHEET.worksheet('user_details').get_all_values()) + 1
        super().__init__(name, surname, pin_code, int(id_number), account_number, row_number, balance=0)
        self.add_new_account()
        self.confirmation_new_account()
    
    def validate_new_account_input(self, value, field_name):
        """
        Ensures that the inputted name and surname are non-empty, contain only letters, and are at least 2 characters long.
        """
        if not value:
            print(f"Invalid data: {field_name} is missing. Required data. Please try again.")
            return False    
        elif not value.isalpha():
            print(f"Invalid data: {field_name} should contain only letters. Please try again.")
            return False
        elif len(value) < 2:
            print(f"Invalid data: {field_name} must be at least 2 characters long. Please try again.")
            return False
        return True

    def add_new_account(self):
        new_account_data = [self.name, self.surname, self.pin_code, self.id_number, self.account_number, self.balance]
        SHEET.worksheet("user_details").append_row(new_account_data)

    def confirmation_new_account(self):
        print(f"Congratulations! A new account has been successfully created.\n{self.name} {self.surname}\nPersonal ID number: {self.id_number}\nAccount number: {self.account_number}\nPIN code: {self.pin_code}\nInitial balance amount: {self.balance} sek")
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
    print(" -Personal ID number should be 10 digits. Format: YYMMDD****, Example: 8909091234")
    print(" -PIN code should be exactly 6 digits. Example: 123456")
    print("______________________________________________________")
    while True:
        personal_ID = input("Enter your personal ID number here, 10 digits:\n")
        print()
        if login_validation(personal_ID, "personal ID number", 10):
            break
    while True:
        pin_code = input("Enter your PIN code here, 6 digits:\n")
        print()
        if login_validation(pin_code, "PIN code", 6):
            break
    account_validation(personal_ID, pin_code)

def login_validation(login_input, string, length):
    try:
        if not login_input.isdigit():
            raise ValueError(
                f"Your {string} should only include digits!"
            )
        elif len(login_input) != length:
            raise ValueError(
                f"Your {string} should be exactly {length} digits."
            )
    except ValueError as e:
        print(f"Invalid data: {e} Please try again.\n")
        return False
    return True

def account_validation(personal_ID, pin_code):  
    user_details = SHEET.worksheet('user_details')
    try:
        cell = user_details.find(personal_ID)
        if cell is None:
            while True:
                try:
                    print(f"Account doesn't exist. Would you like to create a new account with \npersonal ID number {personal_ID} and \nPIN code {pin_code}?")
                    response = input("(yes/no)\n").strip().lower()
                    if response == "yes":
                        NewAccount(pin_code, personal_ID)
                        return
                    elif response == "no":
                        temp_account = BankAccount("", "", "", "", "", 0)
                        temp_account.log_out()
                        return
                    else:
                        raise ValueError(
                            "Invalid choice! The answer must be either 'yes' or 'no'."
                        )
                except ValueError as e:
                    print(e)
        else:
            data = user_details.row_values(cell.row)
            row_number = cell.row
            if data[2] == pin_code:
                costumer = BankAccount(data[0], data[1], data[2], data[3], data[4], row_number, float(data[5]))
                costumer.welcome_message()
            else:
                print("Wrong PIN code.")
                pin_code = input("Please enter the correct PIN code:\n")
                print()
                account_validation(personal_ID, pin_code)   
    except gspread.exceptions.GSpreadException as e:
        print(f"An unexpected error occurred: {e}")

get_login_inputs()
