from ..db.connection import get_connection

class Author:
    def __init__(self, name, id=None):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Author name must be a non-empty string.")
        self._id = id
        self.name = name.strip()
        if id is None:
            self.save()

    @property
    def id(self):
        return self._id

    def save(self):
        conn = get_connection()
        try:
            with conn:
                cursor = conn.execute(
                    "INSERT INTO authors (name) VALUES (?)",
                    (self.name,)
                )
                self._id = cursor.lastrowid
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        try:
            cursor = conn.execute("SELECT * FROM authors WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row:
                return cls(row["name"], row["id"])
        finally:
            conn.close()
        return None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        try:
            cursor = conn.execute("SELECT * FROM authors WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                return cls(row["name"], row["id"])
        finally:
            conn.close()
        return None

    def articles(self):
        from .article import Article  # Local import to avoid circular import
        conn = get_connection()
        try:
            cursor = conn.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,))
            return [Article.from_row(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def magazines(self):
        from .magazine import Magazine  # Local import to avoid circular import
        conn = get_connection()
        try:
            cursor = conn.execute("""
                SELECT DISTINCT m.* FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
            """, (self.id,))
            return [Magazine.from_row(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def add_article(self, magazine, title):
        from .article import Article  # Local import to avoid circular import
        from .magazine import Magazine  # Local import for type check
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Article title must be a non-empty string.")
        if not isinstance(magazine, Magazine):
            raise ValueError("magazine must be a Magazine instance.")
        article = Article(title=title.strip(), author=self, magazine=magazine)
        return article

    def topic_areas(self):
        conn = get_connection()
        try:
            cursor = conn.execute("""
                SELECT DISTINCT m.category FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
            """, (self.id,))
            return [row["category"] for row in cursor.fetchall()]
        finally:
            conn.close()
