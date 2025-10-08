from .database_utils import get_connection
from .article import Article
from .magazine import Magazine

class Author:
    def __init__(self, id, name):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string")
        self.id = id
        self._name = name

    @property
    def name(self):
        return self._name

    @classmethod
    def new_from_db(cls, row):
        return cls(*row)

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls.new_from_db(row)
        return None

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            self.id = cursor.lastrowid
        else:
            cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
        conn.commit()
        conn.close()

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article.new_from_db(row) for row in rows]

    def magazines(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT magazines.* FROM magazines JOIN articles ON magazines.id = articles.magazine_id WHERE articles.author_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Magazine.new_from_db(row) for row in rows]

    def add_article(self, magazine, title):
        article = Article(None, title, "", self, magazine)
        article.save()
        return article

    def topic_areas(self):
        magazines = self.magazines()
        categories = set(m.category for m in magazines)
        return list(categories)
