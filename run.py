# Dependencies to use our Google Sheets API
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Bank_account')

user_details = SHEET.worksheet('user_details')
data = user_details.get_all_values()

def login():
    print("_______________________WELCOME!_______________________\n")
    print(" Please enter your personal ID number and your PIN code to login.")
    print(" -Personal ID number should be 10 digits. Example: 8909091234, format: YYMMDD****")
    print(" -PIN code should be exactly 6 digits. Example: 123456")
    print("______________________________________________________")
    personal_ID = input("Enter your personal ID number here, 10 digits:\n")
    pin_code = input("Enter your PIN code here, 6 digits:\n")
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

login()
