import pytest
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.db.seed import seed

@pytest.fixture(autouse=True)
def setup_db():
    seed()

def test_article_creation():
    author = Author.find_by_name("Bob")
    mag = Magazine.find_by_name("Health Weekly")
    article = Article("Test Article", author, mag)
    assert article.id is not None
    assert article.title == "Test Article"
    assert article.author.id == author.id
    assert article.magazine.id == mag.id
    with pytest.raises(ValueError):
        Article("", author, mag)

def test_find_by_id_and_title():
    article = Article.find_by_title("AI Revolution")
    assert article is not None
    by_id = Article.find_by_id(article.id)
    assert by_id.title == "AI Revolution"

def test_author_and_magazine_obj():
    article = Article.find_by_title("AI Revolution")
    assert article.author_obj().name == "Alice"
    assert article.magazine_obj().name == "Tech Today"
