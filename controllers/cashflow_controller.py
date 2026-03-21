__all__ = ['CashflowController']

from models import CashflowModel
from .transact_controller import TransactController

class CashflowController:
    @staticmethod
    def cashflows():
        return CashflowModel.get_cashflows()
    
    @staticmethod
    def add_cashflow(expenseid, incomeid, type_):
        CashflowModel.add_cashflow(expenseid, incomeid, type_)

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