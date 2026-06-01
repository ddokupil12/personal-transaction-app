from utils.db import db_fetchall, db_commit, db_fetchone

class CashflowModel:
    @staticmethod
    def get_cashflows(per_page=None, offset=None, return_total=True):
        cashflows = db_fetchall("""
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
            ORDER BY t.transactiondate DESC, t.transactionid DESC
            LIMIT %s OFFSET %s
        """, (per_page, offset))
        
        if return_total is True:
            total = db_fetchone("""
                SELECT COUNT(*) as total FROM cashflow
            """)['total']
            return cashflows, total
        else:
            return cashflows

    @staticmethod
    def add_cashflow(expenseid, incomeid, type_):
        db_commit("""
            INSERT INTO cashflow (expense, income, type_) 
            VALUES (%s, %s, %s)
        """, (expenseid, incomeid, type_), return_id=False)

    @staticmethod
    def get_cashflows_by_type(type_):
        return db_fetchall("""
            SELECT t.transactionid as expensetransactionid,
                t.transactiondate as expensedate, t.amount as expenseamount, 
                t.dscr as expensedscr, t.categoryid as expensecategory,
                t2.transactionid as incometransactionid,
                t2.amount as incomeamount, t2.transactiondate as incomedate, 
                t2.dscr as incomedscr, t2.categoryid as incomecategory, r1.type_
            FROM transact t
            JOIN cashflow r1 on t.transactionid = r1.expense
            JOIN transact t2 on r1.income = t2.transactionid
            WHERE r1.type_ = %s
            ORDER BY t.transactiondate DESC, t.transactionid DESC;
        """, (type_,))
    
    @staticmethod
    def get_expense_ids():
        return db_fetchall('SELECT expense FROM cashflow')
    
    @staticmethod
    def get_income_ids():
        return db_fetchall('SELECT income FROM cashflow')