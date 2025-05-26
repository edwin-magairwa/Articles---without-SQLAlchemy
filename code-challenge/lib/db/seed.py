from .connection import get_connection

def seed():
    conn = get_connection()
    try:
        with conn:
            conn.execute("DELETE FROM articles;")
            conn.execute("DELETE FROM authors;")
            conn.execute("DELETE FROM magazines;")
            # Reset auto-increment sequences for SQLite
            conn.execute("DELETE FROM sqlite_sequence WHERE name='authors';")
            conn.execute("DELETE FROM sqlite_sequence WHERE name='magazines';")
            conn.execute("DELETE FROM sqlite_sequence WHERE name='articles';")
            # Authors
            conn.execute("INSERT INTO authors (name) VALUES (?)", ("Alice",))
            conn.execute("INSERT INTO authors (name) VALUES (?)", ("Bob",))
            conn.execute("INSERT INTO authors (name) VALUES (?)", ("Carol",))
            # Magazines
            conn.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Tech Today", "Technology"))
            conn.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Health Weekly", "Health"))
            conn.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Travel Explorer", "Travel"))
            # Articles
            conn.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", ("AI Revolution", 1, 1))
            conn.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", ("Wellness Tips", 2, 2))
            conn.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", ("Journey Abroad", 3, 3))
            conn.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", ("Cloud Computing", 1, 1))
            conn.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", ("Healthy Living", 1, 2))
    finally:
        conn.close()

if __name__ == "__main__":
    seed()
