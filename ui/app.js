const state = { conversations: [], selected: null, busy: false, thought: "", controller: null };
const $ = (id) => document.getElementById(id);

async function request(path, options = {}) {
  const response = await fetch(path, options);
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || "Request failed");
  return payload;
}

function renderMarkdown(text) {
  return escapeHtml(text)
    .replace(/^### (.*)$/gm, "<h3>$1</h3>")
    .replace(/^## (.*)$/gm, "<h2>$1</h2>")
    .replace(/^# (.*)$/gm, "<h1>$1</h1>")
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\n/g, "<br>");
}

function escapeHtml(text) {
  return text.replace(/[&<>'"]/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[character]));
}

function renderConversations() {
  $("conversation-count").textContent = state.conversations.length;
  $("conversation-list").innerHTML = state.conversations.map((item) => `
    <button class="conversation-item ${state.selected?.id === item.id ? "active" : ""}" data-id="${item.id}">
      <strong>${escapeHtml(item.title)}</strong><small>${new Date(item.updated_at).toLocaleDateString()}</small>
    </button>`).join("");
  document.querySelectorAll(".conversation-item").forEach((button) => button.addEventListener("click", () => selectConversation(button.dataset.id)));
}

function renderConversation() {
  $("header-title").textContent = state.selected?.title || "New conversation";
  $("empty-state").classList.toggle("hidden", Boolean(state.selected?.messages?.length));
  const list = $("message-list");
  list.innerHTML = (state.selected?.messages || []).map((message) => `
    <article class="message ${message.role}"><div class="message-label">${message.role === "user" ? "You" : "Agent"}</div>
      <div class="message-body">${message.role === "assistant" ? renderMarkdown(message.content) : escapeHtml(message.content)}</div>
    </article>`).join("");
  list.scrollTop = list.scrollHeight;
  if (state.selected) {
    $("model-input").value = state.selected.model;
    $("temperature-input").value = state.selected.temperature;
    $("temperature-value").value = state.selected.temperature;
    $("temperature-value").textContent = state.selected.temperature;
    $("turns-input").value = state.selected.max_turns;
    $("system-input").value = state.selected.system_prompt;
  }
}

async function loadConversations() {
  state.conversations = await request("/api/conversations");
  renderConversations();
  if (state.conversations[0]) await selectConversation(state.conversations[0].id);
}

async function selectConversation(id) {
  state.selected = await request(`/api/conversations/${id}`);
  renderConversations(); renderConversation();
}

async function newConversation() {
  state.selected = await request("/api/conversations", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ model: $("model-input").value, temperature: Number($("temperature-input").value), max_turns: Number($("turns-input").value), system_prompt: $("system-input").value }) });
  state.conversations.unshift(state.selected); renderConversations(); renderConversation();
}

async function saveSettings() {
  if (!state.selected || state.busy) return;
  try {
    state.selected = await request(`/api/conversations/${state.selected.id}`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ model: $("model-input").value, temperature: Number($("temperature-input").value), max_turns: Number($("turns-input").value), system_prompt: $("system-input").value }) });
    state.conversations = state.conversations.map((item) => item.id === state.selected.id ? state.selected : item);
    renderConversations(); renderConversation();
  } catch (error) { $("stream-status").textContent = error.message; }
}

async function sendPrompt(prompt) {
  if (!prompt.trim() || state.busy) return;
  if (!state.selected) await newConversation();
  state.busy = true; $("send-button").disabled = true; $("stream-status").textContent = "Generating...";
  $("stop-button").classList.remove("hidden"); state.controller = new AbortController();
  state.selected.messages.push({ role: "user", content: prompt }); renderConversation();
  $("prompt").value = ""; $("thought-panel").classList.remove("hidden"); $("thought-content").textContent = ""; state.thought = "";
  try {
    const response = await fetch("/api/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ conversation_id: state.selected.id, prompt }), signal: state.controller.signal });
    if (!response.ok || !response.body) throw new Error("Unable to open stream");
    const reader = response.body.getReader(); const decoder = new TextDecoder(); let buffer = ""; let final = "";
    while (true) { const { value, done } = await reader.read(); if (done) break; buffer += decoder.decode(value, { stream: true });
      const blocks = buffer.split("\n\n"); buffer = blocks.pop();
      blocks.forEach((block) => { const eventName = block.match(/^event: (.+)$/m)?.[1]; const data = block.match(/^data: (.+)$/m)?.[1]; if (!data) return; const event = JSON.parse(data); if (eventName === "thought") { state.thought += event.content; $("thought-content").textContent = state.thought; } if (eventName === "final") final += event.content; if (eventName === "error") throw new Error(event.content); });
    }
    if (final) state.selected.messages.push({ role: "assistant", content: final }); renderConversation(); await loadConversations();
  } catch (error) { $("stream-status").textContent = error.name === "AbortError" ? "Stopped" : error.message; } finally { state.busy = false; state.controller = null; $("send-button").disabled = false; $("stop-button").classList.add("hidden"); if ($("stream-status").textContent === "Generating...") $("stream-status").textContent = "Ready"; }
}

$("new-chat").addEventListener("click", newConversation);
$("chat-form").addEventListener("submit", (event) => { event.preventDefault(); sendPrompt($("prompt").value); });
$("stop-button").addEventListener("click", () => state.controller?.abort());
$("prompt").addEventListener("keydown", (event) => { if (event.key === "Enter" && !event.shiftKey) { event.preventDefault(); $("chat-form").requestSubmit(); } });
$("settings-toggle").addEventListener("click", () => $("settings-panel").classList.add("open"));
$("settings-close").addEventListener("click", () => $("settings-panel").classList.remove("open"));
$("thought-toggle").addEventListener("click", () => { $("thought-content").classList.toggle("hidden"); $("thought-toggle").textContent = $("thought-content").classList.contains("hidden") ? "show" : "hide"; });
$("temperature-input").addEventListener("input", (event) => { $("temperature-value").textContent = event.target.value; });
$("model-input").addEventListener("change", saveSettings);
$("temperature-input").addEventListener("change", saveSettings);
$("turns-input").addEventListener("change", saveSettings);
$("system-input").addEventListener("change", saveSettings);
document.querySelectorAll("[data-prompt]").forEach((button) => button.addEventListener("click", () => { $("prompt").value = button.dataset.prompt; $("prompt").focus(); }));
loadConversations().catch((error) => { $("stream-status").textContent = error.message; });