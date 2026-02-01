from datetime import datetime
from traceback import print_exc
from functools import wraps
from enum import Enum, auto

from flask import render_template, request, redirect, url_for, flash

from controllers import AcctController, BudgetController, CashflowController
from controllers import CatController, GeneralController, TransactController
from context import app

__all__ = []

##### Helper functions

class Model(Enum):
    acct = auto()
    budget = auto()
    cashflow = auto()
    category = auto()
    transact = auto()

class Action(Enum):
    add = auto()
    read = auto()
    edit = auto()
    delete = auto()

def _log_success(model: Model, action: Action, **kwargs):
    """
    Sends a success message to the top of the screen and redirects to 
    `rte`
    
    :param message: str (message to show at the top of the screen)
    :param rte: str (where to redirect the user)
    :param kwargs: any (passed to `url_for()`)

    Returns:
    Response (flask.Flask.redirect)

    O(1) (with constant route length)
    """
    match model:
        case Model.acct:
            page_msg = 'Account'
            rte = 'accounts'
        case Model.budget:
            page_msg = 'Budget'
            rte = 'budgets'
        case Model.cashflow:
            page_msg = 'Cashflow'
            rte = 'cashflows'
        case Model.transact:
            page_msg = 'Transaction'
            rte = 'transactions'
        case _ :
            page_msg = 'Data'
            rte = 'dashboard'
    
    match action:
        case Action.add:
            action_msg = 'added'
        case Action.read:
            action_msg = 'loaded'
        case Action.edit:
            action_msg = 'edited'
        case Action.delete:
            action_msg = 'deleted'

    flash(f'{page_msg} {action_msg} successfully!', 'success')
    return redirect(url_for(rte, **kwargs))

