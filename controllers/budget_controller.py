from decimal import Decimal
from datetime import datetime

from models.budget_model import BudgetModel

class BudgetController:
    @staticmethod
    def budgets(year, month):
        """
        Controller to get all budgets
        
        :param year: int (budget year)
        :param month: int (budget month)
        """
        totalSpent = 0
        budgetSpending = 0
        budgetIncome = 0
        budgets = BudgetModel.get_budgets(year, month)
        for budget in budgets:
            actual = budget['actual']
            absActual = abs(actual) # Budgets are positive numbers
            budget['remaining'] = budget['budget_amount'] - absActual
            if budget['type_'] == 'Expense':
                budgetSpending += budget['budget_amount']
                if actual > 0: # Handle expense accounts with income
                    totalSpent += actual
                    budget['actual'] = 0 - actual
                    budget['remaining'] = budget['budget_amount'] + absActual
                else: # Handle expense accounts normally
                    totalSpent += absActual
                    budget['actual'] = absActual

            else: # Handle income accounts
                budgetIncome += budget['budget_amount']
                budget['actual'] = absActual


        # Summary of expenses
        summary = {'total_budgeted': budgetSpending,
                'total_spent': totalSpent,
                'total_remaining': budgetSpending - totalSpent
                }
            
        return budgets, summary
        
    @staticmethod
    def add_budget(category_id, budget_year, budget_month, amount):
        """
        Controller for adding budgets
        
        :param category_id: int
        :param budget_year: int
        :param budget_month: int
        :param amount: Decimal

        Raises AssertionError when:
            amount == 0
            budget_month is not one of the 12 months
            budget_year is not in the 2020s
        """
        budget_amount = Decimal(amount)
        BudgetModel.add_budget(category_id, budget_year, budget_month, 
                               budget_amount)