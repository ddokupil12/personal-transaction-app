__all__ = ['TransactController']

from decimal import Decimal
from datetime import datetime

from account import AcctController
from category import CatController
from .model import TransactModel

class TransactController:
    @staticmethod
    def transactions(per_page=None, offset=None, search_query=None, return_total=True):
        return TransactModel.get_transactions(per_page, offset, search_query, return_total)
    
    @staticmethod
    def filter_category(categories):
        return TransactModel.filter_category(categories)

    @classmethod
    def get_transfers(cls):
        transfer_cat = CatController.get_category_by_name('Account Transfer')
        return cls.filter_category([transfer_cat['categoryid']])
    
    @classmethod
    def get_business_transacts(cls):
        business_cat = CatController.get_category_by_name('Business')
        return cls.filter_category([business_cat['categoryid']])

    @staticmethod
    def get_transaction(transaction_id):
        return TransactModel.get_transaction(transaction_id)

    @staticmethod
    def __check_date(transaction_date):
        # Ensures that `transaction_date` is not in the future
        # :param transaction_date: date
        # Raises: AssertionError when `transaction_date` is in
        #     the future.
        dateObj = datetime.strptime(transaction_date, '%Y-%m-%d').date()
        currentDate = datetime.today().date()
        assert dateObj <= currentDate, 'Date must not be in the future'

    @classmethod
    def add_transaction(cls, account_id, category_id, amount, transaction_date,
                        description):
        # Controller for adding a transaction to the database
        # :param account_id: int
        # :param category_id: int
        # :param amount: Decimal
        # :param transaction_date: date
        # :param description: str
        # Raises AssertionError if:
        #     amount == 0
        #     transaction date is in the future
        cls.__check_date(transaction_date)
        assert amount != 0, 'amount must be nonzero'
        return TransactModel.add_transaction(account_id, category_id, 
                                             Decimal(amount),
                                             transaction_date, description)
        
    @classmethod
    def edit_transaction(cls, account_id, category_id, amount, 
                         transaction_date, description, transaction_id):
        cls.__check_date(transaction_date)
        return TransactModel.edit_transaction(account_id, category_id, amount,
                                       transaction_date, description, 
                                       transaction_id)
        
    @staticmethod
    def dashboard(limit):
        # Main dashboard showing accounts and recent transactions
        accounts = AcctController.accounts()
        
        # Get recent transactions
        recent_transactions = TransactModel.get_transactions(
            limit, 
            return_total=False
        )
        return accounts, recent_transactions
    
    @staticmethod
    def get_account_balance(account_id):
        return TransactModel.get_account_balance(account_id)