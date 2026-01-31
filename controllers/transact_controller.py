from decimal import Decimal
from datetime import datetime

from models.transact_model import TransactModel

__all__ = ['TransactController']

class TransactController:
    @staticmethod
    def transactions(per_page=None, offset=None):
        return TransactModel.get_transactions(per_page, offset)
    
    @staticmethod
    def get_transaction(transaction_id):
        return TransactModel.get_transaction(transaction_id)

    @staticmethod
    def __check_date(transaction_date):
        """
        Ensures that `transaction_date` is not in the future
        
        :param transaction_date: date

        Raises: AssertionError when `transaction_date` is in the future
        """
        dateObj = datetime.strptime(transaction_date, '%Y-%m-%d').date()
        currentDate = datetime.today().date()
        assert dateObj <= currentDate, 'Date must not be in the future'

    @classmethod
    def add_transaction(cls, account_id, category_id, amount, transaction_date,
                        description):
        """
        Controller for adding a transaction to the database
        
        :param account_id: int
        :param category_id: int
        :param amount: Decimal
        :param transaction_date: date
        :param description: str

        Raises AssertionError if:
            amount == 0
            transaction date is in the future
        """
        cls.__check_date(transaction_date)
        assert amount != 0, 'amount must be nonzero'
        TransactModel.add_transaction(account_id, category_id, Decimal(amount),
                                      transaction_date, description)
        
    @classmethod
    def edit_transaction(cls, account_id, category_id, amount, 
                         transaction_date, description, transaction_id):
        cls.__check_date(transaction_date)
        TransactModel.edit_transaction(account_id, category_id, amount,
                                       transaction_date, description, 
                                       transaction_id)