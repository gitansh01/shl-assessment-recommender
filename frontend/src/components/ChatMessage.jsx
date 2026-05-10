export default function ChatMessage({ role, content, time }) {
  const isUser = role === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
          isUser
            ? "bg-brand-600 text-white"
            : "bg-slate-100 text-slate-800"
        }`}
      >
        <p>{content}</p>
        {time ? (
          <span
            className={`mt-2 block text-[10px] ${
              isUser ? "text-white/70" : "text-slate-500"
            }`}
          >
            {time}
          </span>
        ) : null}
      </div>
    </div>
  );
}
