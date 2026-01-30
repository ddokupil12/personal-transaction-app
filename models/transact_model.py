from db import db_fetchone, db_fetchall, db_commit, get_db_connection

class TransactModel:
    @staticmethod
    def get_transactions(per_page=None, offset=0):
        if per_page is not None:
            print('if true')
            with get_db_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT t.*, a.accountname, c.categoryname 
                    FROM transact t
                    JOIN acct a ON t.accountid = a.accountid
                    JOIN category c ON t.Categoryid = c.Categoryid
                    ORDER BY t.transactiondate DESC, t.transactionid DESC
                    LIMIT %s OFFSET %s
                """, (per_page, offset))
                transactions = cursor.fetchall()

        else:
            print('if false')
            transactions = db_fetchall("""
                SELECT *
                FROM transact t
                INNER JOIN acct a
                ON t.accountid = a.accountid
                INNER JOIN category c
                ON t.categoryid = c.categoryid
                ORDER BY t.transactiondate DESC, t.transactionid DESC
            """)


        # Get total count for pagination
        total = db_fetchone("SELECT COUNT(*) as total FROM transact")['total']

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