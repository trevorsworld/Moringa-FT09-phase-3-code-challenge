from __init__ import CURSOR, CONN


class Author:
    def __init__(self, id = None, name = None):
        self.id = id
        self.name = name

        
    def __repr__(self):
        return f'<Author {self.name}>'
    
    # from database.setup import create_tables

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise TypeError("Id must be of type int")
        self._id = value
        
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Name must be a non-empty string")
        if not hasattr(self, '_name'):
            self._name = value
        else:
            raise AttributeError("Name cannot be changed after instantiation")
        

    def articles(self):
        from models.article import Article
        sql = """
            SELECT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id
            FROM articles
            INNER JOIN authors
            ON authors.id = articles.author_id
            WHERE authors.id = ?
        """
        CURSOR.execute(sql, (self.id,))
        rows = CURSOR.fetchall()
        return [Article(row[0], row[1], row[2], row[3], row[4]) for row in rows]


    def magazines(self):
        from models.magazine import Magazine
        sql = """
            SELECT DISTINCT magazines.id, magazines.name, magazines.category
            FROM magazines
            INNER JOIN articles
            ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        """
        CURSOR.execute(sql, (self.id,))
        rows = CURSOR.fetchall()
        return [Magazine(row[0], row[1], row[2]) for row in rows]
    

    def save(self):
        if self.id is None:
            sql = """
                INSERT INTO authors (name)
                VALUES (?)
            """
            CURSOR.execute(sql, (self.name,))
            CONN.commit()
            self.id = CURSOR.lastrowid
        else:
            sql = """
                UPDATE authors
                SET name = ?
                WHERE id = ?
            """
            CURSOR.execute(sql, (self.name, self.id))
            CONN.commit()


    @classmethod
    def instance_from_db(cls, row):
        return cls(row[0], row[1])
    

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM authors
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]