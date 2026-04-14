import { useState } from "react";
import { getBookSummary, getBookRecommendations } from "../api";

export default function BookDetail({ book }) {
  const [summary, setSummary] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [loadingSummary, setLoadingSummary] = useState(false);
  const [loadingRecommendations, setLoadingRecommendations] = useState(false);
  const [showRecommendations, setShowRecommendations] = useState(false);

  const fetchSummary = async () => {
    if (!book) return;
    
    setLoadingSummary(true);
    try {
      const data = await getBookSummary(book.id);
      setSummary(data.summary);
    } catch (error) {
      setSummary("Unable to generate summary at this time.");
    } finally {
      setLoadingSummary(false);
    }
  };

  const fetchRecommendations = async () => {
    if (!book) return;
    
    setLoadingRecommendations(true);
    try {
      const data = await getBookRecommendations(book.id);
      setRecommendations(data.recommendations || []);
      setShowRecommendations(true);
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    } finally {
      setLoadingRecommendations(false);
    }
  };

  if (!book) {
    return (
      <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-slate-800">📘 Book details</h2>
        <p className="mt-3 text-slate-600">Select a book from the list to see more information.</p>
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="flex items-center gap-3 text-xl font-semibold text-slate-800">📘 {book.title}</h2>
      <p className="mt-2 text-sm text-slate-500">by {book.author}</p>
      <p className="mt-4 text-slate-700">{book.description || "No description available."}</p>
      <div className="mt-4 flex flex-wrap gap-3 text-sm text-slate-600">
        <span className="rounded-full bg-slate-100 px-3 py-1">Rating: {book.rating}</span>
        <a
          href={book.book_url}
          target="_blank"
          rel="noreferrer"
          className="rounded-full bg-slate-100 px-3 py-1 text-slate-700 hover:bg-slate-200"
        >
          View book
        </a>
      </div>

      {/* AI Features */}
      <div className="mt-8 space-y-4">
        <div className="flex flex-wrap gap-3">
          <button
            onClick={fetchSummary}
            disabled={loadingSummary}
            className="inline-flex items-center justify-center rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm transition hover:bg-blue-700 hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loadingSummary ? (
              <>
                <span className="mr-2 inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                Generating...
              </>
            ) : (
              "Generate Summary"
            )}
          </button>
          <button
            onClick={fetchRecommendations}
            disabled={loadingRecommendations}
            className="inline-flex items-center justify-center rounded-lg bg-green-600 px-4 py-2 text-sm font-medium text-white shadow-sm transition hover:bg-green-700 hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loadingRecommendations ? (
              <>
                <span className="mr-2 inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                Finding...
              </>
            ) : (
              "Similar Books"
            )}
          </button>
        </div>

        <div className="rounded-lg border border-blue-200 bg-blue-50 p-4 shadow-sm">
          <h3 className="flex items-center gap-2 font-semibold text-blue-900">🤖 AI Summary</h3>
          <p className="mt-2 text-sm leading-7 text-blue-800">
            {summary || "Click Generate Summary to see a book summary here."}
          </p>
        </div>

        {showRecommendations && (
          <div className="rounded-lg border border-green-200 bg-green-50 p-4 shadow-sm">
            <h3 className="flex items-center gap-2 font-semibold text-green-900">📚 Similar Books You Might Like</h3>
            {recommendations.length > 0 ? (
              <div className="mt-3 space-y-2">
                {recommendations.map((recBook) => (
                  <div key={recBook.id} className="rounded bg-white p-3 shadow-sm">
                    <div className="font-medium text-slate-900">{recBook.title}</div>
                    <div className="text-sm text-slate-600">by {recBook.author}</div>
                    <div className="text-sm text-slate-500">Rating: {recBook.rating}</div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="mt-3 text-sm text-slate-600">No similar books found yet.</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
