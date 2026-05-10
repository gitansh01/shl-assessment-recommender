import SectionHeader from "./SectionHeader.jsx";
import { apiPreview } from "../data/content.js";

export default function ApiPreview() {
  return (
    <section id="api" className="section-padding">
      <div className="container-page">
        <SectionHeader
          label="API Preview"
          title="Clean, predictable API responses"
          description="A stateless FastAPI endpoint returns clear recommendations, official URLs, and conversation-safe replies."
        />
        <div className="grid gap-6 lg:grid-cols-2">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-soft">
            <div className="flex items-center justify-between text-xs text-slate-500">
              <span className="font-semibold text-slate-700">POST /chat</span>
              <span>Request</span>
            </div>
            <pre className="mt-4 max-h-80 overflow-auto whitespace-pre-wrap text-xs font-mono leading-relaxed text-slate-700">
              {apiPreview.request}
            </pre>
          </div>
          <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5 shadow-soft">
            <div className="flex items-center justify-between text-xs text-slate-500">
              <span className="font-semibold text-slate-700">200 OK</span>
              <span>Response</span>
            </div>
            <pre className="mt-4 max-h-80 overflow-auto whitespace-pre-wrap text-xs font-mono leading-relaxed text-slate-700">
              {apiPreview.response}
            </pre>
          </div>
        </div>
      </div>
    </section>
  );
}
