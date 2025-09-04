from datetime import datetime
from decimal import Decimal
from config import config
from contextlib import contextmanager

from flask import Flask, render_template, request, redirect, url_for, flash
from mysql.connector import Error, connect
from dotenv import load_dotenv

##### Setup
config_name = 'development'
load_dotenv()
app = Flask(__name__)
app.config.from_object(config.get(config_name, config['default']))
app.secret_key = app.config['SECRET_KEY']
DB_CONFIG = app.config['DB_CONFIG']


##### Helper functions
@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    connection = None
    try:
        connection = connect(**DB_CONFIG)
        yield connection
    except Error as e:
        print(f'Error connecting to MySQL: {e}')
        if connection:
            connection.rollback()
        raise Exception(e)
    finally:
        if connection and connection.is_connected():
            connection.close()

def db_fetchall(*args):
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        if len(args) == 1:
            query = args[0]
            cursor.execute(query)
        else:
            raise ValueError("Can't accept multiple queries or arguments yet")
        
        return cursor.fetchall()

def db_fetchone(*args):
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        if len(args) == 1:
            query = args[0]
            cursor.execute(query)
        elif len(args) == 2:
            query = args[0]
            dbArgs = args[1]
            cursor.execute(query, dbArgs)
        else:
            raise ValueError("Can't accept multiple queries yet")
        
        return cursor.fetchone()

def db_commit(*args):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        lenArgs = len(args)
        if lenArgs % 2 == 0:
            for i in range(0, lenArgs, 2):
                query = args[i]
                dbArgs = args[i + 1]
                cursor.execute(query, dbArgs)
        else:
            raise ValueError("Expected an even number of arguments")
        
        conn.commit()

def get_accounts():
    """Fetch all accounts"""
    return db_fetchall('SELECT * FROM acct ORDER BY accountname')

def get_categories():
    """Fetch all categories"""
    return db_fetchall('SELECT * FROM category ORDER BY categoryname')

def get_account_balance(account_id):
    """Calculate account balance using relational method"""
    result = db_fetchone("""
        SELECT COALESCE(SUM(amount), 0) as balance
        FROM transact
        WHERE accountid = %s
        """, (account_id,))['balance'] # db_fetchone() returns dict with only key 'balance'
    return result



##### Routes
@app.route('/')
def dashboard():
    """Main dashboard showing accounts and recent transactions"""
    try:
        accounts = get_accounts()
        
        # Add balance to each account
        for account in accounts:
            account['balance'] = get_account_balance(account['accountid'])
        
        # Get recent transactions
        recent_transactions = db_fetchall("""
            SELECT t.*, a.accountname, c.categoryname 
            FROM transact t
            JOIN acct a ON t.accountid = a.accountid
            JOIN category c ON t.CategoryID = c.CategoryID
            ORDER BY t.TransactionDate DESC, t.TransactionID DESC
            LIMIT 10
        """)
        return render_template('dashboard.html', accounts=accounts, 
                               recent_transactions=recent_transactions)
    except Exception as e:
        flash('Error loading dashboard', 'error')
        print('err:', e)
        return render_template('dashboard.html', accounts=[], 
                               recent_transactions=[])

@app.route('/accounts')
def accounts():
    """Manage accounts"""
    try:
        accounts = get_accounts()
        for account in accounts:
            account['balance'] = get_account_balance(account['accountid'])
            # print(account['balance'])
        return render_template('accounts.html', accounts=accounts)
    except Exception as e:
        flash('Error loading accounts', 'error')
        print('err:', e)
        return render_template('accounts.html', accounts=[])

@app.route('/accounts/add', methods=['GET', 'POST'])
def add_account():
    """Add new account"""
    if request.method == 'POST':
        try:
            name = request.form['accountname']
            account_type = request.form['accounttype']
            db_commit("""
                      INSERT INTO acct (accountname, accounttype) VALUES 
                      (%s, %s)""", 
                      (name, account_type))
            flash('Account added successfully!', 'success')
            return redirect(url_for('accounts'))
        except Exception as e:
            flash('Error adding account', 'error')
        print('err:', e)
    
    return render_template('add_account.html')

@app.route('/accounts/edit', methods=['GET', 'POST'])
def edit_account():
    """Edit existing account"""
    try:    
        if request.method == 'POST':
            account_id = request.form['accountid']
            account_name = request.form['accountname']
            account_type = request.form['accounttype']
            db_commit(
                """
                    UPDATE acct
                    SET accountname = %s
                    WHERE accountid = %s
                """, (account_name, account_id),
                """
                    UPDATE acct
                    SET accounttype = %s
                    WHERE accountid = %s
                """, (account_type, account_id)
                )
            account = {'accountid': account_id, 'accountname': account_name, 'accounttype': account_type}
            flash('Account edited successfully!', 'success')
            return redirect(url_for('accounts'))
        else:
            account_id = request.args['id']
            account = db_fetchone("""
                                  SELECT * 
                                  FROM acct
                                  WHERE accountid = %s
                                  """, [account_id])
            return render_template('edit_account.html', account=account)        

    except Exception as e:
        flash('Error editing account', 'error')
        print('err:', e)
        return render_template('edit_account.html', account=None) 

