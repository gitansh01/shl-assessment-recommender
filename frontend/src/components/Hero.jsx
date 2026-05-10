import Button from "./Button.jsx";

export default function Hero() {
  return (
    <section id="product" className="section-padding">
      <div className="container-page grid gap-12 md:grid-cols-[1.15fr_0.85fr]">
        <div className="space-y-6">
          <span className="text-sm font-semibold uppercase tracking-wide text-brand-700">
            SHL Conversational Assessment Recommender
          </span>
          <h1 className="text-4xl font-semibold leading-tight text-slate-900 sm:text-5xl">
            Find the Right SHL Assessments Through Conversation
          </h1>
          <p className="text-lg text-slate-600">
            An AI-powered assistant that helps recruiters translate hiring needs
            into a trusted shortlist of SHL assessments — grounded in the
            official catalog and easy to refine.
          </p>
          <div className="flex flex-wrap gap-4">
            <Button href="#demo">Try Demo</Button>
            <Button href="#api" variant="secondary">
              View API Docs
            </Button>
          </div>
          <div className="flex flex-wrap gap-6 text-sm text-slate-500">
            <div className="flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-emerald-500"></span>
              Live catalog recommendations
            </div>
            <div className="flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-blue-500"></span>
              Enterprise-ready UX
            </div>
          </div>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-soft">
          <div className="flex items-center justify-between text-xs text-slate-500">
            <span className="font-semibold text-slate-700">Recruiter Snapshot</span>
            <span>Updated today</span>
          </div>
          <div className="mt-6 space-y-4">
            <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">
              <p className="text-sm font-semibold text-slate-900">
                Role: Java Developer
              </p>
              <p className="mt-1 text-xs text-slate-500">
                Level: Mid–Senior • Location: Remote
              </p>
            </div>
            <div className="rounded-xl border border-slate-200 bg-white p-4">
              <p className="text-sm font-semibold text-slate-900">
                Key Skills
              </p>
              <p className="mt-1 text-xs text-slate-500">
                Spring Boot, SQL, Communication
              </p>
            </div>
            <div className="rounded-xl border border-slate-200 bg-white p-4">
              <p className="text-sm font-semibold text-slate-900">
                Recommended Mix
              </p>
              <p className="mt-1 text-xs text-slate-500">
                Technical knowledge + personality fit
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
