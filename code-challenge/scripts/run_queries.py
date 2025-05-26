from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def list_authors():
    authors = []
    for i in range(1, 100):
        a = Author.find_by_id(i)
        if a:
            authors.append(a)
    print("\nAuthors:")
    for a in authors:
        print(f"{a.id}: {a.name}")

def list_articles_by_author():
    name = input("Enter author name: ")
    author = Author.find_by_name(name)
    if not author:
        print("Author not found.")
        return
    print(f"\nArticles by {author.name}:")
    for art in author.articles():
        print(f"- {art.title} (Magazine: {art.magazine.name})")

def list_magazines_by_author():
    name = input("Enter author name: ")
    author = Author.find_by_name(name)
    if not author:
        print("Author not found.")
        return
    print(f"\nMagazines contributed to by {author.name}:")
    for mag in author.magazines():
        print(f"- {mag.name} ({mag.category})")

def list_articles_by_magazine():
    name = input("Enter magazine name: ")
    mag = Magazine.find_by_name(name)
    if not mag:
        print("Magazine not found.")
        return
    print(f"\nArticles in {mag.name}:")
    for art in mag.articles():
        print(f"- {art.title} (Author: {art.author.name})")

def main():
    while True:
        print("\nMenu:")
        print("1. List all authors")
        print("2. List articles by author")
        print("3. List magazines by author")
        print("4. List articles by magazine")
        print("5. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            list_authors()
        elif choice == "2":
            list_articles_by_author()
        elif choice == "3":
            list_magazines_by_author()
        elif choice == "4":
            list_articles_by_magazine()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
