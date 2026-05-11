import { API_BASE_URL } from "../api/config.js";

const DEFAULT_TIMEOUT_MS = 25000;

export async function postChat(payload, options = {}) {
  const { timeoutMs = DEFAULT_TIMEOUT_MS } = options;
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
      signal: controller.signal,
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
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new Error("Request timed out. Please try again.");
    }
    throw error;
  } finally {
    clearTimeout(timeoutId);
  }
}
