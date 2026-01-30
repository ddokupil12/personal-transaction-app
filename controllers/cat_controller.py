from models.category_model import CategoryModel

class CatController:
    @staticmethod
    def categories():
        return CategoryModel.get_categories()
    
    @staticmethod
    def add_category(name, cat_type):
        """
        Docstring for add_category
        
        :param name: str
        :param cat_type: 'Income' | 'Expense'
        """
        assert cat_type in ['Income', 'Expense']
        CategoryModel.add_category(name, cat_type)