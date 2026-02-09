__all__ = []

from datetime import datetime

from flask import render_template, request

from controllers import AcctController, BudgetController, CashflowController
from controllers import CatController, GeneralController, TransactController
from context import app
from message import log_error, log_success, Model, Action

@app.route('/')
@log_error(template='dashboard.html', accounts=[], recent_transactions=[],
           action=Action.read)
def dashboard():
    """
    Load the main dashboard showing accounts and recent transactions.
    
    This function takes no arguments and returns the rendered template 
    showing a simplified view of all accounts and recent transactions.
    """
    limit = 10 # limit the recent transactions
    accounts, recent_transactions = GeneralController.dashboard(limit)
    return render_template('dashboard.html', accounts=accounts, 
                           recent_transactions=recent_transactions)

@app.route('/accounts')
@log_error(template='accounts.html', action=Action.read, accounts=[])
def accounts():
    """
    View all accounts.

    This function takes no arguments and returns the rendered template 
    showing all accounts in detail.
    """
    accounts = AcctController.accounts()
    return render_template('accounts.html', accounts=accounts)

@app.route('/accounts/add', methods=['GET', 'POST'])
@log_error(action=Action.add, template='add_edit_account.html', mode='Add')
def add_account():
    """
    Add a new account.

    On a GET request, this function takes no arguments and returns a
    page that allows a user to add a new account. The user can
    enter an account name and an account type.

    On a POST request, this function takes an account name and type as
    arguments. The user will get a success or error message depending 
    on whether the account could be added.
    
    Method parameters: None

    GET request parameters: None

    POST request parameters:
    accountname: str
    accounttype: str
    """
    if request.method == 'POST':
        name = request.form['accountname']
        account_type = request.form['accounttype']
        AcctController.add_account(name, account_type)
        return log_success(Model.acct, Action.add)
    
    return render_template('add_edit_account.html', mode='Add')

@app.route('/accounts/edit', methods=['GET', 'POST'])
@log_error(action=Action.edit, template='add_edit_account.html', account=None, 
           mode='Edit')
def edit_account():
    """
    Edit an existing account.

    On a GET request, this function takes no arguments and returns a
    page with account information filled in. The user can then change
    the information.

    On a POST request, this function takes an account id, name, and 
    type as arguments. The user will get a success or error message 
    depending on whether the account could be edited.
    
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
        return log_success(Model.acct, Action.edit)
    else:
        account_id = request.args['id']
        account = AcctController.get_account(account_id)
        return render_template('add_edit_account.html', account=account, mode='Edit')

@app.route('/categories')
@log_error(action=Action.read, template='categories.html', categories=[])
def categories():
    """
    View all categories.
    
    This function takes no arguments and returns the rendered template 
    showing all categories in detail.
    """
    categories = CatController.categories()
    return render_template('categories.html', categories=categories)

@app.route('/categories/add', methods=['GET', 'POST'])
@log_error(action=Action.add, template='add_edit_category.html')
def add_category():
    """
    Add a new category.

    On a GET request, this function takes no arguments and returns a
    page that allows a user to add a new category. The user can
    enter a category name and select a category type.

    On a POST request, this function takes a category name and type as
    arguments. The user will get a success or error message depending 
    on whether the category could be added.

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
        return log_success(Model.category, Action.add)
    else:
        return render_template('add_edit_category.html')

@app.route('/categories/edit', methods=['GET', 'POST'])
@log_error(action=Action.edit, template='add_edit_category.html')
def edit_category():
    """
    Edit a selected category.

    For future implementation
    """
    return 'Hello World'

@app.route('/transactions')
@log_error(action=Action.read, template='transactions.html', transactions=[], 
           p=1, has_next=False, has_prev=False)
def transactions():
    """
    View all transactions.
    
    This function takes no arguments and returns the rendered template 
    showing all transactions in detail. There is a Next button at the
    bottom of the page to show more transactions.
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
@log_error(action=Action.add, template='add_edit_transaction.html', 
           accounts=[], categories=[], datetime=datetime, mode='Add')
def add_transaction():
    """
    Add a new transaction.
    
    On a GET request, this function takes no arguments and returns a
    page that allows a user to add a new transaction. The user can 
    select an account and category, and then enter the amount, date,
    and description.

    On a POST request, this function takes an account ID, category ID, 
    amount, date, and description as arguments. The user will get a 
    success or error message depending on whether the transaction could
    be added.

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
        return log_success(Model.transact, Action.add)
    else:
        accounts = AcctController.accounts(balance=False)
        categories = CatController.categories()
        return render_template('add_edit_transaction.html',             
                                accounts=accounts, categories=categories, 
                                datetime=datetime, mode='Add')
    
