__all__ = ['TransactController']

from decimal import Decimal
from datetime import datetime

from category import CatController
from utils.message import Model
from .transact_model import TransactModel
# from account import AcctController already in dashboard()

class TransactController:
    @staticmethod
    def transactions(per_page=None, offset=None, search_query=None, return_total=True):
        query = None if search_query == '' else search_query
        return TransactModel.get_transactions(per_page, offset, query, 
                                              return_total)
    
    # Individual filters
    # @staticmethod
    # def filter_category(categories):
    #     return TransactModel.filter(categories, Model.category)
    # Acct
    # @staticmethod
    # def filter_acct(accounts):
    #     return TransactModel.filter(accounts, Model.acct)
    # amount
    # @staticmethod
    # def filter_amount(lower, upper):
    #     return TransactModel.filter_amount(lower, upper)
    # date
    # @staticmethod
    # def filter_date(lower, upper):
    #     return TransactModel.filter_date(lower, upper)

    # General filter
    @staticmethod
    def filter(ids, model):
        return TransactModel.filter(ids, model)

    @classmethod
    def get_transfers(cls):
        transfer_cat = CatController.get_category_by_name('Account Transfer')
        return cls.filter([transfer_cat['categoryid']], Model.category)
    
    @classmethod
    def get_business_transacts(cls):
        business_cat = CatController.get_category_by_name('Business')
        return cls.filter([business_cat['categoryid']], Model.category)

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

        from account import AcctController
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
    
    @classmethod
    def delete(cls, id):
        try:
            x = TransactModel.delete(id) 
        except Exception as e:
            assert cls.get_transaction(id) is None, 'Transaction is still being used somewhere else'
            raise Exception(e)

    @classmethod
    def sum_transacts_from_cat(cls, category_name):
        category = CatController.get_category_by_name(category_name)['categoryid']
        transactions = cls.filter((category,), Model.category)
        total = sum([i['amount'] for i in transactions])
        return total