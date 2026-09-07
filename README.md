# Personal Transaction App

This appplication allows users to keep track of personal finances.

Users can add multiple accounts and categories to keep track of transactions. Additionally, users can add budgets to highlight spending in important areas. Accounts, categories, budgets, and transactions can be edited as needed.

# Specs

Uses Python 3.13, Flask, Jinja2, MySQL 9.4.0

This code has not been tested with any other versions.

# Installation
- Clone the repository
- Run `pip install -r requirements.txt`
    - This checks for version compatibility and installs all required modules
- Install [MySQL Community Server](https://dev.mysql.com/downloads/mysql/) 9.4.0 using their instructions
    - This is the version I use, but other versions might be compatible as well
    - Version 9.4.0 is the latest at the time of this writing.
- Using MySQL, add a new database and use `budget.sql` to create the tables.
    - Run `CREATE DATABASE db_name;`
    - Copy and paste `budget.sql` and run it
- In the same folder as this repository, create a `.env` file with:
    - DB_HOST -- name of the server, usually `localhost`
    - DB_PORT -- the server's port, usually 3306
    - DB_NAME -- name of the database
    - DB_USER -- your username, usually `root`
    - DB_PASSWORD -- your password, which should be secure
    - SECRET_KEY -- a 256-bit string to keep your server secure
    - PORT -- the port your server will run on, default 5000
    - CONFIG_NAME -- the name of the configuration you want to use
        - Options:
            - `production` - default
            - `development` - turns on debug mode
    - ALLOWED_HOSTS -- the computers that are allowed to access the server
        - Use comma-separated values: ex. localhost,127.0.0.1
- To launch the server, open a terminal/ command prompt window. Run `python3 run.py` (use `python` if applicable)

# Usage
- Use the navigation bar to switch between sections of the website
- Click Add on most pages to add data.
    - For example, click Add Account on the Accounts page to add an account.
    - The Budgets page does not have an Add button because budgets are added automatically.
- Click the Edit buttons to edit the data shown next to it.
    - For example, click Edit on the Transactions page next to a transaction to edit that transaction.
- After clicking Edit, you will see a Delete button.
    - You will be asked to confirm that you want to delete the data. 
    - Data is deleted immediately and permanently.
- The Cashflows page has several unimplemented features.
    - For example, the Edit buttons don't work yet.

# Acknowledgements
- Made with Claude, ChatGPT, and Copilot, although most of the abstraction and some features were entirely written by me.
- I was inspired by the standard POS transaction database schema and adapted it to better track my own finances. I encourage you to find a system that works for you.

# Contributions
- I try to update this repository regularly and follow [PEP 8](https://peps.python.org/pep-0008/) for readability whenever possible.
    - Specific style information below
- Use a fork to suggest new functionality, readability improvements, bug fixes, or security updates.
- All pull requests should use the style guidelines below. Follow PEP 8 unless otherwise specified.
- If it becomes necessary to collaborate on this repo, this policy will change.

## Style
### Quotes
- Use double quotes for multi-line SQL queries (See [Indentation](#indentation))
- Use single quotes [in ambiguous cases](https://peps.python.org/pep-0008/#string-quotes)

```python
raise ValueError("Can't accept multiple queries or arguments")
```
```python
print('err:', e)
```
```python 
'SELECT * FROM category ORDER BY categoryname'
```

### Indentation
- When necessary, SQL queries should be on multiple lines using the [hanging indent method](https://peps.python.org/pep-0008/#indentation) or aligned with the triple double quotes:

```python
"""
    UPDATE acct
    SET accountname = %s
    WHERE accountid = %s
"""
```
- A list or tuple of query arguments can go on the same line as the ending delimiter of the query, as long as it fits.
    - This improves readability when there are many queries being run at once.
    - When using the hanging indent, follow the PEP 8 guidelines for multiline constructs.
```python
# Correct:
account = db_fetchone("""
                      SELECT * 
                      FROM acct
                      WHERE accountid = %s
                      """, [account_id])
```
```python
# Also correct:
account = db_fetchone(
    """
        SELECT * 
        FROM acct
        WHERE accountid = %s
    """, [account_id]
)
```

- When this doesn't work, use the hanging indent method:
```python
# Correct:
db_commit(
    """
        INSERT INTO transact (accountid, categoryid, amount, 
            transactiondate, dscr) 
        VALUES (%s, %s, %s, %s, %s)
    """, 
    (
        account_id, category_id,amount, transaction_date, 
        description 
    )
)
```
```python
# Wrong, but compliant with PEP 8:
db_commit("""
          INSERT INTO transact (accountid, categoryid, amount, 
                transactiondate, dscr) 
          VALUES (%s, %s, %s, %s, %s)""", 
          (account_id, category_id,amount, transaction_date, 
           description))
```

### Imports
I prefer using the `from file import something` syntax since name clashes in this project are  between methods of classes and not between functions. This is not required.

I haven't figured out a way to put all the imports at the top of the file without preventing circular imports. That's just the way this project is designed. Using more files or restructuring the project would be very confusing.

Given this, I've decided to keep all imports between the controller files in the methods where they're used, unless an import is used in two or more controller methods. When this happens, specify the import in a comment at the top of the file below all other project imports.

See [Contributions](#contributions) for instructions on how to suggest a better solution.

```python
"""Correct:"""""""""""""""""""""""""""""""""

"""In package table1:"""

import datetime

import local_file
# from table2 import Table2Controller in method()

class Table1Controller:
    @staticmethod
    def method():
        from table2 import Table2Controller # Not technically a circular import
        ...

"""In package table2"""
import decimal

import local_file
# from table1 import Table1Controller in method()

class Table2Controller:
    @staticmethod
    def method():
        from table1 import Table1Controller # Not technically a circular import
        ...
```
```python
"""Wrong:"""""""""""""""""""""""""""""""""

"""In package table1:"""

import datetime

import local_pkg
from table2 import Table2Controller # Circular import

class Table1Controller:
    @staticmethod
    def method():
        Table2Controller.method()

"""In package table2:"""

import decimal

import local_pkg
from table1 import Table1Controller # Circular import

class Table2Controller:
    @staticmethod
    def method():
        Table1Controller.method()
```

Circular imports between other files can be avoided. Therefore, use the PEP 8 guidelines for all other imports.

# License
Copyright (C) 2025-2026 David Dokupil

This program is free software: you can redistribute it and/or modify it under the terms of the [GNU Affero General Public License](LICENSE) as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the [GNU Affero General Public License](LICENSE) along with this program. If not, see <https://www.gnu.org/licenses/>.