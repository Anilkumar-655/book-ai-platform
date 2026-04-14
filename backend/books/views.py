from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ai_utils import answer_question, generate_book_summary, recommend_similar_books
from .models import Book
from .serializers import BookSerializer


@api_view(["GET", "POST"])
def book_list(request):
    """Return a list of books or create a new book."""
    if request.method == "GET":
        cached_data = cache.get("books_list")
        if cached_data is not None:
            return Response(cached_data)

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        cache.set("books_list", serializer.data, 60 * 60)  # Cache for one hour
        return Response(serializer.data)

    if request.method == "POST":
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete("books_list")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def book_detail(request, pk):
    """Return details for a single book."""
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = BookSerializer(book)
    return Response(serializer.data)


@api_view(["POST"])
def ask_question(request):
    """Answer a user question using the AI helper module."""
    question = request.data.get("question", "").strip()
    if not question:
        return Response(
            {"detail": "Please provide a question in the request body."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    cache_key = f"ask_answer:{question.lower()}"
    cached_answer = cache.get(cache_key)
    if cached_answer is not None:
        return Response({"answer": cached_answer})

    try:
        answer = answer_question(question)
        cache.set(cache_key, answer, 60 * 30)  # Cache answers for 30 minutes
        return Response({"answer": answer})
    except ValueError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as exc:
        return Response(
            {"detail": "Unable to answer the question.", "error": str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def book_summary(request, pk):
    """Generate an AI summary for a specific book."""
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

    cache_key = f"book_summary:{pk}"
    cached_summary = cache.get(cache_key)
    if cached_summary is not None:
        return Response({"summary": cached_summary})

    try:
        summary = generate_book_summary(book)
        cache.set(cache_key, summary, 60 * 60 * 24)  # Cache for 24 hours
        return Response({"summary": summary})
    except Exception as exc:
        return Response(
            {"detail": "Unable to generate summary.", "error": str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def book_recommendations(request, pk):
    """Get book recommendations similar to the specified book."""
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

    try:
        recommendations = recommend_similar_books(book)
        serializer = BookSerializer(recommendations, many=True)
        return Response({"recommendations": serializer.data})
    except Exception as exc:
        return Response(
            {"detail": "Unable to get recommendations.", "error": str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
