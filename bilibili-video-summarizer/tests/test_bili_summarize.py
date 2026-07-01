import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "bili_summarize.py"


def test_help_runs():
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "check" in result.stdout
    assert "fetch" in result.stdout


import json
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(SCRIPT.parent))
import bili_summarize as bs  # noqa: E402


def _fixture(name):
    return json.loads((Path(__file__).parent / "fixtures" / name).read_text())


def test_validate_cookie_not_set():
    result = bs.validate_cookie(None)
    assert result == {"valid": False, "reason": "not_set"}


def test_validate_cookie_valid():
    session = MagicMock()
    resp = MagicMock()
    resp.json.return_value = _fixture("nav_valid.json")
    resp.raise_for_status = MagicMock()
    session.get.return_value = resp

    result = bs.validate_cookie("SESSDATA=abc; bili_jct=x", session=session)
    assert result == {"valid": True, "uname": "test_user", "mid": 12345}


def test_validate_cookie_invalid():
    session = MagicMock()
    resp = MagicMock()
    resp.json.return_value = _fixture("nav_invalid.json")
    resp.raise_for_status = MagicMock()
    session.get.return_value = resp

    result = bs.validate_cookie("SESSDATA=stale", session=session)
    assert result == {"valid": False, "reason": "invalid"}


def test_validate_cookie_missing_sessdata():
    result = bs.validate_cookie("some=thing")
    assert result == {"valid": False, "reason": "invalid"}
