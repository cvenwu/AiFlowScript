from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_SECTION_IDS = [
    "hero",
    "current-start",
    "capabilities",
    "weekly-roadmap",
    "project-evolution",
    "architecture",
    "api-overview",
    "data-models",
    "go-fastapi-map",
    "testing-acceptance",
    "interview-story",
]

REQUIRED_KEY_PHRASES = [
    "Go 服务端工程师",
    "FastAPI Agent Backend",
    "每天约 2 小时",
    "Task CRUD",
    "Conversation",
    "Message",
    "Tool",
    "AgentRun",
    "SSE",
    "Pydantic",
    "APIRouter",
    "pytest",
    "TestClient",
    "Mock LLM Provider",
    "30 秒版本",
    "2 分钟版本",
]

FORBIDDEN_PATTERNS = [
    r"https?://",
    r"<script\b",
    r"@import\b",
    r"cdn\.",
    r"fonts\.googleapis",
    r"fonts\.gstatic",
]


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate_roadmap_html.py <html-file>", file=sys.stderr)
        return 2

    html_path = Path(sys.argv[1])
    if not html_path.exists():
        print(f"Missing HTML file: {html_path}", file=sys.stderr)
        return 1

    html = html_path.read_text(encoding="utf-8")

    missing_sections = [
        section_id
        for section_id in REQUIRED_SECTION_IDS
        if f'id="{section_id}"' not in html and f"id='{section_id}'" not in html
    ]
    if missing_sections:
        print(f"Missing required section ids: {', '.join(missing_sections)}", file=sys.stderr)
        return 1

    missing_phrases = [phrase for phrase in REQUIRED_KEY_PHRASES if phrase not in html]
    if missing_phrases:
        print(f"Missing required phrases: {', '.join(missing_phrases)}", file=sys.stderr)
        return 1

    forbidden_hits = [pattern for pattern in FORBIDDEN_PATTERNS if re.search(pattern, html, flags=re.I)]
    if forbidden_hits:
        print(f"Forbidden offline-unsafe patterns found: {', '.join(forbidden_hits)}", file=sys.stderr)
        return 1

    if "<style>" not in html or "</style>" not in html:
        print("Missing embedded <style> block", file=sys.stderr)
        return 1

    if len(html) < 20_000:
        print("HTML looks too small to contain the approved roadmap content", file=sys.stderr)
        return 1

    print("Roadmap HTML validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
