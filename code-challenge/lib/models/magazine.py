from ..db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Magazine name must be a non-empty string.")
        if not isinstance(category, str) or not category.strip():
            raise ValueError("Magazine category must be a non-empty string.")
        self._id = id
        self.name = name.strip()
        self.category = category.strip()
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
                    "INSERT INTO magazines (name, category) VALUES (?, ?)",
                    (self.name, self.category)
                )
                self._id = cursor.lastrowid
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        try:
            cursor = conn.execute("SELECT * FROM magazines WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row:
                return cls(row["name"], row["category"], row["id"])
        finally:
            conn.close()
        return None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        try:
            cursor = conn.execute("SELECT * FROM magazines WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                return cls(row["name"], row["category"], row["id"])
        finally:
            conn.close()
        return None

    def articles(self):
        from .article import Article  # Local import to avoid circular import
        conn = get_connection()
        try:
            cursor = conn.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
            return [Article.from_row(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def contributors(self):
        from .author import Author  # Local import to avoid circular import
        conn = get_connection()
        try:
            cursor = conn.execute("""
                SELECT DISTINCT a.* FROM authors a
                JOIN articles art ON a.id = art.author_id
                WHERE art.magazine_id = ?
            """, (self.id,))
            return [Author(row["name"], row["id"]) for row in cursor.fetchall()]
        finally:
            conn.close()

    def article_titles(self):
        conn = get_connection()
        try:
            cursor = conn.execute("SELECT title FROM articles WHERE magazine_id = ?", (self.id,))
            return [row["title"] for row in cursor.fetchall()]
        finally:
            conn.close()

    def contributing_authors(self):
        from .author import Author  # Local import to avoid circular import
        conn = get_connection()
        try:
            cursor = conn.execute("""
                SELECT a.*, COUNT(art.id) as article_count FROM authors a
                JOIN articles art ON a.id = art.author_id
                WHERE art.magazine_id = ?
                GROUP BY a.id
                HAVING article_count > 2
            """, (self.id,))
            return [Author(row["name"], row["id"]) for row in cursor.fetchall()]
        finally:
            conn.close()

    @classmethod
    def top_publisher(cls):
        conn = get_connection()
        try:
            cursor = conn.execute("""
                SELECT m.*, COUNT(a.id) as article_count FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                GROUP BY m.id
                ORDER BY article_count DESC
                LIMIT 1
            """)
            row = cursor.fetchone()
            if row:
                return cls(row["name"], row["category"], row["id"])
        finally:
            conn.close()
        return None

    @classmethod
    def from_row(cls, row):
        return cls(row["name"], row["category"], row["id"])
