import unittest
from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article
from lib.database_utils import create_tables, get_connection

class TestMagazine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        create_tables()
        cls.conn = get_connection()
        cls.cursor = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def setUp(self):
        self.cursor.execute("DELETE FROM articles")
        self.cursor.execute("DELETE FROM authors")
        self.cursor.execute("DELETE FROM magazines")
        self.conn.commit()

    def test_magazine_creation_and_save(self):
        magazine = Magazine(None, "Science Daily", "Science")
        magazine.save()
        self.assertIsNotNone(magazine.id)

    def test_article_titles_and_contributors(self):
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
