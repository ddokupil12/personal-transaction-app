from flask import Blueprint, render_template, request

from controllers import CatController
from .message import log_error, log_success, header_action, Model, Action

category_bp = Blueprint('category', __name__)

@category_bp.route('/categories')
@log_error(model=Model.category, action=Action.read, pg_template='categories.html', categories=[])
def categories():
    """
    View all categories.
    
    This function takes no arguments and returns the rendered template 
    showing all categories in detail.
    """
    categories = CatController.categories()
    income = []
    expense = []
    for c in categories:
        if c['type_'] == 'Income':
            income.append(c)
        elif c['type_'] == 'Expense':
            expense.append(c)

    return render_template('categories.html', income_categories=income, 
                           expense_categories=expense)

@category_bp.route('/categories/add', methods=['GET', 'POST'])
@log_error(model=Model.category, action=Action.add, pg_template='add_edit_category.html')
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
        return render_template('add_edit_category.html', 
                               mode=header_action(Action.add))

@category_bp.route('/categories/edit', methods=['GET', 'POST'])
@log_error(model=Model.category, action=Action.edit, pg_template='add_edit_category.html')
def edit_category():
    """
    Edit a selected category.
    """
    if request.method == 'POST':
        name = request.form['categoryname']
        cat_type = request.form['type_']
        id = request.form['id']
        CatController.edit_category(id, name, cat_type)
        return log_success(Model.category, Action.edit)
    else:
        id = request.args['id']
        category = CatController.get_category(id)
        return render_template('add_edit_category.html', 
                               mode=header_action(Action.edit), 
                               category=category)