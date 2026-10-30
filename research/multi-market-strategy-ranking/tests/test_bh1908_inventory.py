"""Offline regression tests: no network or YouTube credentials."""
import importlib.util
import io
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "fetch_youtube_channel_videos.py"
spec = importlib.util.spec_from_file_location("bh1908_inventory", SCRIPT)
inventory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventory)


def test_valid_atom_feed_creates_real_video_row():
    xml = f"""<feed xmlns="http://www.w3.org/2005/Atom"
        xmlns:yt="http://www.youtube.com/xml/schemas/2015">
      <yt:channelId>{inventory.CHANNEL_ID}</yt:channelId>
      <title>投資腦袋の熊敖</title>
      <entry><yt:videoId>SPerBx16hMA</yt:videoId>
      <title>SMC 實戰教學</title><published>2025-12-30T00:00:00Z</published></entry>
    </feed>""".encode("utf-8")
    rows, status = inventory.from_feed(lambda req, timeout: io.BytesIO(xml))
    assert len(rows) == 1
    assert rows[0]["Video ID"] == "SPerBx16hMA"
    assert rows[0]["Strategy Type"] == "SMC"
    assert rows[0]["Rule Status"] == "RULES_PENDING"
    assert status["coverage"] == "PARTIAL_RECENT_ONLY"


def test_wrong_channel_feed_fails_closed():
    xml = b"""<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:yt="http://www.youtube.com/xml/schemas/2015">
      <yt:channelId>UCxxxxxxxxxxxxxxxxxxxxxx</yt:channelId>
      <title>Wrong channel</title></feed>"""
    with pytest.raises(ValueError, match="identity"):
        inventory.from_feed(lambda req, timeout: io.BytesIO(xml))


def test_existing_reviewed_strategy_rules_are_preserved():
    old = inventory.make_row("SPerBx16hMA", "old title", source="old")
    old.update({"Rule Status": "REVIEWED", "Notes": "Manual rules", "Strategy Type": "CUSTOM"})
    new = inventory.make_row("SPerBx16hMA", "new title", source="new")
    merged = inventory.merge_rows([new], [old])
    assert len(merged) == 1
    assert merged[0]["Title"] == "new title"
    assert merged[0]["Rule Status"] == "REVIEWED"
    assert merged[0]["Notes"] == "Manual rules"
    assert merged[0]["Strategy Type"] == "CUSTOM"


def test_invalid_video_id_does_not_create_fake_row():
    assert inventory.make_row("not-a-video-id", "MACD strategy") is None
    assert inventory.make_row("SPerBx16hMA", "") is None
