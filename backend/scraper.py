import os
import django
import requests
import random
from bs4 import BeautifulSoup

# Set up Django environment to use the Book model directly
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from books.models import Book

# Sample authors for demo purposes since the site doesn't provide real author data
SAMPLE_AUTHORS = [
    "J.K. Rowling",
    "George Orwell",
    "Jane Austen",
    "Mark Twain",
    "Agatha Christie",
    "Stephen King",
    "Toni Morrison",
    "Haruki Murakami",
    "Maya Angelou",
    "Ernest Hemingway",
    "Virginia Woolf",
    "F. Scott Fitzgerald",
    "Gabriel García Márquez",
    "Chimamanda Ngozi Adichie",
    "Zadie Smith",
    "Cormac McCarthy",
    "Margaret Atwood",
    "Neil Gaiman",
    "Ursula K. Le Guin",
    "Salman Rushdie"
]

BASE_URL = "http://books.toscrape.com/"


def get_soup(url):
    """Fetch a page and return a BeautifulSoup parser."""
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def get_book_description(book_url):
    """Fetch the book detail page and extract the description."""
    try:
        detail_soup = get_soup(book_url)
        description_header = detail_soup.find(id="product_description")
        if description_header:
            description_paragraph = description_header.find_next_sibling("p")
            if description_paragraph:
                return description_paragraph.text.strip()
    except Exception:
        pass
    return "No description available."


def parse_book_data(article, base_url):
    """Extract title, rating, url, and description from a book card."""
    title = article.h3.a["title"].strip()
    relative_url = article.h3.a["href"]
    book_url = base_url + relative_url.replace("../", "")

    rating_class = article.p.get("class", [])
    rating_text = rating_class[1] if len(rating_class) > 1 else "Zero"
    rating_map = {
        "One": 1.0,
        "Two": 2.0,
        "Three": 3.0,
        "Four": 4.0,
        "Five": 5.0,
    }

    return {
        "title": title,
        "author": random.choice(SAMPLE_AUTHORS),
        "description": get_book_description(book_url),
        "rating": rating_map.get(rating_text, 0.0),
        "book_url": book_url,
    }


def validate_book_url(url):
    """Check if a book URL is accessible."""
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except:
        return False


def cleanup_broken_urls():
    """Remove books with broken URLs from the database."""
    books = Book.objects.all()
    removed_count = 0
    
    for book in books:
        if not validate_book_url(book.book_url):
            print(f"Removing broken URL: {book.title}")
            book.delete()
            removed_count += 1
    
    print(f"Cleaned up {removed_count} books with broken URLs.")


def scrape_books(page_limit=2):
    """Scrape multiple pages and save books to the database."""
    current_url = BASE_URL
    saved_count = 0

    for page_number in range(1, page_limit + 1):
        print(f"Scraping page {page_number}: {current_url}")
        soup = get_soup(current_url)
        articles = soup.select("article.product_pod")

        for article in articles:
            book_data = parse_book_data(article, BASE_URL)
            
            # Validate the book URL before saving
            if not validate_book_url(book_data["book_url"]):
                print(f"Skipping {book_data['title']} - URL not accessible")
                continue
                
            book, created = Book.objects.get_or_create(
                title=book_data["title"],
                defaults={
                    "author": book_data["author"],
                    "description": book_data["description"],
                    "rating": book_data["rating"],
                    "book_url": book_data["book_url"],
                },
            )
            if created:
                saved_count += 1
                print(f"Saved: {book.title}")
            else:
                print(f"Already exists: {book.title}")

        next_link = soup.select_one("li.next a")
        if not next_link:
            break
        current_url = BASE_URL + next_link["href"]

    print(f"Finished scraping. Saved {saved_count} new books.")


def update_existing_authors():
    """Update existing books with 'Unknown Author' to have random authors."""
    books = Book.objects.filter(author="Unknown Author")
    updated_count = 0
    
    for book in books:
        book.author = random.choice(SAMPLE_AUTHORS)
        book.save()
        updated_count += 1
        print(f"Updated: {book.title} -> {book.author}")
    
    print(f"Updated {updated_count} books with random authors.")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "cleanup":
            cleanup_broken_urls()
        elif sys.argv[1] == "update_authors":
            update_existing_authors()
        else:
            print("Usage: python scraper.py [cleanup|update_authors]")
    else:
        scrape_books(page_limit=3)
