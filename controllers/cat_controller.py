__all__ = ['CatController']

from models import CategoryModel

class CatController:
    @staticmethod
    def categories():
        return CategoryModel.get_categories()

    @staticmethod
    def get_category(id):
        return CategoryModel.get_category(id)
    
    @staticmethod
    def check_type(cat_type):
        types = ['Income', 'Expense']
        types_fmt = str(types).replace('[', '').replace(']', '')
        error_message = f'Category type must be one of: {types_fmt}'
        assert cat_type in types, error_message       

    @classmethod
    def add_category(cls, name, cat_type):
        # Controller to add a category
        # 
        # :param name: str
        # :param cat_type: 'Income' | 'Expense'
        cls.check_type(cat_type)
        CategoryModel.add_category(name, cat_type)

    @classmethod
    def edit_category(cls, id, name, cat_type):
        cls.check_type(cat_type)
        CategoryModel.edit_category(id, name, cat_type)