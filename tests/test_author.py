"""
Test module for Author class functionality.

This module contains unit tests for the Author class, covering creation,
saving, relationships with articles and magazines, and advanced methods
like add_article and topic_areas.
"""

import unittest
import os
from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article
from lib.database_utils import create_tables, get_connection, DB_FILE

class TestAuthor(unittest.TestCase):
    """
    Test cases for Author class methods and relationships.
    """

    @classmethod
    def setUpClass(cls):
        """Set up test database tables."""
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
        create_tables()

    def setUp(self):
        """Reset database state before each test by clearing all tables."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM articles")
        cursor.execute("DELETE FROM authors")
        cursor.execute("DELETE FROM magazines")
        conn.commit()
        conn.close()

    def test_author_creation_and_save(self):
        """Test creating a new author and saving to database."""
        author = Author(None, "John Doe")
        author.save()
        self.assertIsNotNone(author.id)

    def test_add_article_and_topic_areas(self):
        """Test adding an article to an author and retrieving topic areas."""
        author = Author(None, "Jane Smith")
        author.save()
        magazine = Magazine(None, "Tech Today", "Technology")
        magazine.save()
        article = author.add_article(magazine, "New Tech Trends")
        self.assertEqual(article.title, "New Tech Trends")
        self.assertIn("Technology", author.topic_areas())

    def test_articles_and_magazines_relationship(self):
        """Test author's relationships with articles and magazines."""
        author = Author(None, "Alice")
        author.save()
        magazine = Magazine(None, "Health Weekly", "Health")
        magazine.save()
        author.add_article(magazine, "Health Tips")
        articles = author.articles()
        magazines = author.magazines()
        self.assertEqual(len(articles), 1)
        self.assertEqual(len(magazines), 1)
        self.assertEqual(magazines[0].name, "Health Weekly")

if __name__ == "__main__":
    unittest.main()
