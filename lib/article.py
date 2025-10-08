from .database_utils import get_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    @classmethod
    def new_from_db(cls, row):
        return cls(*row)

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
            cursor.execute("INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)", (self.title, self.content, self.author_id, self.magazine_id))
            self.id = cursor.lastrowid
        else:
            cursor.execute("UPDATE articles SET title = ?, content = ?, author_id = ?, magazine_id = ? WHERE id = ?", (self.title, self.content, self.author_id, self.magazine_id, self.id))
        conn.commit()
        conn.close()
