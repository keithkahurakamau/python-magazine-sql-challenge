"""
Author module for managing author entities in the magazine database.

This module defines the Author class, which represents an author in the system.
Authors have a name and can be associated with articles and magazines through relationships.
"""

from .database_utils import get_connection

class Author:
    """
    Represents an author in the magazine system.

    Authors have a unique ID and a name. The name is read-only after creation
    and must be a non-empty string. Authors can write articles for magazines
    and have relationships to their articles and the magazines they've contributed to.
    """

    def __init__(self, id, name):
        """
        Initialize a new Author instance.

        Args:
            id (int or None): The author's unique identifier (None for new authors)
            name (str): The author's name (must be non-empty string)

        Raises:
            ValueError: If name is not a string or is empty
        """
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string")
        self.id = id
        self._name = name

    @property
    def name(self):
        """
        Get the author's name.

        Returns:
            str: The author's name (read-only property)
        """
        return self._name

    @classmethod
    def new_from_db(cls, row):
        """
        Create an Author instance from a database row.

        Args:
            row (tuple): Database row containing (id, name)

        Returns:
            Author: New Author instance with data from the row
        """
        return cls(*row)

    @classmethod
    def find_by_id(cls, id):
        """
        Find an author by their ID.

        Args:
            id (int): The author's ID to search for

        Returns:
            Author or None: Author instance if found, None otherwise
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls.new_from_db(row)
        return None

    def save(self):
        """
        Save the author to the database.

        If the author is new (id is None), performs an INSERT operation.
        If the author exists (id is set), performs an UPDATE operation.
        Sets the id attribute for new authors after insertion.
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self.id is None:
                cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
                self.id = cursor.lastrowid
            else:
                cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
            conn.commit()
        finally:
            conn.close()

    def articles(self):
        """
        Get all articles written by this author.

        Returns:
            list[Article]: List of Article instances written by this author
        """
        from .article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article.new_from_db(row) for row in rows]

    def magazines(self):
        """
        Get all magazines this author has contributed to.

        Uses a JOIN query to find distinct magazines through the author's articles.

        Returns:
            list[Magazine]: List of unique Magazine instances the author has written for
        """
        from .magazine import Magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT magazines.* FROM magazines JOIN articles ON magazines.id = articles.magazine_id WHERE articles.author_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Magazine.new_from_db(row) for row in rows]

    def add_article(self, magazine, title):
        """
        Create and save a new article for this author in the given magazine.

        Args:
            magazine (Magazine): The magazine to publish the article in
            title (str): The title of the new article

        Returns:
            Article: The newly created and saved Article instance
        """
        from .article import Article
        article = Article(None, title, "", self, magazine)
        article.save()
        return article

    def topic_areas(self):
        """
        Get the unique categories (topic areas) of magazines this author has contributed to.

        Returns:
            list[str]: List of unique category names from the author's magazines
        """
        magazines = self.magazines()
        categories = set(m.category for m in magazines)
        return list(categories)
