__all__ = ['Model', 'Action', 'log_success', 'log_error']

from traceback import print_exc
from functools import wraps
from enum import Enum, auto
from logging import error, ERROR, critical, CRITICAL, info

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

def _match_model(model, plural=False):
    # Helper function for `_log_success()`
    # Determines how to show the model name to the user
    # Determines the route based on what model was changed
    
    # :param model: The model that was changed

    # Returns:
    # message: how the model name appears to the user
    # rte: the route that should be passed to `url_for()`
    match model:
        case Model.acct:
            msg_singular = 'account'
            msg_plural = 'accounts'
            rte = 'acct.accounts'
        case Model.budget:
            msg_singular = 'budget'
            msg_plural = 'budgets'
            rte = 'budget.budgets'
        case Model.cashflow:
            msg_singular = 'cashflow'
            msg_plural = 'cashflows'
            rte = 'cashflow.cashflows'
        case Model.category:
            msg_singular = 'category'
            msg_plural = 'categories'
            rte = 'category.categories'
        case Model.transact:
            msg_singular = 'transaction'
            msg_plural = 'transactions'
            rte = 'transact.transactions'
        case _ :
            msg_singular = 'data'
            msg_plural = msg_singular
            rte = 'transact.dashboard'

    match plural:
        case True:
            return msg_plural, rte
        case False:
            return msg_singular, rte

def header_action(action):
    verb = _match_action(action, tense='present')
    match action:
        case Action.add:
            msg = f'{verb} New'
        case Action.edit:
            msg = verb
        case _ :
            return ''
        
    return msg.title()

def _match_action(action, tense='participle'):
    # Helper function for `_log_success()`
    # Determines how to show the action name to the user

    # :param action: The successful action

    # Returns one of:
    # present: action verb in simple present tense (ex. 'add')
    # past: action verb in past tense (ex. 'added')
    # participle: action verb as a present participle (ex. 'adding')

    match action:
        case Action.add:
            present = 'add'
            past = 'added'
            participle = 'adding'
        case Action.read:
            present = 'load'
            past = 'loaded'
            participle = 'loading'
        case Action.edit:
            present = 'edit'
            past = 'edited'
            participle = 'editing'
        case Action.delete:
            present = 'delete'
            past = 'deleted'
            participle = 'deleting'
        case _:
            raise ValueError("Specify an action")

    match tense:
        case 'participle':
            return participle
        case 'past':
            return past
        case 'present':
            return present
        case _ :
            raise ValueError("Use an available tense")

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
    action_msg = _match_action(action, 'past')
    msg = f'{model_msg} {action_msg} successfully!'.capitalize()
    flash(msg, 'success')
    info(msg)
    return redirect(url_for(rte, **kwargs))

def log_error(
    action,
    log_level=CRITICAL,
    model=None,
    pg_template='dashboard.html',
    **pg_kwargs
):
    """
    Log errors and return a template
    
    :param log_level: Logging level (debug, info, warning, error)
        For future implementation
    :param action: the Action attempted
    :param pg_template: The page that will be loaded
    :param pg_kwargs: The kwargs for the template
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
                    plural = action == Action.read
                    model_msg, _ = _match_model(model, plural=plural)
                    action_msg = _match_action(action) # returns participle
                    error_message = f'Error {action_msg} {model_msg}'
                else:
                    error_message = 'An unexpected error occurred'

                flash(error_message, 'error')
                print_exc()
                if log_level == CRITICAL:
                    critical(error_message)
                else:
                    error(error_message)

                if pg_kwargs.get('mode') is None:
                    mode = header_action(action)

                return render_template(pg_template, mode=mode, **pg_kwargs)
        
        return wrapper
    return decorator