from models.cashflow_model import CashflowModel

__all__ = ['CashflowController']

class CashflowController:
    @staticmethod
    def cashflows():
        return CashflowModel.get_cashflows()
    
    @staticmethod
    def add_cashflow(expenseid, incomeid, type_):
        CashflowModel.add_cashflow(expenseid, incomeid, type_)

    @staticmethod
    def get_cashflow_types():
        return ['Business', 'Transfer']