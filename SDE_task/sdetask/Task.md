# Senior Data Engineer Coding Challenge
## Prerequisites
You'll need Python 3 (we use 3.6) and [SQLite](https://www.sqlite.org/index.html) installed to complete this challenge.
## Setup
Run the below to setup the database:
```bash
sqlite3 data/mortgages.db < bin/create_db.sql
```
## Task 1
Create a Python process to extract data from the SQLite3 mortgages database (data/mortgages.db) and create a report in CSV file format summarising the total number of accounts and the sum of account balances for each product type. The report should have the following 3 columns:

- product_type (based on PRODUCTS.PD_PRODUCT_TYPE)
- total_accounts
- total_balance (based on ACCOUNTS.A_ACCOUNT_BALANCE)

The CSV file should be called 'product_summary_report.csv'.

## Task 2
Create a Python process to extract data from the SQLite3 mortgages database (data/mortgages.db) and create a JSON file in the below format:
```JSON
{
    "accounts": [
        {
            "account_number": 1,
            "months_in_arrears": 17.1,
            "in_possession": false,
            "in_default": true,
            "customers": [
                {
                    "customer_position": 1,
                    "is_bankrupt": false,
                    "is_deceased": false
                },
                {
                    "customer_position": 2,
                    "is_bankrupt": false,
                    "is_deceased": false
                }
            ]
        },
        {
            "account_number": 2,
            "months_in_arrears": 3.3,
            "in_possession": false,
            "in_default": false,
            "customers": [
                {
                    "customer_position": 1,
                    "is_bankrupt": false,
                    "is_deceased": false
                },
                {
                    "customer_position": 2,
                    "is_bankrupt": false,
                    "is_deceased": false
                }
            ]
        },
        ...
    ]
}
```
- The JSON file should be named 'mortgages_data.json'.
- The "accounts" list should contain an entry for each account in the ACCOUNTS table in the mortgages database.
- Each acccount entry should contain a list of all customers attached to the account

## Derived Data Items
### _months_in_arrears_
Defined as the absolute arrears balance for an account divided by the regular monthly payment amount. The value should be rounded to 1 decimal place. The minimum value should be 0
### _in_possession_
A boolean flag based on the field PROPERTIES.PT_IN_POSSESSION
### _in_default_
An account is said to be in default in the following circumstances:
1. The account is in possession
2. The account is 3 months or more in arrears and either customer 1 or customer 2 is bankrupt
3. The account is more than 6 months in arrears
### _customer_position_
This is based on the field ACCOUNTS_CUSTOMERS_LINK.ACL_CUSTOMER_POSITION
### _is_bankrupt_
A boolean flag based on the field CUSTOMERS.C_BANKRUPTCY_IND
### _is_deceased_
This should be set to 'true' if the CUSTOMERS.C_DECEASED_DATE is populated
## Tips
- Write well structured code
- Make it easy to use

## Submission
Please send us all of your code, comments, test data etc. in a new zip file called 'sde_task_{your name}.zip'. Please _do not_ send us:
- PYC files or any other cache files
- SQLite databases

We will unpack your code, run it and review.

## Finally
Thank you for taking the time to complete this task.
