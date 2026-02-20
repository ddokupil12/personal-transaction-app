from db import db_fetchone, db_fetchall, db_commit

class TransactModel:
    @staticmethod
    def get_transactions(per_page=None, offset=0, 
                         search_query=None, return_total=True):
        if per_page is not None:
            transactions = db_fetchall("""
                SELECT t.*, a.accountname, c.categoryname 
                FROM transact t
                JOIN acct a ON t.accountid = a.accountid
                JOIN category c ON t.Categoryid = c.Categoryid
                ORDER BY t.transactiondate DESC, t.transactionid DESC
                LIMIT %s OFFSET %s
            """, (per_page, offset))
        elif search_query is not None:
            transactions = db_fetchall("""
                SELECT t.*, a.accountname, c.categoryname 
                FROM transact t
                JOIN acct a ON t.accountid = a.accountid
                JOIN category c ON t.Categoryid = c.Categoryid
                WHERE t.dscr like %s
                ORDER BY t.transactiondate DESC, t.transactionid DESC
            """, (f'%{search_query}%',))
        else:
            transactions = db_fetchall("""
                SELECT *
                FROM transact t
                INNER JOIN acct a
                ON t.accountid = a.accountid
                INNER JOIN category c
                ON t.categoryid = c.categoryid
                ORDER BY t.transactiondate DESC, t.transactionid DESC
            """)

        if return_total is True: # Get total count for pagination
            total = db_fetchone("""
                                SELECT COUNT(*) as total FROM transact
                                """)['total']
        else:
            total = None

        return transactions, total
        

    @staticmethod
    def get_transaction(transaction_id):
        return db_fetchone("""
                           SELECT * 
                           FROM transact 
                           WHERE transactionid = %s
                           """, [transaction_id])

    @staticmethod
    def add_transaction(account_id, category_id, amount, transaction_date, 
                        description):
        db_commit(
            """
                INSERT INTO transact (accountid, categoryid, amount, 
                    transactiondate, dscr) 
                VALUES (%s, %s, %s, %s, %s)
            """, 
            (
                account_id, category_id, amount, transaction_date, 
                description
            )
        )

    @staticmethod
    def edit_transaction(account_id, category_id, amount, transaction_date,
                         dscr, transaction_id):
        db_commit(
            """
                UPDATE transact 
                SET accountid = %s 
                WHERE transactionid = %s
            """, (account_id, transaction_id),
            """
                UPDATE transact
                SET categoryid = %s
                WHERE transactionid = %s
            """, (category_id, transaction_id),
            """
                UPDATE transact
                SET dscr = %s
                WHERE transactionid = %s
            """, (dscr, transaction_id),
            """
                UPDATE transact
                SET transactiondate = %s
                WHERE transactionid = %s
            """, (transaction_date, transaction_id),
            """
                UPDATE transact
                SET amount = %s
                WHERE transactionid = %s
            """, (amount, transaction_id)
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