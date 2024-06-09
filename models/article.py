from __init__ import CURSOR, CONN

class Article:
    def __init__(self, id = None, title = None, content = None, author_id = None, magazine_id = None):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f'<Article {self.title}>'
    
    from database.setup import create_tables
    
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise TypeError("Id must be of type int")
        self._id = value

    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, value):
        if hasattr(self, "_title"):
            raise AttributeError("Title cannot be changed")
        else:
            if isinstance(value, str):
                if 5 <= len(value) <= 50:
                    self._title = value
                else:
                    raise ValueError("Title must be between 5 and 50 characters")
            else:
                raise TypeError("Title must be a string")
            
    @property
    def content(self):
        return self._content
    @content.setter
    def content(self, value):
        if not isinstance(value, str):
            raise TypeError("Content must be of type str")
        self._content = value

    @property
    def author_id(self):
        return self._author_id
    @author_id.setter
    def author_id(self, value):
        if not isinstance(value, int):
            raise TypeError("Author ID must be of type int")
        self._author_id = value

    @property
    def magazine_id(self):
        return self._magazine_id
    @magazine_id.setter
    def magazine_id(self, value):
        if not isinstance(value, int):
            raise TypeError("Magazine ID must be of type int")
        self._magazine_id = value

    @property
    def author(self):
        from models.author import Author
        sql = """
            SELECT authors.id, authors.name
            FROM authors
            INNER JOIN articles
            ON authors.id = articles.author_id
            WHERE articles.id = ?
        """
        CURSOR.execute(sql, (self.id,))
        row = CURSOR.fetchone()
        if row:
            return Author(row[0], row[1])
        else:
            return None
        
    @property
    def magazine(self):
        from models.magazine import Magazine
        sql = """
            SELECT magazines.id, magazines.name, magazines.category
            FROM magazines
            INNER JOIN articles
            ON magazines.id = articles.magazine_id
            WHERE articles.id = ?
        """
        CURSOR.execute(sql, (self.id,))
        row = CURSOR.fetchone()
        if row:
            return Magazine(row[0], row[1], row[2])
        else:
            return None


    def save(self):
        if self.id is None:
            sql = """
                INSERT INTO articles (title, content, author_id, magazine_id)
                VALUES (?, ?, ?, ?)
            """
            CURSOR.execute(sql, (self.title, self.content, self.author_id, self.magazine_id))
            CONN.commit()
            self.id = CURSOR.lastrowid
        else:
            sql = """
                UPDATE articles
                SET title = ?, content = ?, author_id = ?, magazine_id = ?
                WHERE id = ?
            """
            CURSOR.execute(sql, (self.title, self.content, self.author_id, self.magazine_id, self.id))
            CONN.commit()
            

    @classmethod
    def instance_from_db(cls, row):
        return cls(row[0], row[1],row[2],row[3],row[4])

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM articles
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    