"""
Article module for managing article entities in the magazine database.

This module defines the Article class, which represents an article in the system.
Articles have a title (read-only), content, and belong to an author and a magazine.
The author and magazine are stored as object references for easy access.
"""

from .database_utils import get_connection

class Article:
    """
    Represents an article in the magazine system.

    Articles have a unique ID, a title (read-only after creation), content,
    and references to their author and magazine. The title must be a non-empty string.
    Articles are the core content entities linking authors to magazines.
    """

    def __init__(self, id, title, content, author, magazine):
        """
        Initialize a new Article instance.

        Args:
            id (int or None): The article's unique identifier (None for new articles)
            title (str): The article's title (must be non-empty string, read-only after creation)
            content (str): The article's content text
            author (Author): The Author object who wrote the article
            magazine (Magazine): The Magazine object publishing the article

        Raises:
            ValueError: If title is not a string or is empty
        """
        if not isinstance(title, str) or len(title) == 0:
            raise ValueError("Title must be a non-empty string")
        self.id = id
        self._title = title
        self.content = content
        self.author = author
        self.magazine = magazine

    @property
    def title(self):
        """
        Get the article's title.

        Returns:
            str: The article's title (read-only property)
        """
        return self._title

    @classmethod
    def new_from_db(cls, row):
        """
        Create an Article instance from a database row, loading related objects.

        This method unpacks the database row, looks up the associated Author
        and Magazine objects by their IDs, and creates a fully populated Article instance.

        Args:
            row (tuple): Database row containing (id, title, content, author_id, magazine_id)

        Returns:
            Article: New Article instance with loaded author and magazine objects
        """
        from .author import Author
        from .magazine import Magazine
        id, title, content, author_id, magazine_id = row
        author = Author.find_by_id(author_id)
        magazine = Magazine.find_by_id(magazine_id)
        return cls(id, title, content, author, magazine)

    @classmethod
    def find_by_id(cls, id):
        """
        Find an article by its ID.

        Args:
            id (int): The article's ID to search for

        Returns:
            Article or None: Article instance if found, None otherwise
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls.new_from_db(row)
        return None

    def save(self):
        """
        Save the article to the database.

        Stores the article's data and uses the IDs of the associated author
        and magazine objects for the foreign key relationships.
        If the article is new (id is None), performs an INSERT operation.
        If the article exists (id is set), performs an UPDATE operation.
        Sets the id attribute for new articles after insertion.
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self.id is None:
                cursor.execute("INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)", (self.title, self.content, self.author.id, self.magazine.id))
                self.id = cursor.lastrowid
            else:
                cursor.execute("UPDATE articles SET title = ?, content = ?, author_id = ?, magazine_id = ? WHERE id = ?", (self.title, self.content, self.author.id, self.magazine.id, self.id))
            conn.commit()
        finally:
            conn.close()
