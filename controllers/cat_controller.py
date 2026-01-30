from models.category_model import CategoryModel

class CatController:
    @staticmethod
    def categories():
        return CategoryModel.get_categories()
    
    @staticmethod
    def add_category(name, cat_type): 
        assert cat_type in ['Income', 'Expense']
        CategoryModel.add_category(name, cat_type)