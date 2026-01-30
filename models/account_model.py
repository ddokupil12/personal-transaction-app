from db import db_fetchone, db_fetchall, db_commit

class AccountModel:
    @staticmethod
    def get_accounts():
        """Fetch all accounts"""
        return db_fetchall('SELECT * FROM acct ORDER BY accountname')
    
    @staticmethod
    def get_account_balance(account_id):
        """Calculate account balance using transaction table"""
        result = db_fetchone("""
                             SELECT COALESCE(SUM(amount), 0) as balance
                             FROM transact
                             WHERE accountid = %s
                             """, (account_id,))['balance'] 
        # db_fetchone() returns dict with only key 'balance'

        return result
    
    @staticmethod
    def get_account(account_id):
        return db_fetchone("""
                           SELECT * 
                           FROM acct
                           WHERE accountid = %s
                           """, [account_id])
    
    @staticmethod
    def add_account(name, account_type):
        db_commit("""
                  INSERT INTO acct (accountname, accounttype) 
                  VALUES (%s, %s)
                  """, (name, account_type))
    
    @staticmethod
    def edit_account(account_id, account_name, account_type):
        db_commit(
            """
                UPDATE acct
                SET accountname = %s
                WHERE accountid = %s
            """, (account_name, account_id),
            """
                UPDATE acct
                SET accounttype = %s
                WHERE accountid = %s
            """, (account_type, account_id)
        )