from flask import Blueprint, render_template, request

from utils.message import log_error, log_success, header_action, Model, Action
from .acct_controller import AcctController

acct_bp = Blueprint('acct', __name__)

@acct_bp.route('/accounts')
@log_error(pg_template='accounts.html', model=Model.acct, action=Action.read, accounts=[])
def accounts():
    """
    View all accounts.

    This function takes no arguments and returns the rendered template 
    showing all accounts in detail.
    """
    accounts = AcctController.accounts()
    return render_template('accounts.html', accounts=accounts)

@acct_bp.route('/accounts/add', methods=['GET', 'POST'])
@log_error(model=Model.acct, action=Action.add, pg_template='add_edit_account.html')
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
    
    return render_template('add_edit_account.html', mode=header_action(Action.add))

@acct_bp.route('/accounts/edit', methods=['GET', 'POST'])
@log_error(model=Model.acct, action=Action.edit, template='add_edit_account.html', account=None)
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
        return render_template('add_edit_account.html', account=account, 
                               mode=header_action(Action.edit))
