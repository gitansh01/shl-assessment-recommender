import { useEffect, useRef, useState } from "react";
import SectionHeader from "./SectionHeader.jsx";
import ChatMessage from "./ChatMessage.jsx";
import AssessmentCard from "./AssessmentCard.jsx";
import useChat from "../hooks/useChat.js";

export default function ChatDemo() {
  const { messages, recommendations, isLoading, error, sendMessage, retry } =
    useChat();
  const [draft, setDraft] = useState("");
  const chatScrollRef = useRef(null);

  useEffect(() => {
    if (chatScrollRef.current) {
      chatScrollRef.current.scrollTo({
        top: chatScrollRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [messages, isLoading]);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!draft.trim() || isLoading) {
      return;
    }
    sendMessage(draft);
    setDraft("");
  };

  return (
    <section id="demo" className="section-padding bg-white">
      <div className="container-page">
        <SectionHeader
          label="Interactive Demo"
          title="Recruiter-first conversations that feel natural"
          description="The assistant clarifies hiring needs, refines requirements, and recommends SHL assessments with official URLs."
        />
        <div className="grid gap-8 lg:grid-cols-[1.05fr_0.95fr]">
          <div className="flex h-[560px] flex-col rounded-2xl border border-slate-200 bg-slate-50 p-6 shadow-soft">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-semibold text-slate-900">
                  Recruiter Chat
                </p>
                <p className="text-xs text-slate-500">
                  Connected to the FastAPI backend
                </p>
              </div>
              <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-semibold text-emerald-700">
                Live
              </span>
            </div>
            <div
              ref={chatScrollRef}
              className="mt-4 flex-1 space-y-4 overflow-y-auto pr-2"
            >
              {messages.map((message, index) => (
                <ChatMessage key={`${message.role}-${index}`} {...message} />
              ))}
              {isLoading ? (
                <div className="flex justify-start">
                  <div className="max-w-[70%] rounded-2xl bg-slate-100 px-4 py-3 text-sm text-slate-600">
                    <div className="flex items-center gap-2 text-xs text-slate-500">
                      <span>Assistant is typing</span>
                      <span className="flex items-center gap-1">
                        <span className="typing-dot"></span>
                        <span className="typing-dot"></span>
                        <span className="typing-dot"></span>
                      </span>
                    </div>
                  </div>
                </div>
              ) : null}
            </div>
            {error ? (
              <div className="mt-4 rounded-xl border border-rose-200 bg-rose-50 p-3 text-xs text-rose-700">
                <div className="flex items-center justify-between gap-3">
                  <span>{error}</span>
                  <button
                    type="button"
                    onClick={retry}
                    className="rounded-full bg-white px-3 py-1 text-xs font-semibold text-rose-700 shadow-sm"
                  >
                    Retry
                  </button>
                </div>
              </div>
            ) : null}
            <form
              onSubmit={handleSubmit}
              className="mt-4 border-t border-slate-200 pt-4"
            >
              <div className="flex items-center gap-3">
                <input
                  value={draft}
                  onChange={(event) => setDraft(event.target.value)}
                  placeholder="Describe the role, seniority, and key skills..."
                  className="flex-1 rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 shadow-sm focus:border-brand-600 focus:outline-none focus:ring-2 focus:ring-brand-100"
                  disabled={isLoading}
                />
                <button
                  type="submit"
                  disabled={!draft.trim() || isLoading}
                  className="rounded-xl bg-brand-600 px-4 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700 disabled:cursor-not-allowed disabled:bg-slate-300"
                >
                  Send
                </button>
              </div>
              <p className="mt-2 text-xs text-slate-500">
                Press Enter to send. The full conversation is sent with each
                request.
              </p>
            </form>
          </div>
          <div className="space-y-4">
            <div>
              <p className="text-sm font-semibold text-slate-900">
                Recommended Assessments
              </p>
              <p className="text-xs text-slate-500">
                Results returned from the SHL catalog
              </p>
            </div>
            {recommendations.length ? (
              <div className="space-y-3">
                {recommendations.map((assessment, index) => (
                  <AssessmentCard
                    key={`${assessment.name || "assessment"}-${index}`}
                    {...assessment}
                  />
                ))}
              </div>
            ) : (
              <div className="rounded-2xl border border-dashed border-slate-200 bg-white p-5 text-sm text-slate-500">
                No recommendations yet. Ask about a role or skillset to see
                personalized SHL assessments.
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
