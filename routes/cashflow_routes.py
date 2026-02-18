from flask import Blueprint, render_template, request

from message import log_error, log_success, Model, Action
from controllers import CashflowController, TransactController

cashflow_bp = Blueprint('cashflow', __name__)

@cashflow_bp.route('/cashflows')
@log_error(action=Action.read, pg_template='cashflows.html', cashflows=[])
def cashflows():
    """View all cashflows."""
    cashflows = CashflowController.cashflows()
    return render_template('cashflows.html', cashflows=cashflows)

@cashflow_bp.route('/cashflows/add', methods=['GET', 'POST'])
@log_error(action=Action.add, pg_template='add_edit_cashflow.html', 
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
        transactions = TransactController.transactions()
        return render_template('add_edit_cashflow.html', 
                               transactions=transactions, 
                               types=CashflowController.get_types())

@cashflow_bp.route('/cashflows/edit', methods=['GET', 'POST'])
def edit_cashflow():
    """
    Edit a selected cashflow.

    For future implementation
    """
    return 'Hello world'