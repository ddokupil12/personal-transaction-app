__all__ = ['CashflowController']

from models import CashflowModel
from .transact_controller import TransactController

class CashflowController:
    @staticmethod
    def cashflows():
        return CashflowModel.get_cashflows()
    
    @staticmethod
    def add_cashflow(expenseid, incomeid, type_):
        expense = TransactController.get_transaction(expenseid)
        income = TransactController.get_transaction(incomeid)
        assert expense['amount'] < 0, 'Expense must be negative'
        assert income['amount'] > 0, 'Income must be positive'
        if type_ == 'Transfer':
            assert expense['amount'] + income['amount'] == 0, 'Sum of both sides must be 0'
            assert expense['transactiondate'] == income['transactiondate']
        CashflowModel.add_cashflow(expenseid, incomeid, type_)

    @classmethod
    def add_transfer(cls, i_account, e_account, i_dscr, e_dscr, amount, date, category):
        i_id = TransactController.add_transaction(i_account, category, amount, 
                                                  date, i_dscr)
        e_id = TransactController.add_transaction(e_account, category, 
                                                  0 - amount, 
                                                  date, e_dscr)
        type_ = 'Transfer'
        cls.add_cashflow(e_id, i_id, type_)

    @staticmethod
    def get_types():
        return ['Business', 'Transfer']
    
    @staticmethod
    def get_transfers():
        return CashflowModel.get_transfers()
    
    @classmethod
    def verify_transfers(cls):
        transfers = cls.get_transfers()
        verified = []
        update = []
        for i in transfers:
            if i['expenseamount'] + i['incomeamount'] == 0:
                verified.append(i)
            else:
                update.append(i)

        return verified, update
    
    @classmethod
    def get_missing_cashflows(cls):
        transfers = TransactController.get_transfers()
        expense_ids = cls.get_expense_ids()
        income_ids = cls.get_income_ids()
        result = [i for i in transfers if i['transactionid'] not in expense_ids and i['transactionid'] not in income_ids]
        return result

    @staticmethod
    def get_expense_ids():
        return [i['expense'] for i in CashflowModel.get_expense_ids()]
    
    @staticmethod
    def get_income_ids():
        return [i['income'] for i in CashflowModel.get_income_ids()]