import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.seed import seed

@pytest.fixture(autouse=True)
def setup_db():
    seed()

def test_author_creation():
    author = Author("Test Author")
    assert author.id is not None
    assert author.name == "Test Author"

    with pytest.raises(ValueError):
        Author("")


def test_find_by_id_and_name():
    author = Author.find_by_name("Alice")
    assert author is not None
    by_id = Author.find_by_id(author.id)
    assert by_id.name == "Alice"


def test_articles_and_magazines():
    author = Author.find_by_name("Alice")
    articles = author.articles()
    assert len(articles) >= 1
    magazines = author.magazines()
    assert len(magazines) >= 1


def test_add_article_and_topic_areas():
    author = Author.find_by_name("Bob")
    mag = Magazine.find_by_name("Tech Today")
    article = author.add_article(mag, "New Tech")
    assert article.title == "New Tech"
    assert article.author.id == author.id
    assert article.magazine.id == mag.id
    topics = author.topic_areas()
    assert "Technology" in topics
