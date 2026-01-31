from models import CategoryModel

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
        types = ['Income', 'Expense']
        types_fmt = str(types).replace('[', '').replace(']', '')
        error_message = f'Category type must be one of: {types_fmt}'
        assert cat_type in types, error_message
        CategoryModel.add_category(name, cat_type)