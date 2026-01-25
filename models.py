from db import db_fetchone, db_fetchall, db_commit, get_db_connection

class AccountModel:
    @staticmethod
    def get_accounts():
        """Fetch all accounts"""
        return db_fetchall('SELECT * FROM acct ORDER BY accountname')
    
    @staticmethod
    def get_account_balance(account_id):
        """Calculate account balance using relational method"""
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
    
class CategoryModel:
    @staticmethod
    def get_categories():
        """Fetch all categories"""
        return db_fetchall('SELECT * FROM category ORDER BY categoryname')
    
    @staticmethod
    def add_category(name, cat_type):
        db_commit("""
                  INSERT INTO category (categoryname, type_) 
                  VALUES (%s, %s)
                  """, (name, cat_type))
    
class TransactModel:
    @staticmethod
    def get_transactions(per_page=None, offset=None):
        if per_page and offset:
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
    def get_recent_transactions():
        return db_fetchall("""
            SELECT t.*, a.accountname, c.categoryname 
            FROM transact t
            JOIN acct a ON t.accountid = a.accountid
            JOIN category c ON t.CategoryID = c.CategoryID
            ORDER BY t.TransactionDate DESC, t.TransactionID DESC
            LIMIT 10
        """)
        
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
                account_id, category_id,amount, transaction_date, 
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


class BudgetModel:
    @staticmethod
    def get_budgets(year, month):
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                           SELECT b.*, c.categoryname, c.type_
                           FROM budget b
                           JOIN category c ON b.categoryid = c.categoryid
                           WHERE b.budget_year = %s AND b.budget_month = %s
                           ORDER BY c.categoryname
                           """, (year, month))
            budgets = cursor.fetchall()
            # Calculate actual spending for each budget
            for budget in budgets:
                cursor.execute("""
                               SELECT COALESCE(SUM(amount), 0) as actual
                               FROM transact t
                               WHERE t.categoryid = %s 
                               AND YEAR(t.transactiondate) = %s 
                               AND MONTH(t.transactiondate) = %s
                               """, (budget['categoryid'], year, month))
                
                # execute() returns dict with only key 'actual'
                actual = cursor.fetchone()['actual']
                budget['actual'] = actual

            return budgets
        
    
    @staticmethod
    def add_budget(category_id, budget_year, budget_month, budget_amount):
        db_commit(
            """
                INSERT INTO budget (categoryid, budget_year, 
                budget_month, budget_amount) 
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE budget_amount = %s
            """,
            (
                category_id, budget_year, budget_month, budget_amount, 
                budget_amount
            )
        )


        
class CashflowModel:
    @staticmethod
    def get_cashflows():
        return db_fetchall("""
            SELECT t.transactionid as expensetransactionid, 
                a.accountname as expenseacct, c.categoryname as expensecat, 
                t.transactiondate as expensedate, t.amount as expenseamount, 
                t.dscr as expensedscr, r1.*, 
                t2.transactionid as incometransactionid, 
                a2.accountname as incomeacct, c2.categoryname as incomecat, 
                t2.amount as incomeamount, t2.transactiondate as incomedate, 
                t2.dscr as incomedscr
            FROM transact t
            JOIN acct a ON t.accountid = a.accountid
            JOIN category c ON t.CategoryID = c.CategoryID
            JOIN cashflow r1 on t.transactionid = r1.expense
            JOIN transact t2 on r1.income = t2.transactionid
            JOIN acct a2 on t2.accountid = a2.accountid
            JOIN category c2 on t2.categoryid = c2.categoryid
            ORDER BY t.transactiondate DESC, t.transactionid DESC;
        """)

    @staticmethod
    def add_cashflow(expenseid, incomeid, type_):
        db_commit("""
            INSERT INTO cashflow (expense, income, type_) VALUES
            (%s, %s, %s)
        """, (expenseid, incomeid, type_))