from decimal import Decimal
from datetime import datetime

from models.transact_model import TransactModel

class TransactController:
    @staticmethod
    def transactions(per_page=None, offset=None):
        return TransactModel.get_transactions(per_page, offset)
    
    @staticmethod
    def get_transaction(transaction_id):
        return TransactModel.get_transaction(transaction_id)

    @staticmethod
    def check_date(transaction_date):
        try:
            dateObj = datetime.strptime(transaction_date, '%Y-%m-%d').date()
            assert dateObj <= datetime.today().date()
        except AssertionError:
            message = 'Date must not be in the future'
            raise AssertionError(message)

    @classmethod
    def add_transaction(cls, account_id, category_id, amount, transaction_date,
                        description):
        cls.check_date(transaction_date) 
        TransactModel.add_transaction(account_id, category_id, Decimal(amount),
                                      transaction_date, description)
        
    @classmethod
    def edit_transaction(cls, account_id, category_id, amount, 
                         transaction_date, description, transaction_id):
        cls.check_date(transaction_date)
        TransactModel.edit_transaction(account_id, category_id, amount,
                                       transaction_date, description, 
                                       transaction_id)