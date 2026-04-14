export default function BookList({ books, onSelectBook, selectedBookId }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="text-xl font-semibold text-slate-800">Books</h2>
      <p className="text-sm text-slate-500">Select a book to view details.</p>
      <div className="mt-4 space-y-3">
        {books.length === 0 ? (
          <div className="rounded-lg border border-dashed border-slate-300 bg-slate-50 p-6 text-slate-500">
            No books available
          </div>
        ) : (
          books.map((book) => (
            <button
              key={book.id}
              onClick={() => onSelectBook(book)}
              className={`w-full rounded-xl border px-4 py-3 text-left transition-transform duration-200 ${
                selectedBookId === book.id
                  ? "border-sky-500 bg-sky-50 shadow-md"
                  : "border-slate-200 bg-white hover:border-slate-400 hover:shadow-md hover:scale-[1.02]"
              }`}
            >
              <div className="flex items-center gap-2 font-semibold text-slate-900">
                <span>📚</span>
                <span>{book.title}</span>
              </div>
              <div className="text-sm text-slate-600">{book.author}</div>
            </button>
          ))
        )}
      </div>
    </div>
  );
}
