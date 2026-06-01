from utils.db import db_fetchone, db_fetchall, db_commit, join

class AccountModel:
    __select_all = 'SELECT * FROM acct'
    __where_id = 'WHERE accountid = %s'

    @classmethod
    def get_accounts(cls):
        # Fetch all accounts
        # O(n) (where n = len(accounts))
        return db_fetchall(join(cls.__select_all, 'ORDER BY accountname'))
    
    @classmethod
    def get_account(cls, account_id):
        # Gets account information for one account
        # O(1)
        return db_fetchone(join(cls.__select_all, cls.__where_id), 
                           (account_id,))
    
    @staticmethod
    def add_account(name, account_type):
        # Adds one account
        # O(1)
        db_commit("""
                  INSERT INTO acct (accountname, accounttype) 
                  VALUES (%s, %s)
                  """, (name, account_type))
    
    @classmethod
    def edit_account(cls, account_id, account_name, account_type):
        # Edits one account
        # O(1)
        update = 'UPDATE acct'
        db_commit(
            join(update, 'SET accountname = %s', cls.__where_id),
            (account_name, account_id),
            join(update, 'SET accounttype = %s', cls.__where_id),
            (account_type, account_id)
        )
        
    @staticmethod
    def get_account_balance(account_id):
        # Calculate account balance using transaction table
        result = db_fetchone("""
                             SELECT COALESCE(SUM(amount), 0) as balance
                             FROM transact
                             WHERE accountid = %s
                             """, (account_id,))['balance'] 
        # db_fetchone() returns dict with only key 'balance'

        return result
    @classmethod
    def delete(cls, id):
        return db_commit(join('DELETE FROM acct', cls.__where_id), (id,), 
                         return_was_affected=True, return_id=False)