def _log_error(
    log_level='error',  # Logging level
    error_message="An unexpected error occurred",
    template='dashboard.html',
    **templatekwargs
):
    """
    Flexible error handling decorator with multiple configuration options
    
    :param log_level: Logging level (debug, info, warning, error)
    :param error_message: Default error message
    :param custom_handler: Custom error handling function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                nonlocal error_message
                if isinstance(e, AssertionError):
                    error_message = e
                flash(error_message, 'error')
                print('err:', e)
                print_exc()

                return render_template(template, **templatekwargs)
        
        return wrapper
    return decorator

##### Routes
@app.route('/')
@_log_error(template='dashboard.html', accounts=[], recent_transactions=[], 
            error_message='Error loading dashboard')
def dashboard():
    """
    Main dashboard showing accounts and recent transactions
    
    O(n) (where n = len(accounts))
    """
    limit = 10 # limit the recent transactions
    accounts, recent_transactions = GeneralController.dashboard(limit)
    return render_template('dashboard.html', accounts=accounts, 
                            recent_transactions=recent_transactions)

@app.route('/accounts')
@_log_error(template='accounts.html', error_message='Error loading accounts', 
            accounts=[])
def accounts():
    """
    Manage accounts

    O(n) (where n = len(accounts))
    """
    accounts = AcctController.accounts()
    return render_template('accounts.html', accounts=accounts)

@app.route('/accounts/add', methods=['GET', 'POST'])
@_log_error(error_message='Error adding account', 
            template='add_edit_account.html', mode='Add')
def add_account():
    """
    Add new account
    
    Method parameters: None

    GET request parameters: None

    POST request parameters:
    accountname: str
    accounttype: str

    O(1)
    """
    if request.method == 'POST':
        name = request.form['accountname']
        account_type = request.form['accounttype']
        AcctController.add_account(name, account_type)
        return _log_success(Model.acct, Action.add)
    
    return render_template('add_edit_account.html', mode='Add')

@app.route('/accounts/edit', methods=['GET', 'POST'])
@_log_error(error_message='Error editing account', 
            template='add_edit_account.html', account=None, mode='Edit')
def edit_account():
    """
    Edit existing account
    
    Method parameters: None

    GET request parameters: None

    POST request parameters:
    accountid: int
    accountname: str
    accounttype: str
    """
    if request.method == 'POST':
        account_id = request.form['accountid']
        account_name = request.form['accountname']
        account_type = request.form['accounttype']
        AcctController.edit_account(account_id, account_name, account_type)
        return _log_success(Model.acct, Action.edit)
    else:
        account_id = request.args['id']
        account = AcctController.get_account(account_id)
        return render_template('add_edit_account.html', account=account, mode='Edit')

@app.route('/categories')
@_log_error(error_message='Error loading categories', 
            template='categories.html', categories=[])
def categories():
    """
    View categories
    
    O(n) (where n = len(categories))
    """
    categories = CatController.categories()
    return render_template('categories.html', categories=categories)

@app.route('/categories/add', methods=['GET', 'POST'])
@_log_error(error_message='Error adding category', 
            template='add_edit_category.html')
def add_category():
    """
    Add new category

    Method parameters: None

    GET request parameters: None

    POST request parameters:
    categoryname: str
    type_: 'Income' | 'Expense'

    Raises:
    GET request: None
    POST request:
        AssertionError when `type_` not in ['Income', 'Expense']
    """
    if request.method == 'POST':
        name = request.form['categoryname']
        cat_type = request.form['type_']
        CatController.add_category(name, cat_type)
        return _log_success(Model.category, Action.add)
    else:
        return render_template('add_edit_category.html')

@app.route('/categories/edit', methods=['GET', 'POST'])
@_log_error(error_message='Error editing category', 
            template='add_edit_category.html')
def edit_category():
    """
    Edit a selected category
    For future implementation
    """
    return 'Hello World'

@app.route('/transactions')
@_log_error(error_message='Error loading transactions', 
            template='transactions.html', transactions=[], p=1, has_next=False, 
            has_prev=False)
def transactions():
    """
    View all transactions
    
    O(limit) (could be up to len(transactions))
    """
    page = request.args.get('p', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page
    transactions, total = TransactController.transactions(per_page, offset)
    has_next = offset + per_page < total
    has_prev = page > 1
    return render_template('transactions.html', transactions=transactions,
                           p=page, has_next=has_next, has_prev=has_prev)

@app.route('/transactions/add', methods=['GET', 'POST'])
@_log_error(error_message='Error adding transaction', 
            template='add_edit_transaction.html', accounts=[], categories=[], 
            datetime=datetime, mode='Add')
def add_transaction():
    """
    Add new transaction
    
    Method parameters: None

    GET request parameters: None

    POST request parameters:
    accountid: int
    categoryid: int
    amount: Decimal
    transactiondate: date
    dscr: str

    Returns:
    Error: str (HTML)
    GET request: str (HTML)
    POST request: Redirect

    Raises: 
    GET request: None
    POST request: 
        AssertionError when `transactiondate` is in the future
            (see `TransactController.check_date()`)
        AssertionError when amount == 0
            (see `TransactController.add_transaction()`)
    """
    if request.method == 'POST':
        account_id = request.form['accountid']
        category_id = request.form['categoryid']
        amount = request.form['amount']
        transaction_date = request.form['transactiondate']
        dscr = request.form['dscr']
        TransactController.add_transaction(account_id, category_id, amount, 
                                            transaction_date, dscr)
        return _log_success(Model.transact, Action.add)
    else:
        accounts = AcctController.accounts(balance=False)
        categories = CatController.categories()
        return render_template('add_edit_transaction.html',             
                                accounts=accounts, categories=categories, 
                                datetime=datetime, mode='Add')
    
@app.route('/transactions/edit', methods=['GET', 'POST'])
@_log_error(error_message='Error editing transaction', 
            template='add_edit_transaction.html', transaction=None, 
            datetime=datetime, accounts=[], categories=[])
def edit_transaction():
    """
    Edit a selected transaction

    Method parameters: None

    GET request parameters: None

    POST request parameters:
    accountid: int
    categoryid: int
    amount: Decimal
    transactiondate: date
    dscr: str

    Returns:
    Error: str (HTML)
    GET request: str (HTML)
    POST request: Redirect

    Raises: 
    GET request: None
    POST request: 
        AssertionError from `TransactController.check_date()` when 
        `transactiondate` is in the future
    """
    if request.method == 'POST':
        transaction_id = request.form['transactionid']
        account_id = request.form['accountid']
        category_id = request.form['categoryid']
        dscr = request.form['dscr']
        transaction_date = request.form['transactiondate']
        amount = request.form['amount']
        TransactController.edit_transaction(account_id, category_id, 
                                            amount, transaction_date, dscr, 
                                            transaction_id)
        return _log_success(Model.transact, Action.edit)
    else:
        transaction_id = request.args['id']
        accounts = AcctController.accounts(balance=False)
        categories = CatController.categories()
        transaction = TransactController.get_transaction(transaction_id)
        return render_template('add_edit_transaction.html', 
                                transaction=transaction, datetime=datetime, 
                                accounts=accounts, categories=categories)
        
@app.route('/budgets')
@_log_error(error_message='Error loading budgets', template='budgets.html', 
            budgets=[], year=datetime.now().year, month=datetime.now().month, 
            datetime=datetime, abs=abs)
def budgets():
    """
    View budgets
    
    O(n) (where n = len(budgets))
    """
    now = datetime.now()
    year = request.args.get('year', now.year, type=int)
    month = request.args.get('month', now.month, type=int)
    budgets, summary = BudgetController.budgets(year, month)
    return render_template('budgets.html', budgets=budgets, year=year, 
                            month=month, datetime=datetime, summary=summary)

@app.route('/budgets/add', methods=['GET', 'POST'])
@_log_error(error_message='Error adding budget', 
            template='add_edit_budget.html', categories=[], datetime=datetime)
def add_budget():
    """
    Add new budget

    Method parameters: None

    GET request parameters: None

    POST request parameters:
    categoryid: int
    budget_year: int
    budget_month: int
    amount: Decimal

    Raises: 
    GET request: None
    POST request:
    AssertionError when: (see `BudgetController.add_budget()`)
        amount == 0
        budget_month is not one of the 12 months
        budget_year is not in the 2020s
    """
    if request.method == 'POST':
        category_id = request.form['categoryid']
        year = request.form['budget_year']
        month = request.form['budget_month']
        budget_amount = request.form['amount']
        BudgetController.add_budget(category_id, year, month, budget_amount)
        return _log_success(Model.budget, Action.add, year=year, month=month)
    else:
        categories = CatController.categories()
        return render_template('add_edit_budget.html', 
                                categories=categories, 
                                datetime=datetime)

@app.route('/budgets/edit', methods=['GET', 'POST'])
def edit_budget():
    """
    Edit a selected budget
    For future implementation
    """
    # This functionality exists in add_budget(). If you try to add 
    # a budget with a category that already has a budget, the existing 
    # budget will be updated.
    return 'Hello World'
    
@app.route('/cashflows')
@_log_error(error_message='Error loading cashflows', template='cashflows.html', 
            cashflows=[])
def cashflows():
    """View cashflows"""
    cashflows = CashflowController.cashflows()
    return render_template('cashflows.html', cashflows=cashflows)

@app.route('/cashflows/add', methods=['GET', 'POST'])
@_log_error(error_message='Error adding cashflow', 
            template='add_edit_cashflow.html', transactions=[], 
            cashflow_types=CashflowController.get_cashflow_types())
def add_cashflow():
    """Add new cashflow"""
    if request.method == 'POST':
        incomeid = request.form['incomeid']
        expenseid = request.form['expenseid']
        type_ = request.form['type']
        CashflowController.add_cashflow(expenseid, incomeid, type_)
        return _log_success(Model.cashflow, Action.add)
    else:
        transactions = TransactController.transactions()
        return render_template('add_edit_cashflow.html', 
                                transactions=transactions, 
                                cashflow_types=CashflowController.
                                get_cashflow_types())

@app.route('/cashflows/edit', methods=['GET', 'POST'])
def edit_cashflow():
    """
    Edit a selected cashflow
    For future implementation
    """
    return 'Hello world'

@app.route('/verify', methods=['GET'])
def verify():
    """
    Verify that the sum of all account transfers is 0 and that all 
    cashflows have 2 equal sides
    For future implementation
    """
    return 'Hello world'

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'], 
            load_dotenv=False)