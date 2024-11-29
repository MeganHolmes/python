"""This is a script that takes a csv as input, uses another database csv as a lookup table, and uses both to categorize expenses then prints results to the console."""

# Imports
# System Imports
from __future__ import absolute_import
import sys
from dataclasses import dataclass
import datetime

# Project imports
import IO.file
import IO.currency

# Constants
COL_NUMBER_FOR_RBC_ACCOUNT_TYPE = 0
COL_NUMBER_FOR_RBC_MERCHANT_NAME = 4
COL_NUMBER_FOR_RBC_EXPENSE_TOTAL_CAD = 6
COL_NUMBER_FOR_RBC_DATE = 2
COL_NUMBER_FOR_RBC_EXPENSE_TOTAL_USD = 7

COL_NUMBER_FOR_PP_MERCHANT_NAME = 3
COL_NUMBER_FOR_PP_EXPENSE_TOTAL = 7
COL_NUMBER_FOR_PP_CURRENCY = 6
COL_NUMBER_FOR_PP_SKIP = 4
COL_NUMBER_FOR_PP_TIMEZONE = 2

COL_NUMBER_FOR_RBC_USD_CREDIT_DETERMINATION = 3
COL_NUMBER_FOR_RBC_USD_CREDIT_EXPENSE_TOTAL = 6
COL_NUMBER_FOR_RBC_USD_CREDIT_MERCHANT_NAME = 8

COL_NUMBER_FOR_RBC_USD_DEBIT_DETERMINATION = 4
COL_NUMBER_FOR_RBC_USD_DEBIT_EXPENSE_TOTAL = 7
COL_NUMBER_FOR_RBC_USD_DEBIT_MERCHANT_NAME = 9


DEBUG_MODE = False

# Structs

@dataclass
class ExpenseCategory:
    """Dataclass for Expense Categories"""
    category: str
    numberOfElements: int = 0
    expenseTotal: float = 0

@dataclass
class ExpenseElement:
    """Datacalss for an individual expense location"""
    name: str
    category: str = None
    expense: float = 0

def print_all_categories(listOfCategories):
    """
    Takes a list of categories and prints all of them to the console

    Inputs: listOfCategories: A list of categories to print

    Returns: None
    """
    for category in listOfCategories:
        print(f"{category.categoryName}: ${category.expenseTotal}")

def load_database(pathToDatabase):
    """
    Loads the database containing existing categories and the individual expense locations that makes them up.

    Inputs: pathToDatabase: Path to the database containing expense locaations

    Returns: listOfCategories: A list of ExpenseCategory for each category in the database, sums initalized to 0
             listOfExpenseLocations: A list of ExpenseElement
    """
    databaseList = IO.file.getListFromCSV(pathToDatabase)

    listOfExpenseLocations = []
    listOfCategories = []
    rawListOfCategoryNames = []

    # 0 is the element name / merchant, 1 is category assigned
    for row in databaseList:
        listOfExpenseLocations.append(ExpenseElement(row[0], row[1]))

        if row[1] not in rawListOfCategoryNames:
            rawListOfCategoryNames.append(row[1])
            listOfCategories.append(ExpenseCategory(row[1]))

    return listOfCategories, listOfExpenseLocations

def determine_account_type(row):
    """
    Determines the account type from a row so correct columns can be used.

    Inputs: row: row to categorize

    Returns: type: account type as a string
    """
    type = None

    if row[COL_NUMBER_FOR_RBC_ACCOUNT_TYPE] in ["Chequing", "Savings", "MasterCard"]:
        type = "RBC CAD"
    elif row[COL_NUMBER_FOR_PP_TIMEZONE] == "PDT":
        type = "PayPal"
    elif row[COL_NUMBER_FOR_RBC_USD_CREDIT_DETERMINATION] == "CREDITCARD":
        type = "RBC USD CREDIT"
    elif row[COL_NUMBER_FOR_RBC_USD_DEBIT_DETERMINATION] == "MONEYMRKT":
        type = "RBC USD DEBIT"
    else:
        print(f"Failed to determine type for: {row}")

    return type

