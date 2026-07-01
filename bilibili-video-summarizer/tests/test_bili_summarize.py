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
from unittest.mock import MagicMock

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


def test_extract_audio(tmp_path):
    calls = []

    def fake_run(cmd, *a, **kw):
        calls.append(cmd)
        rv = MagicMock(); rv.returncode = 0; return rv

    audio = tmp_path / "a.wav"
    result = bs.extract_audio(tmp_path / "v.mp4", audio, runner=fake_run)
    assert result == audio
    assert "-ar" in calls[0] and "16000" in calls[0]


def test_transcribe_with_whisper(tmp_path):
    fake_model = MagicMock()
    fake_model.transcribe.return_value = {
        "segments": [
            {"start": 1.2, "text": " 你好"},
            {"start": 3.4, "text": " 世界"},
        ]
    }
    fake_loader = MagicMock(return_value=fake_model)

    result = bs.transcribe_with_whisper(tmp_path / "a.wav", "base", whisper_loader=fake_loader)
    assert result == [
        {"start": 1.2, "text": "你好"},
        {"start": 3.4, "text": "世界"},
    ]
    fake_loader.assert_called_once_with("base")


def test_sanitize_dirname():
    assert bs.sanitize_dirname("A/B:C?<D>|E") == "A_B_C__D__E"
    assert bs.sanitize_dirname("  标题  ") == "标题"


def test_cmd_fetch_end_to_end(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("BILIBILI_COOKIE", "SESSDATA=abc; bili_jct=x")

    monkeypatch.setattr(bs, "validate_cookie", lambda c, session=None: {"valid": True, "uname": "u", "mid": 1})
    monkeypatch.setattr(bs, "parse_bvid", lambda url: "BV1xx411c7mD")
    monkeypatch.setattr(bs, "fetch_video_info", lambda bvid, cookie, session=None: {
        "title": "示例标题", "author": "UP", "duration_sec": 300, "cid": 1,
    })
    monkeypatch.setattr(bs, "fetch_subtitle", lambda bvid, cid, cookie, session=None: [
        {"start": 0.0, "text": "开场"}, {"start": 10.0, "text": "内容"},
    ])
    def fake_download(url, workdir, cookie, **kw):
        (Path(workdir) / "source.mp4").write_bytes(b"x")
        return Path(workdir) / "source.mp4"
    monkeypatch.setattr(bs, "download_video", fake_download)
    def fake_frames(video, frames_dir, duration_sec, **kw):
        Path(frames_dir).mkdir(parents=True, exist_ok=True)
        return [{"time": 5.0, "path": "frames/frame_0005.jpg"}]
    monkeypatch.setattr(bs, "extract_key_frames", fake_frames)

    ns = argparse.Namespace(
        url="https://www.bilibili.com/video/BV1xx411c7mD",
        outdir=str(tmp_path), keep_video=False,
    )
    code = bs.cmd_fetch(ns)
    assert code == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["title"] == "示例标题"
    assert payload["subtitle_source"] == "bilibili_cc"
    assert payload["segments"][0] == {"start": 0.0, "text": "开场"}
    assert payload["frames"] == [{"time": 5.0, "path": "frames/frame_0005.jpg"}]
    assert Path(payload["workdir"]).name == "示例标题"
    assert not (Path(payload["workdir"]) / "source.mp4").exists()


def test_cmd_fetch_falls_back_to_whisper(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("BILIBILI_COOKIE", "SESSDATA=abc")
    monkeypatch.setattr(bs, "validate_cookie", lambda c, session=None: {"valid": True, "uname": "u", "mid": 1})
    monkeypatch.setattr(bs, "parse_bvid", lambda url: "BV1")
    monkeypatch.setattr(bs, "fetch_video_info", lambda *a, **kw: {"title": "T", "author": "U", "duration_sec": 60, "cid": 1})
    monkeypatch.setattr(bs, "fetch_subtitle", lambda *a, **kw: None)  # 无字幕
    monkeypatch.setattr(bs, "download_video", lambda url, workdir, cookie, **kw: Path(workdir) / "source.mp4")
    monkeypatch.setattr(bs, "extract_audio", lambda video, out, **kw: out)
    monkeypatch.setattr(bs, "transcribe_with_whisper", lambda audio, model_name="base", whisper_loader=None: [{"start": 0.0, "text": "hi"}])
    monkeypatch.setattr(bs, "extract_key_frames", lambda *a, **kw: [])

    ns = argparse.Namespace(url="x", outdir=str(tmp_path), keep_video=True)
    code = bs.cmd_fetch(ns)
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["subtitle_source"] == "whisper"
    assert payload["segments"] == [{"start": 0.0, "text": "hi"}]


def test_cmd_fetch_rejects_invalid_cookie(monkeypatch, tmp_path, capsys):
    monkeypatch.delenv("BILIBILI_COOKIE", raising=False)
    ns = argparse.Namespace(url="x", outdir=str(tmp_path), keep_video=False)
    code = bs.cmd_fetch(ns)
    assert code == 2
    assert "cookie" in capsys.readouterr().out.lower()


import argparse


def test_cmd_fetch_empty_subtitle_list_is_bilibili_cc(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("BILIBILI_COOKIE", "SESSDATA=abc")
    monkeypatch.setattr(bs, "validate_cookie", lambda c, session=None: {"valid": True, "uname": "u", "mid": 1})
    monkeypatch.setattr(bs, "parse_bvid", lambda url: "BV1")
    monkeypatch.setattr(bs, "fetch_video_info", lambda *a, **kw: {"title": "T", "author": "U", "duration_sec": 60, "cid": 1})
    monkeypatch.setattr(bs, "fetch_subtitle", lambda *a, **kw: [])  # 空列表：有轨但无内容
    monkeypatch.setattr(bs, "download_video", lambda url, workdir, cookie, **kw: Path(workdir) / "source.mp4")
    def _boom(*a, **kw):
        raise AssertionError("空列表不应触发 whisper 转录")
    monkeypatch.setattr(bs, "transcribe_with_whisper", _boom)
    monkeypatch.setattr(bs, "extract_key_frames", lambda *a, **kw: [])

    ns = argparse.Namespace(url="x", outdir=str(tmp_path), keep_video=True)
    code = bs.cmd_fetch(ns)
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["subtitle_source"] == "bilibili_cc"
    assert payload["segments"] == []
