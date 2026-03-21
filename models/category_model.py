from db import db_fetchall, db_commit, db_fetchone

class CategoryModel:
    @staticmethod
    def get_categories():
        # Fetch all categories
        return db_fetchall('SELECT * FROM category ORDER BY categoryname')
    
    @staticmethod
    def get_category(categoryid):
        return db_fetchone("""SELECT * FROM category WHERE categoryid = %s""", (categoryid,))

    @staticmethod
    def get_category_by_name(name):
        return db_fetchone(
            """SELECT * FROM category WHERE categoryname = %s""", 
            (name,)
        )
    
    @staticmethod
    def add_category(name, cat_type):
        return db_commit("""
                  INSERT INTO category (categoryname, type_) 
                  VALUES (%s, %s)
                  """, (name, cat_type))
    
    @staticmethod
    def edit_category(id, name, cat_type):
        return db_commit("""
                  UPDATE category
                  SET categoryname = %s
                  WHERE categoryid = %s
                  """, (name, id),
                  """
                  UPDATE category
                  SET type_ = %s
                  WHERE categoryid = %s
                  """, (cat_type, id)
        )