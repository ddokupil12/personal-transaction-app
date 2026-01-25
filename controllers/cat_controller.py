from models.category_model import CategoryModel

class CatController:
    @staticmethod
    def categories():
        return CategoryModel.get_categories()
    
    @staticmethod
    def add_category(name, cat_type): 
        CategoryModel.add_category(name, cat_type)