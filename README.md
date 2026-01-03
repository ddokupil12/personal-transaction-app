# Personal Transaction App

This Flask application allows users to keep track of personal finances. 
Users can add multiple accounts and categories to sort transactions and add budgets to keep track of spending in important areas.

# Specs

Uses Python 3.13, Flask, Jinja2, MySQL 9.4.0

This code has not been tested with any other versions.

# Installation
- Clone the repository
- `pip install -r requirements.txt`
    - Check for Python version compatibility
    - Installs all required modules
- Install [MySQL Community Server](https://dev.mysql.com/downloads/mysql/) 9.4.0
    - This is the version I use, but other versions might be compatible as well
    - Version 9.4.0 is the latest at the time of this writing.
- Add a new database and use `budget.sql` to create the tables.
- Write `./.env` file with:
    - DB_HOST -- name of the server, usually `localhost`
    - DB_PORT -- the server's port, usually 3306
    - DB_NAME -- name of the database
    - DB_USER -- your username, usually `root`
    - DB_PASSWORD -- your password, which should be secure
- Launch server using `python app.py` (use `python3` if applicable)

# Usage
- Use nav bar to switch between sections of the website
- Click the "Edit" buttons to edit those particular rows of their respective tables.
    - For example, click "Edit" on the `/transactions` page to edit a transaction.

# Acknowledgements
- Made with Claude and Copilot, although most of the abstraction and some features were entirely written by me.
- I was inspired by the standard POS transaction database schema and adapted it to better track my own finances. I encourage you to find a system that works for you.

# Contributions
- I try to update this repository regularly and follow [PEP 8](https://peps.python.org/pep-0008/) for readability.
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


# License
To support open source development, you may use this code under the [AGPL v3 license](LICENSE).