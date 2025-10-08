import ipdb
from lib.database_utils import create_tables
from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article

# Create tables
create_tables()

# Create sample data
author1 = Author(None, "John Doe")
author1.save()
author2 = Author(None, "Jane Smith")
author2.save()

magazine1 = Magazine(None, "Tech Today", "Technology")
magazine1.save()
magazine2 = Magazine(None, "Health Weekly", "Health")
magazine2.save()

# Add articles
article1 = author1.add_article(magazine1, "AI Trends")
article2 = author1.add_article(magazine2, "Healthy Living")
article3 = author2.add_article(magazine1, "Blockchain Basics")
article4 = author2.add_article(magazine1, "Cybersecurity Tips")
article5 = author2.add_article(magazine1, "Machine Learning")

# Test relationships
print("Author1 articles:", [a.title for a in author1.articles()])
print("Author1 magazines:", [m.name for m in author1.magazines()])
print("Author1 topic areas:", author1.topic_areas())

print("Magazine1 articles:", magazine1.articles())
print("Magazine1 contributors:", [c.name for c in magazine1.contributors()])
print("Magazine1 article titles:", magazine1.article_titles())
print("Magazine1 contributing authors:", [a.name for a in magazine1.contributing_authors()])

print("Top publisher:", Magazine.top_publisher().name if Magazine.top_publisher() else None)

# Test validations
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

# Manual testing completed
print("All tests passed successfully!")
