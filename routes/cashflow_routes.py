from flask import Blueprint, render_template, request
from datetime import datetime

from controllers import CashflowController, AcctController, CatController
from .message import log_error, log_success, header_action, Model, Action

cashflow_bp = Blueprint('cashflow', __name__)

@cashflow_bp.route('/cashflows')
@log_error(model=Model.cashflow, action=Action.read, pg_template='cashflows.html', cashflows=[])
def cashflows():
    """View all cashflows."""
    cashflows = CashflowController.cashflows()
    return render_template('cashflows.html', cashflows=cashflows)

@cashflow_bp.route('/cashflows/add', methods=['GET', 'POST'])
@log_error(model=Model.cashflow, action=Action.add, pg_template='add_edit_cashflow.html', 
           transactions=[], types=CashflowController.get_types())
def add_cashflow():
    """Add a new cashflow."""
    if request.method == 'POST':
        incomeid = request.form['incomeid']
        expenseid = request.form['expenseid']
        type_ = request.form['type']
        CashflowController.add_cashflow(expenseid, incomeid, type_)
        return log_success(Model.cashflow, Action.add)
    else:
        transactions = CashflowController.get_missing_cashflows()
        return render_template('add_edit_cashflow.html', 
                               transactions=transactions, 
                               types=CashflowController.get_types(), 
                               mode=header_action(Action.add))

@cashflow_bp.route('/cashflows/edit', methods=['GET', 'POST'])
@log_error(model=Model.cashflow, action=Action.edit, pg_template='add_edit_cashflow.html', 
           transactions=[], types=CashflowController.get_types())
def edit_cashflow():
    """
    Edit a selected cashflow.

    For future implementation
    """
    return 'Hello world'

@cashflow_bp.route('/cashflows/verify')
@log_error(model=Model.cashflow, action=Action.read, pg_template='verify_cashflows.html', cashflows=[])
def verify():
    """Verify that account transfers are accurate and paired"""
    # Get transactions where cashflow is type transfer (Controller)
    verified, update = CashflowController.verify_transfers()
    # For each transfer, make sure the amounts on both sides are equal (Controller)

    # Make sure that all transfers are cashflows, and raise exceptions for the ones that aren't (Controller)
    missing = CashflowController.get_missing_cashflows()
    # Suggest transfers the user can confirm to add so that all transfers are paired (Controller)

    # Display transfers that aren't paired (View)
    # Display transfers that are paired, but aren't accurate (View)
    # Suggest additions and revisions to the user (View)

    return render_template('verify_cashflows.html', verified=verified, update=update, missing=missing)

@cashflow_bp.route('/cashflows/add_transfer', methods=['GET', 'POST'])
@log_error(model=Model.cashflow, action=Action.read, pg_template='add_transfer.html', cashflows=[])
def add_transfer():
    """Add both transfer transactions on one page, and add the corresponding cashflow"""
    if request.method == 'POST':
        i_account = request.form['i_account']
        e_account = request.form['e_account']
        i_dscr = request.form['i_dscr']
        e_dscr = request.form['e_dscr']
        amount = request.form['amount']
        date = request.form['date']
        category = request.form['categoryid']
        CashflowController.add_transfer(i_account, e_account, i_dscr, e_dscr, 
                                        amount, date, category)
        return log_success(Model.cashflow, Action.add)
    else:
        accounts = AcctController.accounts(balance=False)
        categories = CatController.categories()
        return render_template('add_transfer.html',             
                                accounts=accounts, categories=categories, 
                                datetime=datetime, mode=header_action(Action.add))
    