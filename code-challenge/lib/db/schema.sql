-- Schema for Authors, Magazines, and Articles
DROP TABLE IF EXISTS articles;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS magazines;

CREATE TABLE authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE magazines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL
);

CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    author_id INTEGER NOT NULL,
    magazine_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE,
    FOREIGN KEY (magazine_id) REFERENCES magazines(id) ON DELETE CASCADE
);

CREATE INDEX idx_articles_author_id ON articles(author_id);
CREATE INDEX idx_articles_magazine_id ON articles(magazine_id);
