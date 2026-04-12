from utils.db import db_fetchall, db_commit, db_fetchone, join

class CategoryModel:
    __where_id = ' WHERE categoryid = %s'
    __select_all = 'SELECT * FROM category'

    @staticmethod
    def get_categories():
        # Fetch all categories
        return db_fetchall('SELECT * FROM category ORDER BY categoryname')
    
    @classmethod
    def get_category(cls, categoryid):
        return db_fetchone(join(cls.__select_all, cls.__where_id), (categoryid,))

    @classmethod
    def get_category_by_name(cls, name):
        return db_fetchone(
            join(cls.__select_all, 'WHERE categoryname = %s'), 
            (name,)
        )
    
    @staticmethod
    def add_category(name, cat_type):
        return db_commit("""
                         INSERT INTO category (categoryname, type_)
                         VALUES (%s, %s)
                         """, (name, cat_type))
    
    @classmethod
    def edit_category(cls, id, name, cat_type):
        update = 'UPDATE category'
        return db_commit(
            join(update, 'SET categoryname = %s', cls.__where_id), 
            (name, id),
            join(update, 'SET type_ = %s', cls.__where_id), 
            (cat_type, id)
        )