import { API_BASE_URL } from "../api/config.js";

export async function postChat(payload, signal) {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
    signal,
  });

  if (!response.ok) {
    let message = `Request failed (${response.status})`;
    try {
      const errorBody = await response.json();
      if (errorBody?.detail) {
        message = errorBody.detail;
      }
    } catch {
      // Ignore JSON parsing errors for non-JSON responses.
    }
    throw new Error(message);
  }

  const data = await response.json();
  if (!data || typeof data.reply !== "string") {
    throw new Error("Invalid response from the API.");
  }
  return data;
}
