#!/bin/bash

# Path to your Python interpreter
PYTHON_INTERPRETER="~/.venvs/foo/bin/python3"  # Adjust this to the correct path if needed

# Path to your Python script
SCRIPT_UPDATE_DEALS="/root/reporting_cron/update_deals.py"
# Path to your Python script
SCRIPT_UPDATE_CURRENCY="/root/reporting_cron/update_currency.py"


# Run the Python script
print("========Start Running update_deals.py========")
$PYTHON_INTERPRETER $SCRIPT_UPDATE_DEALS
print("-------Completed update_deals.py--------")



# Run the Python script
print("========Start Running update_currency.py========")
$PYTHON_INTERPRETER $SCRIPT_UPDATE_CURRENCY
print("-------Completed update_currency.py--------")

