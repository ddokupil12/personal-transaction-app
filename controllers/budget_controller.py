from decimal import Decimal

from models.budget_model import BudgetModel

class BudgetController:
    @staticmethod
    def budgets(year, month):
        totalSpent = 0
        budgetSpending = 0
        budgetIncome = 0
        budgets = BudgetModel.get_budgets(year, month)
        for budget in budgets:
            actual = budget['actual']
            absActual = abs(actual)
            budget['remaining'] = budget['budget_amount'] - absActual
            if budget['type_'] == 'Expense':
                budgetSpending += budget['budget_amount']
                if actual > 0:
                    totalSpent += actual
                    budget['actual'] = 0 - actual
                    budget['remaining'] = budget['budget_amount'] + absActual
                else:
                    totalSpent += absActual
                    budget['actual'] = absActual

            else:
                budgetIncome += budget['budget_amount']
                budget['actual'] = absActual


        summary = {'total_budgeted': budgetSpending,
                'total_spent': totalSpent,
                'total_remaining': budgetSpending - totalSpent
                }
            
        return budgets, summary
        
    @staticmethod
    def add_budget(category_id, budget_year, budget_month, amount):
        budget_amount = Decimal(amount)
        BudgetModel.add_budget(category_id, budget_year, budget_month, 
                               budget_amount)