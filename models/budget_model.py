from db import db_commit, get_db_connection, db_fetchone, db_fetchall
from .utils import join

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
                budget['actual'] = cursor.fetchone()['actual']

            return budgets
        
    @staticmethod
    def get_budget(budget_id):
        return db_fetchone("""
                           SELECT *
                           FROM budget
                           WHERE budgetid = %s
                           """, (budget_id,))

    @staticmethod
    def add_budget(category_id, budget_year, budget_month, budget_amount):
        db_commit(
            """
                INSERT INTO budget (categoryid, budget_year, 
                budget_month, budget_amount) 
                VALUES (%s, %s, %s, %s)
            """, (category_id, budget_year, budget_month, budget_amount)
        )
    
    @staticmethod
    def edit_budget(budget_id, category_id, budget_year, budget_month, budget_amount):
        update = 'UPDATE budget'
        where_id = 'WHERE budget_id = %s'
        others = db_fetchall(
            """
            SELECT *
            FROM budget
            WHERE categoryid = %s AND budget_year = %s AND budget_month = %s
            """, (category_id, budget_year, budget_month)
        )
        assert others is None, 'Budget is not unique'
        db_commit(
            join(update, 'SET budget_amount = %s', where_id), (budget_amount, budget_id),
            join(update, 'SET category_id = %s', where_id),
            (category_id, budget_id),
            join(update, 'SET budget_year = %s', where_id),
            (budget_year, budget_id),
            join(update, 'SET budget_month = %s', where_id),
            (budget_month, budget_id)
        )