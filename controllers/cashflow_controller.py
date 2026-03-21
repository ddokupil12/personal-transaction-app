__all__ = ['CashflowController']

from models import CashflowModel

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