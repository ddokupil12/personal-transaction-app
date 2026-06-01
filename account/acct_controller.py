__all__ = ['AcctController']

from decimal import Decimal

# TransactController imported in accounts()
from .account_model import AccountModel

class AcctController:
    @staticmethod
    def accounts(balance=True, show_net_cash=False):
        # Controller for returning all current accounts from the database
        # :param balance: bool | True
        #    Determines whether each account balance is returned
        # O(n) (where n = len(accounts))

        if show_net_cash:
            assert balance, 'An internal error occurred'
        from transact import TransactController

        accounts = AccountModel.get_accounts()
        if balance is True:
            net_cash = Decimal(0)
            for account in accounts:
                account['balance'] = TransactController.get_account_balance(
                    account['accountid'])
                
                if show_net_cash:
                    net_cash += account['balance']
            

    
        if show_net_cash:
            return accounts, net_cash
        else:
            return accounts
    
    @staticmethod
    def get_account(account_id): return AccountModel.get_account(account_id)
    
    @staticmethod
    def add_account(name, account_type): 
        AccountModel.add_account(name, account_type)
    
    @staticmethod
    def edit_account(account_id, account_name, account_type):
        AccountModel.edit_account(account_id, account_name, account_type)

    @classmethod
    def delete(cls, id):
        try:
            x = AccountModel.delete(id) 
        except Exception as e:
            assert cls.get_account(id) is None, 'Account is still being used somewhere else'
            raise Exception(e)