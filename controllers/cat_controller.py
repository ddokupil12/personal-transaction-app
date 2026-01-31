from models.category_model import CategoryModel

__all__ = ['CatController']

class CatController:
    @staticmethod
    def categories():
        return CategoryModel.get_categories()
    
    @staticmethod
    def add_category(name, cat_type):
        """
        Controller to add a category
        
        :param name: str
        :param cat_type: 'Income' | 'Expense'
        """
        assert cat_type in ['Income', 'Expense']
        CategoryModel.add_category(name, cat_type)