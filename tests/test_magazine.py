"""
Test module for Magazine class functionality.

This module contains unit tests for the Magazine class, covering creation,
saving, relationships with articles and contributors, and advanced methods
like contributing_authors and top_publisher.
"""

import unittest
import os
from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article
from lib.database_utils import create_tables, get_connection, DB_FILE

class TestMagazine(unittest.TestCase):
    """
    Test cases for Magazine class methods and relationships.
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

    def test_magazine_creation_and_save(self):
        """Test creating a new magazine and saving to database."""
        magazine = Magazine(None, "Science Daily", "Science")
        magazine.save()
        self.assertIsNotNone(magazine.id)

    def test_article_titles_and_contributors(self):
        """Test retrieving article titles and contributors for a magazine."""
        author = Author(None, "Bob")
        author.save()
        magazine = Magazine(None, "Nature", "Science")
        magazine.save()
        author.add_article(magazine, "Climate Change")
        titles = magazine.article_titles()
        contributors = magazine.contributors()
        self.assertIn("Climate Change", titles)
        self.assertEqual(len(contributors), 1)
        self.assertEqual(contributors[0].name, "Bob")

    def test_contributing_authors_and_top_publisher(self):
        """Test contributing authors filter and top publisher selection."""
        author = Author(None, "Carol")
        author.save()
        magazine = Magazine(None, "Tech World", "Technology")
        magazine.save()
        # Add 3 articles by the same author to test contributing_authors
        for i in range(3):
            author.add_article(magazine, f"Tech Article {i+1}")
        contributing_authors = magazine.contributing_authors()
        self.assertEqual(len(contributing_authors), 1)
        self.assertEqual(contributing_authors[0].name, "Carol")
        top = Magazine.top_publisher()
        self.assertEqual(top.id, magazine.id)

if __name__ == "__main__":
    unittest.main()
