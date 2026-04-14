from django.urls import path

from . import views

urlpatterns = [
    path("books/", views.book_list, name="book-list"),
    path("books/<int:pk>/", views.book_detail, name="book-detail"),
    path("books/<int:pk>/summary/", views.book_summary, name="book-summary"),
    path("books/<int:pk>/recommendations/", views.book_recommendations, name="book-recommendations"),
    path("ask/", views.ask_question, name="ask-question"),
]
