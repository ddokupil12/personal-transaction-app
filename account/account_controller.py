__all__ = ['AcctController']

# TransactController imported in accounts()
from .account_model import AccountModel

class AcctController:
    @staticmethod
    def accounts(balance=True):
        # Controller for returning all current accounts from the database
        # :param balance: bool | True
        #    Determines whether each account balance is returned
        # O(n) (where n = len(accounts))
        from transact import TransactController

        accounts = AccountModel.get_accounts()
        if balance:
            for account in accounts:
                account['balance'] = TransactController.get_account_balance(
                    account['accountid'])

        return accounts
    
    @staticmethod
    def get_account(account_id): return AccountModel.get_account(account_id)
    
    @staticmethod
    def add_account(name, account_type): 
        AccountModel.add_account(name, account_type)
    
    @staticmethod
    def edit_account(account_id, account_name, account_type):
        AccountModel.edit_account(account_id, account_name, account_type)