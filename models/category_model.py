from config import db_fetchall, db_commit

class CategoryModel:
    @staticmethod
    def get_categories():
        """Fetch all categories"""
        return db_fetchall('SELECT * FROM category ORDER BY categoryname')
    
    @staticmethod
    def add_category(name, cat_type):
        db_commit("""
                  INSERT INTO category (categoryname, type_) 
                  VALUES (%s, %s)
                  """, (name, cat_type))