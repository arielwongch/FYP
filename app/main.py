"""Local HTTP server for the backend API and browser UI."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from urllib.parse import urlparse

from .config import Settings
from .llm_client import create_client
from .react_loop import run_loop
from .store import ConversationStore


def create_server(settings: Settings) -> ThreadingHTTPServer:
    store = ConversationStore(Path(".data"))
    client = create_client(settings)
    ui_dir = Path(__file__).parent.parent / "ui"

    class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            if parsed.path == "/api/conversations":
                self._send_json([item.to_dict() for item in store.list()])
                return
            if parsed.path.startswith("/api/conversations/"):
                conversation_id = parsed.path.rsplit("/", 1)[-1]
                try:
                    self._send_json(store.get(conversation_id).to_dict())
                except KeyError:
                    self._send_error_json(404, "Conversation not found.")
                return
            if parsed.path == "/" or parsed.path.startswith("/ui/"):
                self._serve_ui(parsed.path)
                return
            self._send_error_json(404, "Not found.")

        def do_POST(self) -> None:
            parsed = urlparse(self.path)
            payload = self._read_json()
            if payload is None:
                return
            if parsed.path == "/api/conversations":
                conversation = store.create(
                    model=str(payload.get("model", settings.qwen_model)),
                    max_turns=int(payload.get("max_turns", settings.max_agent_turns)),
                    temperature=float(payload.get("temperature", 0.2)),
                    system_prompt=str(payload.get("system_prompt", "You are a careful research assistant.")),
                )
                self._send_json(conversation.to_dict(), status=201)
                return
            if parsed.path == "/api/chat":
                self._stream_chat(payload, store, client)
                return
            self._send_error_json(404, "Not found.")

        def do_PATCH(self) -> None:
            parsed = urlparse(self.path)
            payload = self._read_json()
            if payload is None or not parsed.path.startswith("/api/conversations/"):
                if payload is not None:
                    self._send_error_json(404, "Not found.")
                return
            conversation_id = parsed.path.rsplit("/", 1)[-1]
            try:
                conversation = store.get(conversation_id)
                store.update_settings(
                    conversation,
                    model=str(payload.get("model", conversation.model)),
                    temperature=float(payload.get("temperature", conversation.temperature)),
                    max_turns=int(payload.get("max_turns", conversation.max_turns)),
                    system_prompt=str(payload.get("system_prompt", conversation.system_prompt)),
                )
                self._send_json(conversation.to_dict())
            except (KeyError, ValueError):
                self._send_error_json(400, "Conversation settings are invalid.")

        def _stream_chat(self, payload: dict[str, object], store: ConversationStore, client: object) -> None:
            conversation_id = payload.get("conversation_id")
            prompt = payload.get("prompt")
            if not isinstance(conversation_id, str) or not isinstance(prompt, str):
                self._send_error_json(400, "conversation_id and prompt are required.")
                return
            try:
                conversation = store.get(conversation_id)
                store.append_user_message(conversation, prompt)
            except (KeyError, ValueError):
                self._send_error_json(400, "Conversation or prompt is invalid.")
                return

            messages = [{"role": "system", "content": conversation.system_prompt}]
            messages.extend(conversation.messages)
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()
            final_content = ""
            for event in run_loop(
                client, messages, conversation.model, conversation.temperature, conversation.max_turns
            ):
                self.wfile.write(event.to_sse().encode("utf-8"))
                self.wfile.flush()
                if event.kind == "final":
                    final_content = event.content
            if final_content:
                store.append_assistant_message(conversation, final_content)

        def _read_json(self) -> dict[str, object] | None:
            try:
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length))
                if not isinstance(payload, dict):
                    raise ValueError
                return payload
            except (ValueError, json.JSONDecodeError):
                self._send_error_json(400, "Request body must be a JSON object.")
                return None

        def _serve_ui(self, path: str) -> None:
            relative_path = "index.html" if path == "/" else path.removeprefix("/ui/")
            if "/" in relative_path or relative_path not in {"index.html", "styles.css", "app.js"}:
                self._send_error_json(404, "UI asset not found.")
                return
            asset_path = ui_dir / relative_path
            content_types = {"index.html": "text/html", "styles.css": "text/css", "app.js": "text/javascript"}
            body = asset_path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", f"{content_types[relative_path]}; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _send_json(self, payload: object, status: int = 200) -> None:
            body = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _send_error_json(self, status: int, message: str) -> None:
            self._send_json({"error": message}, status=status)

        def log_message(self, format: str, *args: object) -> None:
            print(format % args)

    return ThreadingHTTPServer((settings.host, settings.port), RequestHandler)


def main() -> None:
    settings = Settings.from_env()
    server = create_server(settings)
    print(f"FYP research console listening on http://{settings.host}:{settings.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()