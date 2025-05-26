from ..db.connection import get_connection

class Article:
    def __init__(self, title, author, magazine, id=None):
        from .author import Author  # Local import to avoid circular import
        from .magazine import Magazine  # Local import to avoid circular import
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Article title must be a non-empty string.")
        if not isinstance(author, Author):
            raise ValueError("author must be an Author instance.")
        if not isinstance(magazine, Magazine):
            raise ValueError("magazine must be a Magazine instance.")
        self._id = id
        self.title = title.strip()
        self.author = author
        self.magazine = magazine
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
                    "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                    (self.title, self.author.id, self.magazine.id)
                )
                self._id = cursor.lastrowid
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        from .author import Author
        from .magazine import Magazine
        conn = get_connection()
        try:
            cursor = conn.execute("SELECT * FROM articles WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row:
                author = Author.find_by_id(row["author_id"])
                magazine = Magazine.find_by_id(row["magazine_id"])
                if author is None or magazine is None:
                    return None
                return cls(row["title"], author, magazine, row["id"])
        finally:
            conn.close()
        return None

    @classmethod
    def find_by_title(cls, title):
        from .author import Author
        from .magazine import Magazine
        conn = get_connection()
        try:
            cursor = conn.execute("SELECT * FROM articles WHERE title = ?", (title,))
            row = cursor.fetchone()
            if row:
                author = Author.find_by_id(row["author_id"])
                magazine = Magazine.find_by_id(row["magazine_id"])
                if author is None or magazine is None:
                    return None
                return cls(row["title"], author, magazine, row["id"])
        finally:
            conn.close()
        return None

    @classmethod
    def from_row(cls, row):
        from .author import Author
        from .magazine import Magazine
        author = Author.find_by_id(row["author_id"])
        magazine = Magazine.find_by_id(row["magazine_id"])
        if author is None or magazine is None:
            return None
        return cls(row["title"], author, magazine, row["id"])

    def author_obj(self):
        return self.author

    def magazine_obj(self):
        return self.magazine