@app.route('/categories')
def categories():
    """Manage categories"""
    try:
        categories = get_categories()
        return render_template('categories.html', categories=categories)
    except Exception as e:
        flash('Error loading categories', 'error')
        print('err:', e)
        return render_template('categories.html', categories=[])

@app.route('/categories/add', methods=['GET', 'POST'])
def add_category():
    """Add new category"""
    if request.method == 'POST':
        try:
            name = request.form['categoryname']
            cat_type = request.form['type_']
            db_commit("""
                      INSERT INTO category (categoryname, type_) 
                      VALUES (%s, %s)
                      """, (name, cat_type))
            flash('Category added successfully!', 'success')
            return redirect(url_for('categories'))
        except Exception as e:
            flash('Error adding category', 'error')
            print('err:', e)
    
    return render_template('add_category.html')

@app.route('/transactions')
def transactions():
    """View all transactions"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 20
        offset = (page - 1) * per_page
        
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                    SELECT t.*, a.accountname, c.categoryname 
                    FROM transact t
                    JOIN acct a ON t.accountid = a.accountid
                    JOIN category c ON t.CategoryID = c.CategoryID
                    ORDER BY t.transactiondate DESC, t.transactionid DESC
                    LIMIT %s OFFSET %s
                """, (per_page, offset)
                )
            transactions = cursor.fetchall()
            
            # Get total count for pagination
            cursor.execute("SELECT COUNT(*) as total FROM transact")
            total = cursor.fetchone()['total']
        
        has_next = offset + per_page < total
        has_prev = page > 1
        
        return render_template('transactions.html', 
                               transactions=transactions,
                               page=page, 
                               has_next=has_next, 
                               has_prev=has_prev)
    except Exception as e:
        flash('Error loading transactions', 'error')
        print("err:", e)
        return render_template('transactions.html', transactions=[], page=1, 
                               has_next=False, has_prev=False)

@app.route('/transactions/add', methods=['GET', 'POST'])
def add_transaction():
    """Add new transaction"""
    if request.method == 'POST':
        try:
            account_id = request.form['accountid']
            category_id = request.form['categoryid']
            amount = Decimal(request.form['amount'])
            transaction_date = request.form['transactiondate']
            description = request.form['dscr']     
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
            flash('Transaction added successfully!', 'success')
            return redirect(url_for('transactions'))
        except Exception as e:
            flash('Error adding transaction', 'error')
            print('err:', e)
            return render_template('add_transaction.html', accounts=[], 
                                   categories=[], datetime=datetime)
    else:
        try:
            accounts = get_accounts()
            categories = get_categories()
            return render_template('add_transaction.html', accounts=accounts, 
                                   categories=categories, datetime=datetime)
        except Exception as e:
            flash('Error loading form data', 'error')
            print('err:', e)
            return render_template('add_transaction.html', accounts=[], 
                                   categories=[], datetime=datetime)
    
@app.route('/transactions/edit', methods=['GET', 'POST'])
def edit_transaction():
    try:
        accounts = get_accounts()
        categories = get_categories()
        if request.method == 'POST':
            transaction_id = request.form['transactionid']
            account_id = request.form['accountid']
            category_id = request.form['categoryid']
            dscr = request.form['dscr']
            transaction_date = request.form['transactiondate']
            amount = request.form['amount']
            db_commit(
                """
                    UPDATE transact 
                    SET accountid = %s 
                    WHERE transactionid = %s
                """, (account_id, transaction_id),
                """
                    UPDATE transact
                    SET categoryid = %s
                    WHERE transactionid = %s
                """, (category_id, transaction_id),
                """
                    UPDATE transact
                    SET dscr = %s
                    WHERE transactionid = %s
                """, (dscr, transaction_id),
                """
                    UPDATE transact
                    SET transactiondate = %s
                    WHERE transactionid = %s
                """, (transaction_date, transaction_id),
                """
                    UPDATE transact
                    SET amount = %s
                    WHERE transactionid = %s
                """, (amount, transaction_id)
                )
            flash('Transaction edited successfully!', 'success')
            return redirect(url_for('transactions')) 
        else:
            transaction_id = request.args['id']
            transaction = db_fetchone("""
                                      SELECT * 
                                      FROM transact 
                                      WHERE transactionid = %s
                                      """, [transaction_id])
            return render_template('edit_transaction.html', 
                                   transaction=transaction, datetime=datetime, 
                                   accounts=accounts, categories=categories)
    except Exception as e:
        flash('Error editing transaction', 'error')
        print("err:", e)
        return render_template('edit_transaction.html', transaction=None, 
                               datetime=datetime, accounts=[], categories=[])
        