def load_new_expenses(pathToNewData):
    """
    Loads the new data and converts raw fields into ExpenseElements lacking category assignment

    Inputs: pathToNewData: Path to the data to import.

    Returns: listOfNewExpenses: List of ExpenseElements from new data file.
    """
    rawData = IO.file.getListFromCSV(pathToNewData)

    listOfNewExpenses = []

    pp_is_detected = False

    # Look ahead to filter extra papypal charges from bank
    for row in rawData[1:]:
        if determine_account_type(row) == "PayPal":
            pp_is_detected = True
            print("Paypal charges were detected in sheet")
            break

    for row in rawData[1:]:

        account_type = determine_account_type(row)

        col_number_for_expense = None
        col_number_for_name = None
        is_cad = True

        if account_type == "PayPal":
            if row[COL_NUMBER_FOR_PP_SKIP] == "Bank Deposit to PP Account ":
                continue
            is_cad = row[COL_NUMBER_FOR_PP_CURRENCY] == "CAD"
            col_number_for_expense = COL_NUMBER_FOR_PP_EXPENSE_TOTAL
            col_number_for_name = COL_NUMBER_FOR_PP_MERCHANT_NAME
        elif account_type == "RBC CAD":
            is_cad = row[COL_NUMBER_FOR_RBC_EXPENSE_TOTAL_CAD] is not None and row[COL_NUMBER_FOR_RBC_EXPENSE_TOTAL_CAD] != ""
            col_number_for_expense = COL_NUMBER_FOR_RBC_EXPENSE_TOTAL_CAD if is_cad else COL_NUMBER_FOR_RBC_EXPENSE_TOTAL_USD
            col_number_for_name = COL_NUMBER_FOR_RBC_MERCHANT_NAME
            col_number_for_name += int(row[COL_NUMBER_FOR_RBC_ACCOUNT_TYPE] != "MasterCard")
        elif account_type == "RBC USD CREDIT":
            is_cad = False
            col_number_for_expense = COL_NUMBER_FOR_RBC_USD_CREDIT_EXPENSE_TOTAL
            col_number_for_name = COL_NUMBER_FOR_RBC_USD_CREDIT_MERCHANT_NAME
        elif account_type == "RBC USD DEBIT":
            is_cad = False
            col_number_for_expense = COL_NUMBER_FOR_RBC_USD_DEBIT_EXPENSE_TOTAL
            col_number_for_name = COL_NUMBER_FOR_RBC_USD_DEBIT_MERCHANT_NAME

        total = float(row[col_number_for_expense])

        if row[col_number_for_name] in ["ONLINE TRANSFER ", "E-TRANSFER SENT "]:
            continue

        if account_type != "PayPal" and total > 0:
            # Expenses are negative, i don't want to track credits right now
            continue

        if account_type != "PayPal" and pp_is_detected and row[col_number_for_name] == "PAYPAL ":
            continue

        total = total if is_cad else IO.currency.convert_usd_to_cad(total)


        listOfNewExpenses.append(ExpenseElement(
            row[col_number_for_name],
            None,
            abs(total)))

    return listOfNewExpenses

def categorize_new_data(listOfExpenseLocations, listOfNewExpenses):
    """
    Searches the existing list of expenses to categorize the new list of expenses

    Inputs: listOfExpenseLocations: The existing expenses that have been categorized previously
            listOfNewExpenses: Thw new exepenses that need category assignment

    Returns: listOfNewExpenses: Expenses with categories now assigned.
    """

    for newExpense in listOfNewExpenses:
        for expenseLocation in listOfExpenseLocations:
            if newExpense.name == expenseLocation.name:
                newExpense.category = expenseLocation.category
                break
            elif newExpense.name == '' and newExpense.expense == 11.95:
                # Stupid format...
                newExpense.category = "Financial"
                newExpense.expense -= 6.00
                break

    return listOfNewExpenses

def sum_expenses(listOfCategories, listOfExpenses, outputCategory):
    """
    Iterates through the expenses and assigns to appropriate category

    Inputs: listOfCategories: A list of categories
            listOfExpenses: A list of expenses to categorize

    Returns listOfCategories: The same list of categories with the totals updated
    """

    if outputCategory is not None:
        print(f"Outputting detailed category {outputCategory}")

    for expense in listOfExpenses:
        for category in listOfCategories:
            if expense.category == category.category:
                category.expenseTotal += expense.expense
                category.numberOfElements += 1

                if expense.category == outputCategory:
                    print(f"Category {outputCategory}, expense: {expense.name}, total: {expense.expense}")

                if DEBUG_MODE:
                    print(f"Adding expense: {expense.name} to {category.category}")

    return listOfCategories

def output_sums(listOfCategories):
    """
    Print all the category sums

    Inputs: listOfCategories: List of categories with sums.

    Returns: None
    """
    print("\nCategory totals:")
    for category in listOfCategories:
        print(f"{category.category}: ${category.expenseTotal} from {category.numberOfElements} elements")

def output_expenses_missing_category(listOfExpenses):
    """
    Print all the expenses that do not have an category defined

    Inputs: listOfExpenses: List of expenses

    Returns: None
    """
    print("\nExpense category not found:")
    for expense in listOfExpenses:
        if expense.category == None or expense.category == "":
            print(f"{expense.name} Missing Category. {expense.expense}")
    print("\n")

def categorize_expenses(pathToDatabase, pathToNewData, outputCategory):
    """
    This is the main function of the categorize_expenses file

    Inputs: pathToDatabase: A file path to the database containing existing categories and classifications
            pathToNewData: A file path to the new data to import.

    Returns:
    """

    print(f"Loading database {pathToDatabase}")
    listOfCategories, listOfExpenseLocations = load_database(pathToDatabase)

    if DEBUG_MODE:
        print("categories loaded:")
        print(listOfCategories)
        print("merchants loaded:")
        print(listOfExpenseLocations)


    print(f"Loading and processing new data from {pathToNewData}")
    listOfNewExpenses = load_new_expenses(pathToNewData)

    if DEBUG_MODE:
        print("list of new expenses")
        print(listOfNewExpenses)

    print(f"Applying existing categories")
    categorizedNewData = categorize_new_data(listOfExpenseLocations, listOfNewExpenses)

    print(f"Totatalling")
    listOfCategories = sum_expenses(listOfCategories, categorizedNewData, outputCategory)

    return listOfCategories, categorizedNewData

if __name__ == '__main__':
    pathToDatabase = sys.argv[1]
    pathToNewData = sys.argv[2]
    outputCategory = None

    if len(sys.argv) == 4:
        outputCategory = sys.argv[3]

    categories, expenses = categorize_expenses(pathToDatabase, pathToNewData, outputCategory)
    output_sums(categories)
    output_expenses_missing_category(expenses)
