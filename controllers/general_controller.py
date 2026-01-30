from models.account_model import AccountModel
from models.transact_model import TransactModel

class GeneralController:
    @staticmethod
    def dashboard(limit):
        """Main dashboard showing accounts and recent transactions"""
        accounts = AccountModel.get_accounts()
        
        # Add balance to each account
        for account in accounts:
            account['balance'] = AccountModel.get_account_balance(account['accountid'])
        
        # Get recent transactions
        recent_transactions, total = TransactModel.get_transactions(limit, return_total=False)
        return (accounts, recent_transactions)