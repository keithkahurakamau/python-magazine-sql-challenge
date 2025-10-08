"""
Magazine module for managing magazine entities in the magazine database.

This module defines the Magazine class, which represents a magazine in the system.
Magazines have a name and category, both of which are mutable with validation.
Magazines can contain articles and have relationships to their contributors.
"""

from .database_utils import get_connection

class Magazine:
    """
    Represents a magazine in the magazine system.

    Magazines have a unique ID, a name, and a category. Both name and category
    are mutable properties with validation requiring non-empty strings.
    Magazines can publish articles and have relationships to their articles and contributors.
    """

    def __init__(self, id, name, category):
        """
        Initialize a new Magazine instance.

        Args:
            id (int or None): The magazine's unique identifier (None for new magazines)
            name (str): The magazine's name (must be non-empty string)
            category (str): The magazine's category (must be non-empty string)

        Raises:
            ValueError: If name or category is not a string or is empty
        """
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string")
        self.id = id
        self._name = name
        self._category = category

    @property
    def name(self):
        """
        Get the magazine's name.

        Returns:
            str: The magazine's name
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Set the magazine's name with validation.

        Args:
            value (str): The new name (must be non-empty string)

        Raises:
            ValueError: If value is not a string or is empty
        """
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Name must be a non-empty string")
        self._name = value

    @property
    def category(self):
        """
        Get the magazine's category.

        Returns:
            str: The magazine's category
        """
        return self._category

    @category.setter
    def category(self, value):
        """
        Set the magazine's category with validation.

        Args:
            value (str): The new category (must be non-empty string)

        Raises:
            ValueError: If value is not a string or is empty
        """
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string")
        self._category = value

    @classmethod
    def new_from_db(cls, row):
        """
        Create a Magazine instance from a database row.

        Args:
            row (tuple): Database row containing (id, name, category)

        Returns:
            Magazine: New Magazine instance with data from the row
        """
        return cls(*row)

    @classmethod
    def find_by_id(cls, id):
        """
        Find a magazine by its ID.

        Args:
            id (int): The magazine's ID to search for

        Returns:
            Magazine or None: Magazine instance if found, None otherwise
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls.new_from_db(row)
        return None

    def save(self):
        """
        Save the magazine to the database.

        If the magazine is new (id is None), performs an INSERT operation.
        If the magazine exists (id is set), performs an UPDATE operation.
        Sets the id attribute for new magazines after insertion.
        """
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self.id is None:
                cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
                self.id = cursor.lastrowid
            else:
                cursor.execute("UPDATE magazines SET name = ?, category = ? WHERE id = ?", (self.name, self.category, self.id))
            conn.commit()
        finally:
            conn.close()

    def articles(self):
        """
        Get all articles published in this magazine.

        Returns:
            list[Article]: List of Article instances published in this magazine
        """
        from .article import Article
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article.new_from_db(row) for row in rows]

    def contributors(self):
        """
        Get all authors who have contributed articles to this magazine.

        Uses a JOIN query to find distinct authors through the magazine's articles.

        Returns:
            list[Author]: List of unique Author instances who have written for this magazine
        """
        from .author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT authors.* FROM authors JOIN articles ON authors.id = articles.author_id WHERE articles.magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author.new_from_db(row) for row in rows]

    def article_titles(self):
        """
        Get the titles of all articles published in this magazine.

        Returns:
            list[str]: List of article titles in this magazine
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]

    def contributing_authors(self):
        """
        Get authors who have contributed more than 2 articles to this magazine.

        Uses GROUP BY and HAVING to filter authors with more than 2 articles.

        Returns:
            list[Author]: List of Author instances with more than 2 articles in this magazine
        """
        from .author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT author_id FROM articles WHERE magazine_id = ? GROUP BY author_id HAVING COUNT(id) > 2", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author.find_by_id(row[0]) for row in rows]

    @classmethod
    def top_publisher(cls):
        """
        Find the magazine with the most articles (top publisher).

        Uses GROUP BY, ORDER BY DESC, and LIMIT 1 to find the magazine
        with the highest article count.

        Returns:
            Magazine or None: Magazine instance with most articles, or None if no articles exist
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT magazine_id, COUNT(id) FROM articles GROUP BY magazine_id ORDER BY COUNT(id) DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls.find_by_id(row[0])
        return None
