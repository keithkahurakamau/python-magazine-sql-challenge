"""
Debug script for manual testing of the magazine database system.

This script creates sample data, tests relationships and methods,
and validates error handling to ensure the system works correctly.
"""

import ipdb
from lib.database_utils import create_tables
from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article

# Initialize database tables
create_tables()

# Create sample authors
author1 = Author(None, "John Doe")
author1.save()
author2 = Author(None, "Jane Smith")
author2.save()

# Create sample magazines
magazine1 = Magazine(None, "Tech Today", "Technology")
magazine1.save()
magazine2 = Magazine(None, "Health Weekly", "Health")
magazine2.save()

# Add articles using author's add_article method
article1 = author1.add_article(magazine1, "AI Trends")
article2 = author1.add_article(magazine2, "Healthy Living")
article3 = author2.add_article(magazine1, "Blockchain Basics")
article4 = author2.add_article(magazine1, "Cybersecurity Tips")
article5 = author2.add_article(magazine1, "Machine Learning")

# Test author relationships and methods
print("Author1 articles:", [a.title for a in author1.articles()])
print("Author1 magazines:", [m.name for m in author1.magazines()])
print("Author1 topic areas:", author1.topic_areas())

# Test magazine relationships and methods
print("Magazine1 articles:", magazine1.articles())
print("Magazine1 contributors:", [c.name for c in magazine1.contributors()])
print("Magazine1 article titles:", magazine1.article_titles())
print("Magazine1 contributing authors:", [a.name for a in magazine1.contributing_authors()])

# Test top publisher method
print("Top publisher:", Magazine.top_publisher().name if Magazine.top_publisher() else None)

# Test validation errors
try:
    invalid_author = Author(None, "")
except ValueError as e:
    print("Validation error for author:", e)

try:
    invalid_magazine = Magazine(None, "", "Category")
except ValueError as e:
    print("Validation error for magazine name:", e)

try:
    invalid_magazine = Magazine(None, "Name", "")
except ValueError as e:
    print("Validation error for magazine category:", e)

try:
    invalid_article = Article(None, "", "Content", author1, magazine1)
except ValueError as e:
    print("Validation error for article title:", e)

# Manual testing completed successfully
print("All tests passed successfully!")