@app.route('/transactions/edit', methods=['GET', 'POST'])
@log_error(action=Action.edit, template='add_edit_transaction.html', 
           transaction=None, datetime=datetime, accounts=[], categories=[])
def edit_transaction():
    """
    Edit a selected transaction.

    On a GET request, this function takes no arguments and returns a
    page with transaction information filled in. The user can then change
    the information.

    On a POST request, this function takes an account ID, category ID, 
    transaction ID, description, date, and amount as arguments. The 
    user will get a success or error message depending on whether the 
    transaction could be edited.

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
        return log_success(Model.transact, Action.edit)
    else:
        transaction_id = request.args['id']
        accounts = AcctController.accounts(balance=False)
        categories = CatController.categories()
        transaction = TransactController.get_transaction(transaction_id)
        return render_template('add_edit_transaction.html', 
                               transaction=transaction, datetime=datetime, 
                               accounts=accounts, categories=categories)
        
@app.route('/budgets')
@log_error(action=Action.read, template='budgets.html', budgets=[], 
           year=datetime.now().year, month=datetime.now().month, 
           datetime=datetime, abs=abs)
def budgets():
    """
    View all budgets.
    
    O(n) (where n = len(budgets))
    """
    now = datetime.now()
    year = request.args.get('year', now.year, type=int)
    month = request.args.get('month', now.month, type=int)
    budgets, summary = BudgetController.budgets(year, month)
    return render_template('budgets.html', budgets=budgets, year=year, 
                           month=month, datetime=datetime, summary=summary)

@app.route('/budgets/add', methods=['GET', 'POST'])
@log_error(action=Action.add, template='add_edit_budget.html', categories=[], 
           datetime=datetime)
def add_budget():
    """
    Add a new budget.

    On a GET request, this function takes no arguments and returns a
    page that allows a user to add a new budget. The user can
    select a year, month, and category, and then enter an amount.

    On a POST request, this function takes a category ID, month, year,
    and amount as arguments. The user will get a success or error 
    message depending on whether the budget could be added.

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
        return log_success(Model.budget, Action.add, year=year, month=month)
    else:
        categories = CatController.categories()
        return render_template('add_edit_budget.html', 
                               categories=categories, 
                               datetime=datetime)

@app.route('/budgets/edit', methods=['GET', 'POST'])
def edit_budget():
    """
    Edit a selected budget.

    For future implementation
    """
    # This functionality exists in add_budget(). If you try to add 
    # a budget with a category that already has a budget, the existing 
    # budget will be updated.
    return 'Hello World'
    
@app.route('/cashflows')
@log_error(action=Action.read, template='cashflows.html', cashflows=[])
def cashflows():
    """View all cashflows."""
    cashflows = CashflowController.cashflows()
    return render_template('cashflows.html', cashflows=cashflows)

@app.route('/cashflows/add', methods=['GET', 'POST'])
@log_error(action=Action.add, template='add_edit_cashflow.html', 
           transactions=[], 
           cashflow_types=CashflowController.get_types())
def add_cashflow():
    """Add a new cashflow."""
    if request.method == 'POST':
        incomeid = request.form['incomeid']
        expenseid = request.form['expenseid']
        type_ = request.form['type']
        CashflowController.add_cashflow(expenseid, incomeid, type_)
        return log_success(Model.cashflow, Action.add)
    else:
        transactions = TransactController.transactions()
        return render_template('add_edit_cashflow.html', 
                               transactions=transactions, 
                               cashflow_types=CashflowController.
                               get_types())

@app.route('/cashflows/edit', methods=['GET', 'POST'])
def edit_cashflow():
    """
    Edit a selected cashflow.

    For future implementation
    """
    return 'Hello world'

@app.route('/verify', methods=['GET'])
def verify():
    """
    Verify that account transfers and cashflows are correct.

    Verify that the sum of all account transfers is 0 and that all 
    cashflows have 2 equal sides.

    For future implementation
    """
    return 'Hello world'

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'], 
            load_dotenv=False)