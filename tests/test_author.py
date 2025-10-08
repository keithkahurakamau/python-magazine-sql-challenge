import unittest
from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article
from lib.database_utils import create_tables, get_connection

class TestAuthor(unittest.TestCase):
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

    def test_author_creation_and_save(self):
        author = Author(None, "John Doe")
        author.save()
        self.assertIsNotNone(author.id)

    def test_add_article_and_topic_areas(self):
        author = Author(None, "Jane Smith")
        author.save()
        magazine = Magazine(None, "Tech Today", "Technology")
        magazine.save()
        article = author.add_article(magazine, "New Tech Trends")
        self.assertEqual(article.title, "New Tech Trends")
        self.assertIn("Technology", author.topic_areas())

    def test_articles_and_magazines_relationship(self):
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
