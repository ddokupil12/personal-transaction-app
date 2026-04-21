__all__ = ['CashflowController']

from decimal import Decimal

from transact import TransactController
from .cashflow_model import CashflowModel

class CashflowController:
    @staticmethod
    def cashflows(per_page=None, offset=None, return_total=True):
        return CashflowModel.get_cashflows(per_page, offset, return_total)
    
    @staticmethod
    def add_cashflow(expenseid, incomeid, type_):
        expense = TransactController.get_transaction(expenseid)
        income = TransactController.get_transaction(incomeid)
        assert expense['amount'] < 0, 'Expense must be negative'
        assert income['amount'] > 0, 'Income must be positive'
        assert expense['categoryid'] == income['categoryid'], 'category must be the same'
        if type_ == 'Transfer':
            assert expense['amount'] + income['amount'] == 0, 'Sum of both sides must be 0'
            assert expense['transactiondate'] == income['transactiondate'], 'Date must be the same'
        CashflowModel.add_cashflow(expenseid, incomeid, type_)

    @classmethod
    def add_transfer(cls, i_account, e_account, i_dscr, e_dscr, amount_, date, category):
        amount = abs(Decimal(amount_))
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
        return CashflowModel.get_cashflows_by_type('Transfer')
    
    @staticmethod
    def get_business_cashflows():
        return CashflowModel.get_cashflows_by_type('Business')

    @classmethod
    def verify_transfers(cls):
        transfers = cls.get_transfers()
        verified = []
        update = []
        for i in transfers:
            if (i['expenseamount'] + i['incomeamount'] == 0
                    and i['expensedate'] == i['incomedate']
                    and i['expensecategory'] == i['incomecategory']
                    and i['expenseamount'] < 0
                    and i['incomeamount'] > 0):
                verified.append(i)
            else:
                update.append(i)

        return verified, update
    
    @classmethod
    def verify_business_cashflows(cls):
        business_cashflows = cls.get_business_cashflows()
        verified = []
        update = []
        for i in business_cashflows:
            if (i['expenseamount'] + i['incomeamount'] >= 0
                    and i['expensedate'] == i['incomedate']
                    and i['expensecategory'] == i['incomecategory']
                    and i['expenseamount'] < 0
                    and i['incomeamount'] > 0):
                verified.append(i)
            else:
                update.append(i)

        return verified, update
        
    @classmethod
    def _filter_cashflows(cls, cashflows):
        # For get_missing_cashflows()
        expense_ids = cls.get_expense_ids()
        income_ids = cls.get_income_ids()
        result = [i for i in cashflows if i['transactionid'] not in expense_ids and i['transactionid'] not in income_ids]
        return result

    @classmethod
    def get_missing_cashflows(cls):
        t_transfer = TransactController.get_transfers()
        t_business = TransactController.get_business_transacts()
        res_transfer = cls._filter_cashflows(t_transfer)
        res_business = cls._filter_cashflows(t_business)
        return res_transfer, res_business

    @staticmethod
    def get_expense_ids():
        return [i['expense'] for i in CashflowModel.get_expense_ids()]
    
    @staticmethod
    def get_income_ids():
        return [i['income'] for i in CashflowModel.get_income_ids()]
    
    @staticmethod
    def add_journal_entry(*args):
        # Each transaction is a dictionary
        # Accepts an arbitrary number of dictionary
        # Salary example
        # Expenses
        # -50 McDonald's with friends
        #       Revenue
        #       +10 Friend 1 paid back
        #       +20 Friend 2 paid back
        # 
        # Log each transaction independently, then log the cashflows
        # 
        pass