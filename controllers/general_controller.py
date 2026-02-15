from models import TransactModel
from .acct_controller import AcctController

__all__ = ['GeneralController']

class GeneralController:
    @staticmethod
    def dashboard(limit):
        # Main dashboard showing accounts and recent transactions
        accounts = AcctController.accounts()
        
        # Get recent transactions
        recent_transactions, _ = TransactModel.get_transactions(
            limit, 
            return_total=False
        )
        return accounts, recent_transactions