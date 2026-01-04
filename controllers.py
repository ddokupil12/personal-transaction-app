from datetime import datetime
from decimal import Decimal

from models import AccountModel, CategoryModel, TransactModel
from config import Config
from db import db_fetchall, db_commit

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
        TransactModel.add_transaction(account_id, category_id, amount, 
                                      transaction_date, description)
        
    @classmethod
    def edit_transaction(cls, account_id, category_id, amount, 
                         transaction_date, description, transaction_id):
        cls.check_date(transaction_date)
        TransactModel.edit_transaction(account_id, category_id, amount,
                                       transaction_date, description, 
                                       transaction_id)