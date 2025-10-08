from .database_utils import get_connection
from .author import Author
from .magazine import Magazine

class Article:
    def __init__(self, id, title, content, author, magazine):
        if not isinstance(title, str) or len(title) == 0:
            raise ValueError("Title must be a non-empty string")
        self.id = id
        self._title = title
        self.content = content
        self.author = author
        self.magazine = magazine

    @property
    def title(self):
        return self._title

    @classmethod
    def new_from_db(cls, row):
        id, title, content, author_id, magazine_id = row
        author = Author.find_by_id(author_id)
        magazine = Magazine.find_by_id(magazine_id)
        return cls(id, title, content, author, magazine)

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls.new_from_db(row)
        return None

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)", (self.title, self.content, self.author.id, self.magazine.id))
            self.id = cursor.lastrowid
        else:
            cursor.execute("UPDATE articles SET title = ?, content = ?, author_id = ?, magazine_id = ? WHERE id = ?", (self.title, self.content, self.author.id, self.magazine.id, self.id))
        conn.commit()
        conn.close()
