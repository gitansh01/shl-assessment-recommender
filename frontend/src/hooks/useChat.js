import { useCallback, useState } from "react";
import { postChat } from "../services/chatApi.js";

const formatTime = (date = new Date()) =>
  date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

const buildMessage = (role, content) => ({
  role,
  content,
  time: formatTime(),
});

const initialMessage = buildMessage(
  "assistant",
  "Hi! Tell me about the role you're hiring for and any key skills or seniority."
);

export default function useChat() {
  const [messages, setMessages] = useState([initialMessage]);
  const [recommendations, setRecommendations] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [lastFailedPayload, setLastFailedPayload] = useState(null);

  const sendPayload = useCallback(async (payload) => {
    setIsLoading(true);
    setError("");
    try {
      const data = await postChat(payload, { timeoutMs: 25000 });
      if (data.reply?.trim()) {
        setMessages((prev) => [...prev, buildMessage("assistant", data.reply)]);
      }
      setRecommendations(
        Array.isArray(data.recommendations) ? data.recommendations : []
      );
      setLastFailedPayload(null);
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "Unable to reach the API. Please try again.";
      setError(message);
      setLastFailedPayload(payload);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const sendMessage = useCallback(
    async (text) => {
      const trimmed = text.trim();
      if (!trimmed || isLoading) {
        return;
      }

      setError("");
      setLastFailedPayload(null);
      const userMessage = buildMessage("user", trimmed);
      const nextMessages = [...messages, userMessage];
      setMessages(nextMessages);

      const payload = {
        messages: nextMessages.map(({ role, content }) => ({ role, content })),
      };
      await sendPayload(payload);
    },
    [isLoading, messages, sendPayload]
  );

  const retry = useCallback(async () => {
    if (!lastFailedPayload || isLoading) {
      return;
    }
    await sendPayload(lastFailedPayload);
  }, [isLoading, lastFailedPayload, sendPayload]);

  return {
    messages,
    recommendations,
    isLoading,
    error,
    sendMessage,
    retry,
  };
}
