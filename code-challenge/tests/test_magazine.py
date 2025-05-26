import pytest
from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.models.article import Article
from lib.db.seed import seed

@pytest.fixture(autouse=True)
def setup_db():
    seed()

def test_magazine_creation():
    mag = Magazine("Science World", "Science")
    assert mag.id is not None
    assert mag.name == "Science World"
    assert mag.category == "Science"
    with pytest.raises(ValueError):
        Magazine("", "Science")
    with pytest.raises(ValueError):
        Magazine("Science World", "")

def test_find_by_id_and_name():
    mag = Magazine.find_by_name("Tech Today")
    assert mag is not None
    by_id = Magazine.find_by_id(mag.id)
    assert by_id.name == "Tech Today"

def test_articles_and_contributors():
    mag = Magazine.find_by_name("Tech Today")
    articles = mag.articles()
    assert len(articles) >= 1
    contributors = mag.contributors()
    assert any(a.name == "Alice" for a in contributors)

def test_article_titles_and_contributing_authors():
    mag = Magazine.find_by_name("Tech Today")
    titles = mag.article_titles()
    assert "AI Revolution" in titles
    # Add more articles for Alice to test contributing_authors
    author = Author.find_by_name("Alice")
    author.add_article(mag, "Extra Article 1")
    author.add_article(mag, "Extra Article 2")
    author.add_article(mag, "Extra Article 3")
    contribs = mag.contributing_authors()
    assert any(a.name == "Alice" for a in contribs)

def test_top_publisher():
    top = Magazine.top_publisher()
    assert top is not None
    assert isinstance(top, Magazine)
