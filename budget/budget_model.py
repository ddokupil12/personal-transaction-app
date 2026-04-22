from utils.db import db_commit, get_db_connection, db_fetchone, db_fetchall, join

class BudgetModel:
    __select_all = 'SELECT * FROM budget'
    __where_id = 'WHERE budgetid = %s'

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
        
    @classmethod
    def get_budget(cls, budget_id):
        return db_fetchone(join(cls.__select_all, cls.__where_id), (budget_id,))

    @staticmethod
    def add_budget(category_id, budget_year, budget_month, budget_amount):
        db_commit(
            """
                INSERT INTO budget (categoryid, budget_year, 
                budget_month, budget_amount) 
                VALUES (%s, %s, %s, %s)
            """, (category_id, budget_year, budget_month, budget_amount)
        )
    
    @classmethod
    def edit_budget(cls, budget_id, category_id, budget_year, budget_month, budget_amount):
        update = 'UPDATE budget'
        query = join(
            cls.__select_all, 
            'WHERE categoryid = %s AND budget_year = %s AND budget_month = %s'
        )
        others = db_fetchall(query, (category_id, budget_year, budget_month))
        is_unique = all([i['budgetid'] != budget_id for i in others])
        assert is_unique, 'Budget is not unique'
        db_commit(
            join(update, 'SET budget_amount = %s', cls.__where_id), 
            (budget_amount, budget_id),
            join(update, 'SET categoryid = %s', cls.__where_id),
            (category_id, budget_id),
            join(update, 'SET budget_year = %s', cls.__where_id),
            (budget_year, budget_id),
            join(update, 'SET budget_month = %s', cls.__where_id),
            (budget_month, budget_id)
        )

    @classmethod
    def delete(cls, id):
        return db_commit(join('DELETE FROM budget', cls.__where_id), (id,), 
                         return_was_affected=True, return_id=False)