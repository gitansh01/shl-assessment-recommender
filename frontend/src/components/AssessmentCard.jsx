export default function AssessmentCard({
  name,
  type,
  test_type: testType,
  description,
  url,
}) {
  const displayType = type || testType || "Assessment";
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm transition hover:shadow-soft">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold text-slate-900">{name}</h4>
        <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-600">
          {displayType} · Test Type
        </span>
      </div>
      <p className="mt-2 text-xs text-slate-600">{description}</p>
      <a
        href={url}
        className="mt-3 inline-flex items-center justify-center rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-semibold text-slate-700 hover:border-slate-300 hover:text-slate-900"
      >
        Official SHL URL →
      </a>
    </div>
  );
}
