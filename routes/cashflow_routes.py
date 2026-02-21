from flask import Blueprint, render_template, request

from controllers import CashflowController, TransactController
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
        transactions = TransactController.transactions()
        return render_template('add_edit_cashflow.html', 
                               transactions=transactions, 
                               types=CashflowController.get_types(), mode=Action.add)

@cashflow_bp.route('/cashflows/edit', methods=['GET', 'POST'])
@log_error(model=Model.cashflow, action=Action.edit, pg_template='add_edit_cashflow.html', 
           transactions=[], types=CashflowController.get_types())
def edit_cashflow():
    """
    Edit a selected cashflow.

    For future implementation
    """
    return 'Hello world'