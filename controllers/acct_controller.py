from models.account_model import AccountModel
from models.transact_model import TransactModel

class AcctController:
    @staticmethod
    def accounts(balance=True):
        """
        Controller for returning all current accounts from the database
        
        :param balance: bool | True
            Determines whether each account balance is returned
        """
        accounts = AccountModel.get_accounts()
        if balance:
            for account in accounts:
                account['balance'] = TransactModel.get_account_balance(account['accountid'])


        return accounts
    
    @staticmethod
    def get_account(account_id): return AccountModel.get_account(account_id)
    
    @staticmethod
    def add_account(name, account_type): 
        AccountModel.add_account(name, account_type)
    
    @staticmethod
    def edit_account(account_id, account_name, account_type):
        AccountModel.edit_account(account_id, account_name, account_type)
        account = {'accountid': account_id, 'accountname': account_name, 'accounttype': account_type}
        return account