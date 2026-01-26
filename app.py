from datetime import datetime
import traceback

from flask import render_template, request, redirect, url_for, flash

from controllers.acct_controller import AcctController
from controllers.budget_controller import BudgetController
from controllers.cashflow_controller import CashflowController
from controllers.cat_controller import CatController
from controllers.general_controller import GeneralController
from controllers.transact_controller import TransactController
from context import app

##### Helper functions
def logError(message, e):
    """Sends an error message to the top of the screen"""
    """and logs the traceback"""
    flash(message, 'error')
    print('err:', e)
    traceback.print_exc()

def logSuccess(message, rte, **kwargs):
    """Sends a success message to the top of the screen """
    """and redirects to `rte`"""
    flash(message, 'success')
    return redirect(url_for(rte, **kwargs))

def checkLogAssertionErr(message, e):
    """Changes message if there's an AssertionError"""
    if isinstance(e, AssertionError):
        message = 'Date must not be in the future'

    logError(message, e)

##### Routes
@app.route('/')
def dashboard():
    """Main dashboard showing accounts and recent transactions"""
    try:
        accounts, recent_transactions = GeneralController.dashboard()
        return render_template('dashboard.html', accounts=accounts, 
                               recent_transactions=recent_transactions)
    except Exception as e:
        logError('Error loading dashboard', e)
        return render_template('dashboard.html', accounts=[], 
                               recent_transactions=[])

@app.route('/accounts')
def accounts():
    """Manage accounts"""
    try:
        accounts = AcctController.accounts()
        return render_template('accounts.html', accounts=accounts)
    except Exception as e:
        logError('Error loading accounts', e)
        return render_template('accounts.html', accounts=[])

@app.route('/accounts/add', methods=['GET', 'POST'])
def add_account():
    """Add new account"""
    if request.method == 'POST':
        try:
            name = request.form['accountname']
            account_type = request.form['accounttype']
            AcctController.add_account(name, account_type)
            return logSuccess('Account added successfully!', 'accounts')
        except Exception as e:
            logError('Error adding account', e)
    
    return render_template('add_edit_account.html', mode='Add')

@app.route('/accounts/edit', methods=['GET', 'POST'])
def edit_account():
    """Edit existing account"""
    try:    
        if request.method == 'POST':
            errorMessage = 'Error editing account'
            account_id = request.form['accountid']
            account_name = request.form['accountname']
            account_type = request.form['accounttype']
            AcctController.edit_account(account_id, account_name, account_type)
            return logSuccess('Account edited successfully!', 'accounts')
        else:
            errorMessage = 'Error loading form data'
            account_id = request.args['id']
            account = AcctController.get_account(account_id)
            return render_template('add_edit_account.html', account=account, mode='Edit')

    except Exception as e:
        logError(errorMessage, e)
        return render_template('add_edit_account.html', account=None, 
                               mode='Edit')

@app.route('/categories')
def categories():
    """Manage categories"""
    try:
        categories = CatController.categories()
        return render_template('categories.html', categories=categories)
    except Exception as e:
        logError('Error loading categories', e)
        return render_template('categories.html', categories=[])

@app.route('/categories/add', methods=['GET', 'POST'])
def add_category():
    """Add new category"""
    if request.method == 'POST':
        try:
            name = request.form['categoryname']
            cat_type = request.form['type_']
            CatController.add_category(name, cat_type)
            return logSuccess('Category added successfully!', 'categories')
        except Exception as e:
            logError('Error adding category', e)
    
    return render_template('add_edit_category.html')

@app.route('/categories/edit', methods=['GET', 'POST'])
def edit_category():
    """Edit a selected category"""
    """For future implementation"""
    return 'Hello World'

@app.route('/transactions')
def transactions():
    """View all transactions"""
    try:
        page = request.args.get('p', 1, type=int)
        per_page = 20
        offset = (page - 1) * per_page
        transactions, total = TransactController.transactions(per_page, offset)
        has_next = offset + per_page < total
        has_prev = page > 1
        return render_template('transactions.html', transactions=transactions,
                               p=page, has_next=has_next, has_prev=has_prev)
    except Exception as e:
        logError('Error loading transactions', e)
        return render_template('transactions.html', transactions=[], page=1, 
                               has_next=False, has_prev=False)

@app.route('/transactions/add', methods=['GET', 'POST'])
def add_transaction():
    """Add new transaction"""
    try:
        if request.method == 'POST':
            errorMessage = 'Error adding transaction'
            account_id = request.form['accountid']
            category_id = request.form['categoryid']
            amount = request.form['amount']
            transaction_date = request.form['transactiondate']
            dscr = request.form['dscr']
            TransactController.add_transaction(account_id, category_id, amount, 
                                               transaction_date, dscr)
            return logSuccess('Transaction added successfully!', 'transactions')
        else:
            errorMessage = 'Error loading form data'
            accounts = AcctController.accounts(balance=False)
            categories = CatController.categories()
            return render_template('add_edit_transaction.html',             
                                   accounts=accounts, categories=categories, 
                                   datetime=datetime, mode='Add')

    except Exception as e:
             
        # An AssertionError will be raised if the date is in the future
        checkLogAssertionErr(errorMessage, e)

        return render_template('add_edit_transaction.html', accounts=[], 
                               categories=[], datetime=datetime, mode='Add')
    
