from datetime import datetime
from decimal import Decimal

from models import AccountModel, CategoryModel, TransactModel, BudgetModel, CashflowModel
from db import db_fetchall, db_commit, get_db_connection

class GeneralController:
    @staticmethod
    def dashboard():
        """Main dashboard showing accounts and recent transactions"""
        accounts = AccountModel.get_accounts()
        
        # Add balance to each account
        for account in accounts:
            account['balance'] = AccountModel.get_account_balance(account['accountid'])
        
        # Get recent transactions
        recent_transactions = db_fetchall("""
            SELECT t.*, a.accountname, c.categoryname 
            FROM transact t
            JOIN acct a ON t.accountid = a.accountid
            JOIN category c ON t.CategoryID = c.CategoryID
            ORDER BY t.TransactionDate DESC, t.TransactionID DESC
            LIMIT 10
        """)
        return (accounts, recent_transactions)
    
class AcctController:
    @staticmethod
    def accounts(balance=True):
        accounts = AccountModel.get_accounts()
        if balance:
            for account in accounts:
                account['balance'] = AccountModel.get_account_balance(account['accountid'])


        return accounts
    
    @staticmethod
    def get_account(account_id): return AccountModel.get_account(account_id)
    
    @staticmethod
    def add_account(name, account_type): 
        AccountModel.add_account(name, account_type)
    
    @staticmethod
    def edit_account(account_id, account_name, account_type):
        AccountModel.edit_account(account_id, account_name, account_type)
        account = {'accountid': account_id, 'accountname': account_name, 'accounttype': account_type}
        return account
    
class CatController:
    @staticmethod
    def categories():
        return CategoryModel.get_categories()
    
    @staticmethod
    def add_category(name, cat_type): 
        CategoryModel.add_category(name, cat_type)
    
class TransactController:
    @staticmethod
    def transactions(per_page, offset):
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
        

class BudgetController:
    @staticmethod
    def budgets(year, month):
        totalSpent = 0
        budgetSpending = 0
        budgetIncome = 0
        budgets = BudgetModel.get_budgets(year, month)
        for budget in budgets:
            actual = budget['actual']
            absActual = abs(actual)
            budget['remaining'] = budget['budget_amount'] - absActual
            if budget['type_'] == 'Expense':
                budgetSpending += budget['budget_amount']
                if actual > 0:
                    totalSpent += actual
                    budget['actual'] = 0 - actual
                    budget['remaining'] = budget['budget_amount'] + absActual
                else:
                    totalSpent += absActual
            else:
                budgetIncome += budget['budget_amount']
            
            summary = {'total_budgeted': budgetSpending,
                    'total_spent': totalSpent,
                    'total_remaining': budgetSpending - totalSpent
                    }
            
        return budgets, summary
        
    @staticmethod
    def add_budget(category_id, budget_year, budget_month, amount):
        budget_amount = Decimal(amount)
        BudgetModel.add_budget(category_id, budget_year, budget_month, 
                               budget_amount)
        


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