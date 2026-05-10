import Badge from "./Badge.jsx";

export default function SectionHeader({ label, title, description }) {
  return (
    <div className="mb-10 flex flex-col gap-3">
      {label ? <Badge>{label}</Badge> : null}
      <h2 className="text-2xl font-semibold text-slate-900 sm:text-3xl">
        {title}
      </h2>
      <p className="max-w-2xl text-base text-slate-600">{description}</p>
    </div>
  );
}