@app.route('/transactions/edit', methods=['GET', 'POST'])
def edit_transaction():
    """Edit a selected transaction"""
    try:
        if request.method == 'POST':
            errorMessage = 'Error editing transaction'
            transaction_id = request.form['transactionid']
            account_id = request.form['accountid']
            category_id = request.form['categoryid']
            dscr = request.form['dscr']
            transaction_date = request.form['transactiondate']
            amount = request.form['amount']
            TransactController.edit_transaction(account_id, category_id, 
                                                amount, transaction_date, dscr, 
                                                transaction_id)
            message = 'Transaction edited successfully!'
            return logSuccess(message, 'transactions')
        else:
            errorMessage = 'Error loading form data'
            transaction_id = request.args['id']
            accounts = AcctController.accounts(balance=False)
            categories = CatController.categories()
            transaction = TransactController.get_transaction(transaction_id)
            return render_template('add_edit_transaction.html', 
                                   transaction=transaction, datetime=datetime, 
                                   accounts=accounts, categories=categories)

    except Exception as e: 
        
        # An AssertionError will be raised if the date is in the future
        checkLogAssertionErr(errorMessage, e)

        return render_template('add_edit_transaction.html', transaction=None, 
                               datetime=datetime, accounts=[], categories=[])
        
@app.route('/budgets')
def budgets():
    """View budgets"""
    now = datetime.now()
    try:
        year = request.args.get('year', now.year, type=int)
        month = request.args.get('month', now.month, type=int)
        budgets, summary = BudgetController.budgets(year, month)
        return render_template('budgets.html', budgets=budgets, year=year, 
                               month=month, datetime=datetime, summary=summary)
    except Exception as e:
        logError('Error loading budgets', e)
        return render_template('budgets.html', budgets=[], year=now.year, 
                               month=now.month, datetime=datetime, abs=abs)

@app.route('/budgets/add', methods=['GET', 'POST'])
def add_budget():
    """Add new budget"""
    try:
        if request.method == 'POST':
            errorMessage = 'Error adding budget'
            category_id = request.form['categoryid']
            year = request.form['budget_year']
            month = request.form['budget_month']
            budget_amount = request.form['amount']
            BudgetController.add_budget(category_id, year, month, budget_amount)
            message = 'Budget added successfully!'
            return logSuccess(message, 'budgets', year=year, month=month)
        else:
            errorMessage = 'Error loading form data'
            categories = CatController.categories()
            return render_template('add_edit_budget.html', 
                                   categories=categories, 
                                   datetime=datetime)
        
    except Exception as e:
        logError(errorMessage, e)
        return render_template('add_edit_budget.html', categories=[], 
                                datetime=datetime)    
    

@app.route('/budgets/edit', methods=['GET', 'POST'])
def edit_budget():
    """Edit a selected budget"""
    """For future implementation"""
    # This functionality exists in add_budget(). If you try to add 
    # a budget with a category that already has a budget, the existing 
    # budget will be updated.
    return 'Hello World'
    
@app.route('/cashflows')
def cashflows():
    """View cashflows"""
    try:
        cashflows = CashflowController.cashflows()
        return render_template('cashflows.html', cashflows=cashflows)
    except Exception as e:
        logError('Error loading cashflows', e)
        return render_template('cashflows.html', cashflows=[])

@app.route('/cashflows/add', methods=['GET', 'POST'])
def add_cashflow():
    """Add new cashflow"""
    types = CashflowController.get_cashflow_types()
    try:
        if request.method == 'POST':
            incomeid = request.form['incomeid']
            expenseid = request.form['expenseid']
            type_ = request.form['type']
            CashflowController.add_cashflow(expenseid, incomeid, type_)
            return logSuccess('Cashflow added successfully!', 'cashflows')
        else:
            transactions = TransactController.transactions()
            return render_template('add_edit_cashflow.html', 
                                   transactions=transactions, 
                                   cashflow_types=types)
        
    except Exception as e:
        logError('Error adding cashflow', e)
        return render_template('add_edit_cashflow.html', transactions=[], 
                               cashflow_types=types)

# Before doing this method, the code needs to be abstracted
@app.route('/cashflows/edit', methods=['GET', 'POST'])
def edit_cashflow():
    """Edit a selected cashflow"""
    """For future implementation"""
    return 'Hello world'

@app.route('/verify', methods=['GET'])
def verify():
    """Verify that the sum of all account transfers is 0 and that all"""
    """cashflows have 2 equal sides"""
    return 'Hello world'

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'])