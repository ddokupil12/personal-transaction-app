from models import AccountModel, TransactModel

__all__ = ['GeneralController']

class GeneralController:
    @staticmethod
    def dashboard(limit):
        """Main dashboard showing accounts and recent transactions"""
        accounts = AccountModel.get_accounts()
        
        for account in accounts: # Add balance to each account
            account['balance'] = TransactModel.get_account_balance(
                account['accountid'])
        
        # Get recent transactions
        recent_transactions, _ = TransactModel.get_transactions(
            limit, 
            return_total=False
        )
        return accounts, recent_transactions