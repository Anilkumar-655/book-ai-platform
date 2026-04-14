import { useState } from "react";

export default function AskQuestion({ onAsk, answer, loading }) {
  const [question, setQuestion] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!question.trim()) {
      // Prevent empty submission and show validation message
      setErrorMessage("Please enter a question");
      return;
    }
    setErrorMessage("");
    onAsk(question.trim());
    setQuestion("");
  };

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-xl font-semibold text-slate-800">🤖 Ask a question</h2>
      <p className="mt-2 text-sm text-slate-500">Ask about the books in the platform.</p>
      <form onSubmit={handleSubmit} className="mt-4 space-y-4">
        <label className="block">
          <span className="text-sm font-medium text-slate-700">Your question</span>
          <input
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            className="mt-2 w-full rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 outline-none transition focus:border-sky-500 focus:bg-white"
            placeholder="What books are best for learning Python?"
          />
        </label>
        <button
          type="submit"
          className="inline-flex items-center justify-center rounded-xl bg-sky-600 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-sky-700 hover:shadow-md disabled:cursor-not-allowed disabled:bg-slate-400 disabled:opacity-70"
          disabled={loading}
        >
          {loading ? (
            <>
              <span className="mr-2 inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
              Loading...
            </>
          ) : (
            "Ask AI"
          )}
        </button>
      </form>

      {errorMessage && (
        <p className="mt-3 text-sm text-rose-600">{errorMessage}</p>
      )}

      <div className="mt-6">
        <h3 className="text-base font-semibold text-slate-900">AI Answer</h3>
        <div className="mt-3 rounded-3xl border border-slate-200 bg-slate-50 p-5 shadow-sm">
          {answer ? (
            <p className="whitespace-pre-line text-sm leading-7 text-slate-700">{answer}</p>
          ) : (
            <p className="text-sm leading-6 text-slate-500">Your AI answer will appear here once you ask a question.</p>
          )}
        </div>
      </div>
    </div>
  );
}
