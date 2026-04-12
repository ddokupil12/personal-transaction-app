__all__ = ['BudgetController']

from decimal import Decimal

from models import BudgetModel

class BudgetController:
    @staticmethod
    def budgets(year, month):
        # Controller to get all budgets
        # :param year: int (budget year)
        # :param month: int (budget month)
        totalSpent = 0
        budgetSpending = 0
        budgetIncome = 0
        total_income = 0
        budgets = BudgetModel.get_budgets(year, month)
        for budget in budgets:
            actual = budget['actual'] # Actual expenses are negative
            absActual = abs(actual) # Budgets are positive numbers
            budget['remaining'] = budget['budget_amount'] - absActual
            if budget['type_'] == 'Expense': # Handle expense categories
                budgetSpending += budget['budget_amount']
                if actual > 0: # Handle expense categories with income
                    totalSpent -= actual
                    budget['actual'] = 0 - actual # Show amount as negative
                    budget['remaining'] = budget['budget_amount'] + absActual
                else: # Handle expense categories normally
                    totalSpent += absActual
                    budget['actual'] = absActual

            else: # Handle income categories 
                budgetIncome += budget['budget_amount']
                total_income += budget['actual']

        # Summary of expenses
        summary = {'total_budgeted': budgetSpending,
                   'total_spent': totalSpent,
                   'total_remaining': budgetSpending - totalSpent,
                   'budget_income': budgetIncome,
                   'total_income': total_income,
                   'total_remaining_income': budgetIncome - total_income}
            
        return budgets, summary
        
    @staticmethod
    def get_budget(budget_id):
        return BudgetModel.get_budget(budget_id)

    @staticmethod
    def assert_budget(budget_year, budget_month, amount):
        budget_amount = Decimal(amount)
        assert budget_amount != 0, 'amount must be nonzero'
        budget_month_msg = 'month must be between 1-12'
        assert budget_month >= 1 and budget_month <= 12, budget_month_msg
        budget_year_msg = 'year must be between 2020-2030'
        assert budget_year >= 2020 and budget_year <= 2030, budget_year_msg
        return budget_amount

    @classmethod
    def add_budget(cls, category_id, budget_year, budget_month, amount):
        # Controller for adding budgets
        # 
        # :param category_id: int
        # :param budget_year: int
        # :param budget_month: int
        # :param amount: Decimal

        # Raises AssertionError when:
        #     amount == 0
        #     budget_month is not one of the 12 months
        #     budget_year is not in the 2020s
        budget_amount = cls.assert_budget(budget_year, budget_month, amount)
        BudgetModel.add_budget(category_id, budget_year, budget_month, 
                               budget_amount)
        
    @classmethod
    def edit_budget(cls, budget_id, categoryid, budget_year, budget_month, amount):
        budget_amount = cls.assert_budget(budget_year, budget_month, amount)
        BudgetModel.edit_budget(budget_id, categoryid, budget_year, budget_month, budget_amount)