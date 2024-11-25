# Online Bank Account System -  Testing

![Online Bank Account System](assets/images/portal-image.jpg)

Visit the deployed site: [Online Bank Account System](https://online-bank-account-system-0e5e73e47365.herokuapp.com/)

- - -

## CONTENTS

* [AUTOMATED TESTING](#automated-testing)
  * [PEP8 Validator](#pep8-validator)
* [MANUAL TESTING](#manual-testing)
  * [Testing User Goals](#testing-user-goals)
  * [Testing Site Owner Goals](#testing-site-owner-goals)
  * [Testing Google Sheets](#testing-google-sheets)
  * [The Full Testing](#the-full-testing)
    * [Functional Testing](#functional-testing)

Testing was ongoing throughout the entire project development, and all detected issues have been dealt with and resolved during this time. The deployed site was tested on the following browsers on a VivoBook Asus laptop: Chrome (version: 129.0.6668.100 (Official Build) (64-bit)), Microsoft Edge (version: 129.0.2792.89 (Official Build) (64-bit)), Opera One (version: 114.0.5282.102), and Firefox (version: 131.0.3 (64-bit)). The website proved to be compatible with all the tested browsers. Furthermore, a few friends conducted additional testing on their laptops, and no issues were detected or reported in these sessions.

### Automated Testing

#### PEP8 Validatior

### Manual Testing

#### Testing User Goals

#### Testing Site Owner Goals

#### Testing Google Sheets

#### The Full Testing

##### Functional Testing

* User authentication:
 
 | Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- |
| Personal ID input | The Personal ID input field appears for the user to input their personal ID number | Ran the program | The Personal ID input field appeared and took the required input | Pass|
| PIN code input | The PIN code input field appears and takes the user's input | Tested during the program run | The PIN code input field appeared and took the required input | Pass |
| Personal ID input error handling | An error message appears and prompts the user to enter a valid input | Tested by entering an empty field, input with both fewer and more characters than 10, including letters and signs | The related error message appeared and prompted the user to enter a valid input | Pass |
| PIN code input error handling | An error message appears and prompts the user to enter a valid input | Tested by entering an empty field, input with both fewer and more characters than 6, including letters and signs | The related error message appeared and prompted the user to enter a valid input | Pass |
| Credential validation if the user has an account but the PIN code is incorrect | An error message appears if the PIN code doesn't match the one stored in the Google Sheets and prompts the user to enter the correct PIN code | Entered personal ID number belonging to an existing account with a wrong PIN code | An error message appeared prompting the user to enter the correct PIN code  | Pass |
| Credential validation if the user has an account and the PIN code is correct | The user successfully logs in | Entered personal ID number belonging to an existing account with the correct PIN code | The user successfully logged in and the account dashboard appeared | Pass |
| Credential validation if the account doesn't exist | Offers the user the option to create a new account | Entered a personal ID number that doesn't exist in the Google Sheets | It informed the user that the account didn't exist and offered to create a new account | Pass |
| New account creation input handling |  |  |  | Pass |
|  |  |  |  | Pass |