@app.route('/budgets')
def budgets():
    """View budgets"""
    try:
        year = request.args.get('year', datetime.now().year, type=int)
        month = request.args.get('month', datetime.now().month, type=int)
        
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                           SELECT b.*, c.categoryname, c.type_
                           FROM budget b
                           JOIN category c ON b.categoryid = c.categoryid
                           WHERE b.budget_year = %s AND b.budget_month = %s
                           ORDER BY c.categoryname
                           """, (year, month))
            budgets = cursor.fetchall()
            
            # Calculate actual spending for each budget
            for budget in budgets:
                cursor.execute("""
                               SELECT COALESCE(SUM(ABS(amount)), 0) as actual
                               FROM transact t
                               WHERE t.categoryid = %s 
                               AND YEAR(t.transactiondate) = %s 
                               AND MONTH(t.transactiondate) = %s
                               """, (budget['categoryid'], year, month))
                
                # execute() returns dict with only key 'actual'
                actual = cursor.fetchone()['actual']

                budget['actual'] = actual
                budget['remaining'] = budget['budget_amount'] - actual
        
        return render_template('budgets.html', budgets=budgets, year=year, 
                               month=month, datetime=datetime)
    except Exception as e:
        flash('Error loading budgets', 'error')
        print('err:', e)
        now = datetime.now()
        return render_template('budgets.html', budgets=[], year=now.year, 
                               month=now.month, datetime=datetime)

@app.route('/budgets/add', methods=['GET', 'POST'])
def add_budget():
    """Add new budget"""
    if request.method == 'POST':
        try:
            category_id = request.form['categoryid']
            budget_year = request.form['budget_year']
            budget_month = request.form['budget_month']
            budget_amount = Decimal(request.form['budget_amount'])
            db_commit(
                """
                    INSERT INTO budget (categoryid, budget_year, 
                    budget_month, budget_amount) 
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE budget_amount = %s
                """, 
                (
                    category_id, budget_year, budget_month, budget_amount, 
                    budget_amount
                )
            )
            flash('Budget saved successfully!', 'success')
            return redirect(url_for('budgets', year=budget_year, 
                                    month=budget_month))
        except Exception as e:
            flash('Error saving budget', 'error')
            print('err:', e)
            return render_template('add_budget.html', categories=[], 
                                   datetime=datetime)
    
    else:
        try:
            categories = get_categories()
            return render_template('add_budget.html', categories=categories, 
                                   datetime=datetime)
        except Exception as e:
            flash('Error loading categories', 'error')
            print('err:', e)
            return render_template('add_budget.html', categories=[], 
                                   datetime=datetime)
    
@app.route('/cashflows')
def cashflows():
    """View cashflows"""
    try:
        cashflows = db_fetchall("""
            SELECT t.transactionid as expensetransactionid, a.accountname as expenseacct, c.categoryname as expensecat, t.transactiondate as expensedate, t.amount as expenseamount, t.dscr as expensedscr, r1.*, t2.transactionid as incometransactionid, a2.accountname as incomeacct, c2.categoryname as incomecat, t2.amount as incomeamount, t2.transactiondate as incomedate, t2.dscr as incomedscr
            FROM transact t
            JOIN acct a ON t.accountid = a.accountid
            JOIN category c ON t.CategoryID = c.CategoryID
            JOIN cashflow r1 on t.transactionid = r1.expense
            JOIN transact t2 on r1.income = t2.transactionid
            JOIN acct a2 on t2.accountid = a2.accountid
            JOIN category c2 on t2.categoryid = c2.categoryid
            ORDER BY t.transactiondate DESC, t.transactionid DESC;
        """)
        return render_template('cashflows.html', cashflows=cashflows)
    except Exception as e:
        flash('Error loading cashflows', 'error')
        print("err:", e)
        return render_template('cashflows.html', cashflows=[])

@app.route('/cashflows/add', methods=['GET', 'POST'])
def add_cashflow():
    types = ['Business', 'Transfer']
    try:
        if request.method == 'POST':
            incomeid = request.form['incomeid']
            expenseid = request.form['expenseid']
            type_ = request.form['type']
            db_commit("""
                INSERT INTO cashflow (expense, income, type_) VALUES
                (%s, %s, %s)
            """, (expenseid, incomeid, type_))
            flash('Cashflow saved successfully!', 'success')
            return redirect(url_for('cashflows'))
        else:
            transactions = db_fetchall("""
                SELECT *
                FROM transact t
                INNER JOIN acct a
                ON t.accountid = a.accountid
                INNER JOIN category c
                ON t.categoryid = c.categoryid
                ORDER BY t.transactiondate DESC
            """)
            return render_template('add_cashflow.html', 
                                   transactions=transactions, 
                                   cashflow_types=types)
        
    except Exception as e:
        flash('Error adding cashflow', 'error')
        print('err:', e)
        return render_template('add_cashflow.html', transactions=[], 
                               cashflow_types=types)

# Before doing this method, the code needs to be abstracted
@app.route('/cashflows/edit', methods=['GET', 'POST'])
def edit_cashflow():
    return 'Hello world'

@app.route('/verify', methods=['GET'])
def verify_integrity():
    return 'Hello world'

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])