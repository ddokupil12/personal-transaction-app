from datetime import datetime

from flask import Blueprint, render_template, request

from message import log_error, log_success, Model, Action
from controllers import BudgetController, CatController

budget_bp = Blueprint('budget', __name__)

@budget_bp.route('/budgets')
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

@budget_bp.route('/budgets/add', methods=['GET', 'POST'])
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

@budget_bp.route('/budgets/edit', methods=['GET', 'POST'])
def edit_budget():
    """
    Edit a selected budget.

    For future implementation
    """
    # This functionality exists in add_budget(). If you try to add 
    # a budget with a category that already has a budget, the existing 
    # budget will be updated.
    return 'Hello World'