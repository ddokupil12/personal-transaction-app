from utils.db import Fetch, commit, join
from utils.message import Model

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
    def get_transactions(cls, per_page=None, offset=0, search_query=None,
                         account_ids=None, category_ids=None, return_total=True):
        # Build a WHERE clause from whichever filters are supplied. Every
        # active filter is ANDed together, so search, account, and category
        # can all narrow the result set at once.
        conditions = []
        where_params = []
        if search_query:
            conditions.append('t.dscr LIKE %s')
            where_params.append(f'%{search_query}%')
            # Searches are: WHERE t.dscr LIKE '%sample%'
        if account_ids:
            placeholders = ','.join(['%s'] * len(account_ids))
            conditions.append(f't.accountid IN ({placeholders})')
            where_params.extend(account_ids)
        if category_ids:
            placeholders = ','.join(['%s'] * len(category_ids))
            conditions.append(f't.categoryid IN ({placeholders})')
            where_params.extend(category_ids)
        # where_conditions = ' AND '.join(where_params)
        # where_clause = (' '.join(['WHERE'], where_conditions))
        # where = where_clause if conditions else ''
        where = 'WHERE ' + ' AND '.join(conditions) if conditions else ''

        parts = [cls.__base]
        if where:
            parts.append(where)
        parts.append(cls.__order)
        fetch_params = list(where_params)
        if per_page is not None and offset is not None:
            parts.append('LIMIT %s OFFSET %s')
            fetch_params.extend([per_page, offset])

        if fetch_params:
            transactions = Fetch.all(join(*parts), tuple(fetch_params))
        else:
            transactions = Fetch.all(join(*parts))

        if return_total is True: # Get total count for pagination
            total_query = 'SELECT COUNT(*) as total FROM transact t'
            if where:
                total = Fetch.one(join(total_query, where),
                                  tuple(where_params))['total']
            else:
                total = Fetch.one(total_query)['total']
            return transactions, total
        else:
            return transactions
        
    @classmethod
    def filter(cls, ids, model):
        len_ = len(ids)

        # Specify model
        # 50 is a magic number?
        # assert len_ < 50, 'Too many selected'

        # What changes based on how many filters there are
        db_var = None
        if model == Model.acct:
            db_var = 't.accountid'
        elif model == Model.category:
            db_var = 't.categoryid'
        else:
            raise ValueError()

        placeholders = ','.join(['%s'] * len_)
        query = join(
            cls.__base,
            f'WHERE {db_var} IN ({placeholders})',
            cls.__order
        )
        return Fetch.all(query, ids)

    @classmethod
    def get_transaction(cls, transaction_id):
        return Fetch.one(join(
            'SELECT * FROM transact', cls.__where_id
        ), [transaction_id])

    @staticmethod
    def add_transaction(account_id, category_id, amount, date_, 
                        description):
        return commit(
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
        return commit(
            join(update, 'SET accountid = %s', cls.__where_id), 
            (account_id, id),
            join(update, 'SET categoryid = %s', cls.__where_id), 
            (category_id, id),
            join(update, 'SET dscr = %s', cls.__where_id), 
            (dscr, id),
            join(update, 'SET transactiondate = %s', cls.__where_id), 
            (date_, id),
            join(update, 'SET amount = %s', cls.__where_id), 
            (amount, id)
        )
    
    @staticmethod
    def get_account_balance(account_id):
        # Calculate account balance using transaction table
        result = Fetch.one("""SELECT COALESCE(SUM(amount), 0) as balance
                             FROM transact
                             WHERE accountid = %s
                             """, (account_id,))['balance'] 
        # db_fetchone() returns dict with only key 'balance'

        return result
    
    @classmethod
    def delete(cls, id):
        return commit(join('DELETE FROM transact', cls.__where_id), (id,), 
                         return_was_affected=True, return_id=False)