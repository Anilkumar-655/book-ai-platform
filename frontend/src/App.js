import { useEffect, useState } from "react";
import { getBooks, askQuestion } from "./api";
import BookList from "./components/BookList";
import BookDetail from "./components/BookDetail";
import AskQuestion from "./components/AskQuestion";

function App() {
  const [books, setBooks] = useState([]);
  const [selectedBook, setSelectedBook] = useState(null);
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    loadBooks();
  }, []);

  const loadBooks = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await getBooks();
      setBooks(data);
      if (data.length > 0) {
        setSelectedBook(data[0]);
      }
    } catch (err) {
      setError("Unable to load the book list. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const handleAsk = async (question) => {
    setLoading(true);
    setError("");
    setAnswer("");

    try {
      const data = await askQuestion(question);
      setAnswer(data.answer || "No answer was returned.");
    } catch (err) {
      setError("Failed to get an answer from the backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-blue-50 text-slate-900">
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <header className="mb-8">
          <div className="flex flex-col gap-4 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-sm uppercase tracking-[0.24em] text-sky-600">Document Intelligence</p>
              <h1 className="mt-2 text-3xl font-semibold text-slate-900">Book AI Platform</h1>
              <p className="mt-2 max-w-2xl text-slate-600">
                Browse books, inspect details, and ask intelligent questions about the collection.
              </p>
            </div>
            <div className="rounded-3xl bg-slate-100 px-6 py-4 text-sm text-slate-700 shadow-inner">
              API: <span className="font-semibold text-slate-900">{process.env.REACT_APP_API_URL || "http://127.0.0.1:8000/api"}</span>
            </div>
          </div>
        </header>

        {error && (
          <div className="mb-6 rounded-2xl border border-rose-200 bg-rose-50 p-4 text-rose-900">
            {error}
          </div>
        )}

        {loading && books.length === 0 ? (
          <div className="mb-6 rounded-2xl border border-slate-200 bg-white p-6 text-slate-700 shadow-sm">
            Loading books, please wait...
          </div>
        ) : (
          <div className="grid gap-6 xl:grid-cols-[360px_1fr]">
            <BookList books={books} onSelectBook={setSelectedBook} selectedBookId={selectedBook?.id} />

            <div className="space-y-6">
              <BookDetail book={selectedBook} />
              <AskQuestion onAsk={handleAsk} answer={answer} loading={loading} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
