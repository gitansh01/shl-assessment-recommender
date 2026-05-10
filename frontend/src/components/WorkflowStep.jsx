export default function WorkflowStep({ title, description, index }) {
  return (
    <div className="flex flex-1 flex-col rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <span className="text-xs font-semibold uppercase tracking-wide text-slate-500">
        Step {index}
      </span>
      <h4 className="mt-2 text-sm font-semibold text-slate-900">{title}</h4>
      <p className="mt-2 text-sm text-slate-600">{description}</p>
    </div>
  );
}
