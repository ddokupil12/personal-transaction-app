from models import CashflowModel

__all__ = ['CashflowController']

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