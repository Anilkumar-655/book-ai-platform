import os
import re
from typing import List

from books.models import Book


def summarize_description(description: str, word_limit: int = 30) -> str:
    """Create a short summary for a book description."""
    if not description or description.strip() == "Scraped book from books.toscrape.com":
        return "No description available for summary."

    words = description.split()
    if len(words) <= word_limit:
        return description
    return " ".join(words[:word_limit]) + "..."


def has_valid_description(description: str) -> bool:
    """Return True only if the description is meaningful enough to summarize."""
    return bool(description and description.strip() and description.strip() != "Scraped book from books.toscrape.com")


def build_fallback_summary(book: Book) -> str:
    """Create a simple fallback summary when a full description is not available."""
    author_text = book.author if book.author and book.author != "Unknown Author" else "an unknown author"
    return (
        f"{book.title} is a book by {author_text}. "
        f"It has a rating of {book.rating:.1f} and is available through the Book AI Platform."
    )


def chunk_text(text: str, max_chars: int = 200) -> List[str]:
    """Split text into smaller chunks for simple relevance matching."""
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        chunk = text[start : start + max_chars].strip()
        if chunk:
            chunks.append(chunk)
        start += max_chars
    return chunks


def score_text(question: str, text: str) -> int:
    """Score how well a piece of text matches the question."""
    question_words = set(re.findall(r"\w+", question.lower()))
    text_lower = text.lower()
    score = 0
    for word in question_words:
        if word in text_lower:
            score += 1
    return score


def find_relevant_books(question: str, max_results: int = 3) -> List[Book]:
    """Find the books that best match the user question."""
    if not question:
        return []

    scored_books = []

    for book in Book.objects.all():
        score = 0
        score += score_text(question, book.title) * 3
        score += score_text(question, book.author) * 2

        # Score book description at the chunk level for lightweight RAG.
        description_chunks = chunk_text(book.description)
        for chunk in description_chunks:
            score += score_text(question, chunk)

        scored_books.append((score, book))

    scored_books.sort(key=lambda pair: (-pair[0], -pair[1].rating))
    relevant = [book for score, book in scored_books if score > 0][:max_results]

    if not relevant:
        relevant = [book for _, book in scored_books[:max_results]]

    return relevant


def build_context(books: List[Book]) -> str:
    """Build a text context from a list of books for AI prompt usage."""
    lines = []
    for book in books:
        summary = summarize_description(book.description)
        lines.append(
            f"Title: {book.title}\nAuthor: {book.author}\nRating: {book.rating}\nDescription: {summary}\nURL: {book.book_url}\n"
        )

        # Add short description chunks to provide more detailed context.
        for chunk in chunk_text(book.description, max_chars=180):
            lines.append(f"Description chunk: {chunk}")

    return "\n".join(lines)


def query_openai(question: str, context: str) -> str | None:
    """Call OpenAI if configured, otherwise return None."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        import openai

        openai.api_key = api_key
        prompt = (
            "Answer the question using only the book data below. "
            "If the answer is not in the data, explain that it is not available.\n\n"
            f"{context}\n\nQuestion: {question}\nAnswer:"
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for a book intelligence platform."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return None


def answer_question(question: str) -> str:
    """Answer a user question with book context and fallback logic."""
    question = question.strip()
    if not question:
        raise ValueError("Question cannot be empty.")

    books = find_relevant_books(question)
    context = build_context(books)
    openai_answer = query_openai(question, context)

    if openai_answer:
        # Add source books information
        source_books = [f"- {book.title} by {book.author}" for book in books[:3]]
        return f"{openai_answer}\n\n**Source books used:**\n" + "\n".join(source_books)

    if not books:
        return "I could not find any books to answer that question."

    # Professional fallback response when AI is unavailable
    answer_lines = [
        "Based on available book data, here are some relevant books related to your question:",
        "",  # Empty line for spacing
    ]

    for book in books[:5]:  # Limit to top 5 books for cleaner response
        rating_text = f" (Rating: {book.rating})"
        answer_lines.append(f"• {book.title} by {book.author}{rating_text}")

        # Optional: Add short description line if available
        if has_valid_description(book.description):
            short_desc = summarize_description(book.description, word_limit=15)
            if short_desc and short_desc != "No description available.":
                answer_lines.append(f"  {short_desc}")

    answer_lines.extend([
        "",  # Empty line for spacing
        "You can explore these books for more details related to your query."
    ])

    return "\n".join(answer_lines)


def generate_book_summary(book: Book) -> str:
    """Generate an AI summary for a specific book."""
    if not book:
        return build_fallback_summary(book)

    # Try to use AI if we have a meaningful description
    if has_valid_description(book.description):
        api_key = os.getenv("OPENAI_API_KEY")
        # Improved prompt focusing on themes and key ideas for more natural summaries
        summary_prompt = (
            f"Write a short, engaging summary of this book in 2-3 sentences, "
            f"highlighting themes and key ideas:\n\n{book.description}\n\nSummary:"
        )

        if api_key:
            try:
                import openai

                openai.api_key = api_key
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a book summarizer. Create engaging, concise summaries that highlight the book's main idea, themes, and key concepts."},
                        {"role": "user", "content": summary_prompt},
                    ],
                    max_tokens=150,
                    temperature=0.7,
                )
                return response.choices[0].message.content.strip()
            except Exception:
                # Fallback to description summary if OpenAI fails
                return summarize_description(book.description, word_limit=50)

    # Use intelligent fallback summary with available book data
    return build_fallback_summary(book)


def recommend_similar_books(book: Book, max_results: int = 3) -> List[Book]:
    """Recommend books similar to the given book based on keywords and description."""
    if not book:
        return []

    # Extract keywords from title and description
    title_words = set(re.findall(r"\w+", book.title.lower()))
    desc_words = set(re.findall(r"\w+", book.description.lower() if book.description else ""))
    keywords = title_words | desc_words

    # Remove common stop words
    stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "must", "can", "this", "that", "these", "those", "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them"}

    keywords = keywords - stop_words
    if not keywords:
        # If no keywords, fall back to same author or high rating books
        similar_books = list(Book.objects.exclude(id=book.id).filter(author=book.author)[:max_results])
        if not similar_books:
            similar_books = list(Book.objects.exclude(id=book.id).order_by('-rating')[:max_results])
        return similar_books

    # Score other books based on keyword matches
    scored_books = []
    for other_book in Book.objects.exclude(id=book.id):
        score = 0

        # Title matches (higher weight)
        other_title_words = set(re.findall(r"\w+", other_book.title.lower()))
        title_matches = len(keywords & other_title_words)
        score += title_matches * 3

        # Description matches
        if other_book.description:
            other_desc_words = set(re.findall(r"\w+", other_book.description.lower()))
            desc_matches = len(keywords & other_desc_words)
            score += desc_matches

        # Same author bonus
        if other_book.author == book.author:
            score += 2

        # Rating bonus (prefer higher rated books)
        score += other_book.rating * 0.5

        scored_books.append((score, other_book))

    # Sort by score and return top results
    scored_books.sort(key=lambda x: (-x[0], -x[1].rating))
    return [book for score, book in scored_books[:max_results] if score > 0]
