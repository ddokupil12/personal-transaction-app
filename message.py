__all__ = ['Model', 'Action', 'log_success', 'log_error']

from traceback import print_exc
from functools import wraps
from enum import Enum, auto

from flask import flash, redirect, render_template, url_for

class Model(Enum):
    # Use attributes to indicate which model
    acct = auto()
    budget = auto()
    cashflow = auto()
    category = auto()
    transact = auto()

class Action(Enum):
    # Use attributes to indicate which action is happening
    add = auto()
    read = auto()
    edit = auto()
    delete = auto()

def _match_model(model):
    # Helper function for `_log_success()`
    # Determines how to show the model name to the user
    # Determines the route based on what model was changed
    
    # :param model: The model that was changed

    # Returns:
    # message: how the model name appears to the user
    # rte: the route that should be passed to `url_for()`
    match model:
        case Model.acct:
            message = 'account'
            rte = 'accounts'
        case Model.budget:
            message = 'budget'
            rte = 'budgets'
        case Model.cashflow:
            message = 'cashflow'
            rte = 'cashflows'
        case Model.transact:
            message = 'transaction'
            rte = 'transactions'
        case _ :
            message = 'data'
            rte = 'dashboard'

    return message, rte

def _match_action(action):
    # Helper function for `_log_success()`
    # Determines how to show the action name to the user

    # :param action: The successful action

    # Returns:
    # past: action verb in past tense (ex. 'added')
    # participle: action verb as a present participle (ex. 'adding')
    match action:
        case Action.add:
            past = 'added'
            participle = 'adding'
        case Action.read:
            past = 'loaded'
            participle = 'loading'
        case Action.edit:
            past = 'edited'
            participle = 'editing'
        case Action.delete:
            past = 'deleted'
            participle = 'deleting'

    return past, participle

def log_success(model, action, **kwargs):
    """
    Sends a success message to the user and redirects them
    based on what page they're coming from

    :param model: The model that was changed
    :param action: The successful action
    :param kwargs: any (passed to `url_for()`)

    Returns:
    Response (flask.Flask.redirect)

    O(1) (with constant route length)
    """
    model_msg, rte = _match_model(model)
    action_msg, _ = _match_action(action)
    flash(f'{model_msg} {action_msg} successfully!'.capitalize(), 'success')
    return redirect(url_for(rte, **kwargs))

def log_error(
    log_level='error',  # Logging level
    action=None,
    pg_template='dashboard.html', # The template that will load
    **pg_kwargs # The kwargs for the template
):
    """
    Log errors and return a template
    
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
                if isinstance(e, AssertionError):
                    error_message = e
                elif isinstance(action, Action):
                    model_msg, _ = _match_model(None)
                    _, action_msg = _match_action(action) # returns participle
                    error_message = f'Error {action_msg} {model_msg}'
                else:
                    error_message = 'An unexpected error occurred'

                flash(error_message, 'error')
                print('err:', e)
                print_exc()

                return render_template(pg_template, **pg_kwargs)
        
        return wrapper
    return decorator