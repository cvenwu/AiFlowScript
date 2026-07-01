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


import pytest


def test_parse_bvid_standard_url():
    assert bs.parse_bvid("https://www.bilibili.com/video/BV1xx411c7mD/") == "BV1xx411c7mD"


def test_parse_bvid_with_query():
    assert bs.parse_bvid("https://www.bilibili.com/video/BV1xx411c7mD?p=1&spm_id=abc") == "BV1xx411c7mD"


def test_parse_bvid_short_url_rejected():
    with pytest.raises(ValueError):
        bs.parse_bvid("https://b23.tv/abcd")


def test_fetch_video_info():
    session = MagicMock()
    resp = MagicMock()
    resp.json.return_value = _fixture("view_valid.json")
    resp.raise_for_status = MagicMock()
    session.get.return_value = resp

    info = bs.fetch_video_info("BV1xx411c7mD", "SESSDATA=x", session=session)
    assert info == {
        "title": "示例视频标题",
        "author": "示例UP主",
        "duration_sec": 615,
        "cid": 987654321,
    }


def test_fetch_subtitle_present():
    session = MagicMock()

    player_resp = MagicMock()
    player_resp.json.return_value = _fixture("player_with_subtitle.json")
    player_resp.raise_for_status = MagicMock()

    sub_resp = MagicMock()
    sub_resp.json.return_value = _fixture("subtitle_sample.json")
    sub_resp.raise_for_status = MagicMock()

    session.get.side_effect = [player_resp, sub_resp]

    segments = bs.fetch_subtitle("BV1", 1, "SESSDATA=x", session=session)
    assert segments == [
        {"start": 0.5, "text": "大家好"},
        {"start": 3.2, "text": "今天我们讲解一个新话题"},
    ]


def test_fetch_subtitle_none():
    session = MagicMock()
    resp = MagicMock()
    resp.json.return_value = _fixture("player_no_subtitle.json")
    resp.raise_for_status = MagicMock()
    session.get.return_value = resp

    assert bs.fetch_subtitle("BV1", 1, "SESSDATA=x", session=session) is None


def test_extract_key_frames_scene_detection(tmp_path, monkeypatch):
    frames_dir = tmp_path / "frames"
    frames_dir.mkdir()

    # 模拟场景检测抽出 5 张帧
    def fake_run(cmd, *a, **kw):
        for t in [10, 40, 90, 150, 300]:
            (frames_dir / f"frame_{t:04d}.jpg").write_bytes(b"fake")
        rv = MagicMock()
        rv.returncode = 0
        return rv

    result = bs.extract_key_frames(tmp_path / "v.mp4", frames_dir, 600, runner=fake_run)
    assert len(result) == 5
    assert result[0] == {"time": 10.0, "path": "frames/frame_0010.jpg"}


def test_extract_key_frames_fallback(tmp_path):
    frames_dir = tmp_path / "frames"
    frames_dir.mkdir()

    calls = {"n": 0}

    def fake_run(cmd, *a, **kw):
        calls["n"] += 1
        # 第 1 次：场景检测只出 1 张 → 触发降级
        # 第 2 次：均匀抽帧写 8 张
        if calls["n"] == 1:
            (frames_dir / "frame_0005.jpg").write_bytes(b"x")
        else:
            for i in range(8):
                (frames_dir / f"frame_{i*60:04d}.jpg").write_bytes(b"x")
        rv = MagicMock(); rv.returncode = 0
        return rv

    result = bs.extract_key_frames(tmp_path / "v.mp4", frames_dir, 480, runner=fake_run)
    assert len(result) == 8
    assert calls["n"] == 2
