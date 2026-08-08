from utils.db import commit, get_db_connection, Fetch, join

class BudgetModel:
    __select_all = 'SELECT * FROM budget'
    __where_id = 'WHERE budgetid = %s'

    @staticmethod
    def __get_existing_budgets(year, month):
        # Gets all existing budgets for the given year and month
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""SELECT b.*, c.*
                           FROM budget b
                           RIGHT JOIN category c ON b.categoryid = c.categoryid
                           WHERE budget_year = %s 
                           AND budget_month = %s
                           ORDER BY c.categoryname
                           """, (year, month))
            budgets = cursor.fetchall()

        return budgets

    @staticmethod
    def __list_to_cat_map(lst):
        # Takes a list of dictionaries and returns a dictionary with 
        # categoryid as the keys
        # Helper function for _calculate_actual_budgets()
        map_ = {}
        for i in lst:
            key = i['categoryid']
            map_[key] = i

        return map_

    @classmethod
    def __calculate_actual_budgets(cls, year, month, budgets, categories):
        # Calculates actual spending for each budget
        # If a budget does not exist for the given category, year, and month, 
        # one will be created.
        # Returns all spending and budget amounts for all categories in the 
        # given year and month.
        results = []

        # Creating indicies for categories and budgets by categoryid
        budgets_by_category = cls.__list_to_cat_map(budgets)
        categories_by_id = cls.__list_to_cat_map(categories)

        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)

            # Calculate actual spending for each category
            category_ids = [i['categoryid'] for i in categories]
            for id in category_ids:
                cursor.execute("""SELECT COALESCE(SUM(amount), 0) as actual
                               FROM transact t
                               WHERE t.categoryid = %s 
                               AND YEAR(t.transactiondate) = %s 
                               AND MONTH(t.transactiondate) = %s
                               """, (id, year, month))

                # execute() returns dict with only key 'actual'
                query_result = cursor.fetchone()['actual']

                try: # Add budget to dictionary
                    budget = budgets_by_category[id]
                except KeyError: # Create budget with proper formatting
                    budget_id = cls.__add_budget(id, year, month, 0.0,
                                               return_id=True)
                    budget = cls.get_budget(budget_id)
                    category = categories_by_id[id]
                    budget['type_'] = category['type_']
                    budget['categoryname'] = category['categoryname']

                budget['actual'] = query_result
                results.append(budget)

        return results

    @classmethod
    def get_budgets(cls, year, month, categories):
        # Get all budgets and spending for the current year and month
        budgets = cls.__get_existing_budgets(year, month)
        budgets = cls.__calculate_actual_budgets(year, month, budgets, 
                                                categories)
        budgets = sorted(budgets, key=lambda x: x['categoryname'])
        return budgets

    @classmethod
    def get_budget(cls, budget_id):
        return Fetch.one(join(cls.__select_all, cls.__where_id), (budget_id,))

    @staticmethod
    def __add_budget(category_id, budget_year, budget_month, budget_amount, 
                    return_id=False):
        return commit(
            """
                INSERT INTO budget (categoryid, budget_year, 
                budget_month, budget_amount) 
                VALUES (%s, %s, %s, %s)
            """, 
            (
                category_id, budget_year, budget_month, budget_amount
            ), 
            return_id=return_id
        )
    
    @classmethod
    def edit_budget(cls, budget_id, category_id, budget_year, budget_month, 
                    budget_amount):
        update = 'UPDATE budget'
        old = cls.get_budget(budget_id)
        conditions = all([
            old['categoryid'] == category_id, 
            old['budget_year'] == budget_year, 
            old['budget_month'] == budget_month
        ])
        if conditions is False: 
            # This should raise an error since budgets are auto-generated
            query = join(
                cls.__select_all, 
                'WHERE categoryid = %s AND budget_year = %s AND budget_month = %s'
            )
            others = Fetch.all(query, (category_id, budget_year, budget_month))
            is_unique = all([i['budgetid'] != budget_id for i in others])
            assert is_unique, 'Budget is not unique' # Helpful error message

            # Now save everything to the database
            commit( # This is ok being separate because it usually won't run
                join(update, 'SET categoryid = %s', cls.__where_id),
                (category_id, budget_id),
                join(update, 'SET budget_year = %s', cls.__where_id),
                (budget_year, budget_id),
                join(update, 'SET budget_month = %s', cls.__where_id),
                (budget_month, budget_id)            
            )

        commit(
            join(update, 'SET budget_amount = %s', cls.__where_id), 
            (budget_amount, budget_id),
        )

    @classmethod
    def delete(cls, id):
        return commit(join('DELETE FROM budget', cls.__where_id), (id,), 
                      return_was_affected=True, return_id=False)
    
    @classmethod
    def clear_cache(cls):
        # Delete all budgets with a budget amount of 0.
        budgets = Fetch.all('SELECT * FROM budget WHERE budget_amount = 0')
        for i in budgets:
            yield cls.delete(i['budgetid'])