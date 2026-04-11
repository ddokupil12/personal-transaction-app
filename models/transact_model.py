from db import db_fetchone, db_fetchall, db_commit

class TransactModel:
    __base = """
            SELECT t.*, a.accountname, c.categoryname 
            FROM transact t
            JOIN acct a ON t.accountid = a.accountid
            JOIN category c ON t.Categoryid = c.Categoryid
        """
    __order = 'ORDER BY t.transactiondate DESC, t.transactionid DESC'
    __where_id = 'WHERE transactionid = %s'
    
    @classmethod
    def get_transactions(cls, per_page=None, offset=0, 
                         search_query=None, return_total=True):
        # order = 'ORDER BY t.transactiondate DESC, t.transactionid DESC'
        search = 'WHERE t.dscr like %s'
        limit = 'LIMIT %s OFFSET %s'
        if all([per_page is not None, 
                offset is not None, 
                search_query is not None
                ]):
            transactions = db_fetchall(' '.join([
                cls.__base, 
                search, 
                cls.__order, 
                limit
            ]), (f'%{search_query}%', per_page, offset))
        elif per_page is not None and offset is not None:
            transactions = db_fetchall(' '.join([cls.__base, 
                                                 cls.__order, 
                                                 limit
                                                 ]), (per_page, offset))
        elif search_query is not None:
            transactions = db_fetchall(' '.join([cls.__base, 
                                                 search, 
                                                 cls.__order
                                                 ]), (f'%{search_query}%',))
        else:
            transactions = db_fetchall(' '.join([cls.__base, cls.__order]))

        if return_total is True: # Get total count for pagination
            total = db_fetchone("""
                                SELECT COUNT(*) as total FROM transact
                                """)['total']
            return transactions, total
        else:
            return transactions
        
    @classmethod
    def filter_category(cls, categories):
        len_ = len(categories)
        assert len_ < 50, "Too many categories selected"
        placeholders = ','.join(['%s'] * len_)
        query = ' '.join([
            cls.__base, 
            f'WHERE c.categoryid IN ({placeholders})', 
            cls.__order
        ])
        return db_fetchall(query, categories)

    @staticmethod
    def get_transaction(transaction_id):
        return db_fetchone("""SELECT * FROM transact""", [transaction_id])

    @staticmethod
    def add_transaction(account_id, category_id, amount, date_, 
                        description):
        return db_commit(
            """
                INSERT INTO transact (accountid, categoryid, amount, 
                    transactiondate, dscr) 
                VALUES (%s, %s, %s, %s, %s)
            """, 
            (account_id, category_id, amount, date_, description)
        )

    @classmethod
    def edit_transaction(cls, account_id, category_id, amount, date_,
                         dscr, id):
        update = 'UPDATE transact'
        return db_commit(
            ' '.join([
                update, 
                'SET accountid = %s', 
                cls.__where_id
            ]), (account_id, id),
            ' '.join([
                update, 
                'SET categoryid = %s', 
                cls.__where_id
            ]), (category_id, id),
            ' '.join([update, 'SET dscr = %s', cls.__where_id]), (dscr, id),
            ' '.join([
                update, 
                'SET transactiondate = %s', 
                cls.__where_id
            ]), (date_, id),
            ' '.join([update, 'SET amount = %s', cls.__where_id]), (amount, id)
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