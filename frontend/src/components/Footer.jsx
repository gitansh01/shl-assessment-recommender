export default function Footer() {
  return (
    <footer id="footer" className="border-t border-slate-200 bg-white">
      <div className="container-page flex flex-col items-start justify-between gap-6 py-10 text-sm text-slate-500 md:flex-row md:items-center">
        <div>
          <p className="font-semibold text-slate-900">
            SHL Assessment Recommender
          </p>
          <p className="text-xs text-slate-500">
            Conversational assessment discovery for recruiters.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-4 text-xs text-slate-500">
          <a
            href="https://github.com/your-username/shl-assessment-recommender"
            className="font-semibold text-slate-600 hover:text-slate-900"
          >
            GitHub
          </a>
          <a href="#api" className="font-semibold text-slate-600 hover:text-slate-900">
            API Docs
          </a>
          <span>© 2026 SHL Conversational Assessment Recommender</span>
        </div>
      </div>
    </footer>
  );
}
