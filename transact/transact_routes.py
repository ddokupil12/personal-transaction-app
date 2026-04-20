from datetime import datetime

from flask import Blueprint, render_template, request

from account import AcctController
from category import CatController
from utils.message import log_error, log_success, header_action, Model, Action
from .transact_controller import TransactController

transact_bp = Blueprint('transact', __name__)

@transact_bp.route('/')
@log_error(pg_template='dashboard.html', accounts=[], recent_transactions=[],
           action=Action.read)
def dashboard():
    """
    Load the main dashboard showing accounts and recent transactions.
    
    This function takes no arguments and returns the rendered template 
    showing a simplified view of all accounts and recent transactions.
    """
    limit = 10 # limit the recent transactions
    accounts, recent_transactions = TransactController.dashboard(limit)
    return render_template('dashboard.html', accounts=accounts, 
                           recent_transactions=recent_transactions)

@transact_bp.route('/transactions')
@log_error(model=Model.transact, action=Action.read, pg_template='transactions.html', transactions=[], 
           p=1, has_next=False, has_prev=False, str=str)
def transactions():
    """
    View all transactions.
    
    This function takes no arguments and returns the rendered template 
    showing all transactions in detail. There is a Next button at the
    bottom of the page to show more transactions.
    """
    page = request.args.get('p', 1, type=int)
    query = request.args.get('s', '', type=str)
    per_page = 20
    offset = (page - 1) * per_page
    transactions, total = TransactController.transactions(per_page, offset, search_query=query)
    has_next = offset + per_page < total
    has_prev = page > 1
    return render_template('transactions.html', transactions=transactions,
                           p=page, has_next=has_next, has_prev=has_prev, s=query)

@transact_bp.route('/transactions/add', methods=['GET', 'POST'])
@log_error(model=Model.transact, action=Action.add, pg_template='add_edit_transaction.html', 
           accounts=[], categories=[], datetime=datetime)
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
                                datetime=datetime, mode=header_action(Action.add))
    
@transact_bp.route('/transactions/edit', methods=['GET', 'POST'])
@log_error(model=Model.transact, action=Action.edit, pg_template='add_edit_transaction.html', 
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
                               accounts=accounts, categories=categories, mode=header_action(Action.edit))
    
@transact_bp.route('/transactions/filter')
@log_error(model=Model.transact, action=Action.read, pg_template='transactions.html', transactions=[], 
           p=1, has_next=False, has_prev=False, str=str)
def filter():
    categories = request.args['categories']
    catSplit = categories.split(',')
    transactions = TransactController.filter_category(catSplit)
    return render_template('transactions.html', transactions=transactions,
                           p=1, has_next=False, has_prev=False, s='')

@transact_bp.route('/transactions/delete', methods=['POST'])
@log_error(model=Model.transact, action=Action.delete, transaction=[])
def delete():
    transaction_id = request.form['id']
    TransactController.delete(transaction_id)
    return log_success(Model.transact, Action.delete)