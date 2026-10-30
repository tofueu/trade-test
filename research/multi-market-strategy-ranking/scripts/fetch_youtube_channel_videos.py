#!/usr/bin/env python3
"""Fetch REAL public @bh1908 video metadata; never invent video rows or trading rules.

Try yt-dlp (all videos/shorts/streams) when installed, otherwise the official
YouTube Atom feed (recent uploads ONLY). Existing annotations are preserved.
This is metadata discovery, NOT evidence of watched videos or a backtest.
"""
import csv
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INVENTORY_FILE = ROOT / "results" / "bh1908_video_inventory.csv"
STATUS_FILE = ROOT / "results" / "bh1908_inventory_status.json"
CHANNEL_ID = "UCQ9fNvNHNRQkqFgOCPpu5dg"  # Confirmed by public channel metadata; verify feed title.
HANDLE = "@bh1908"
FIELDS = ["Video ID", "Title", "URL", "Published Date", "Strategy Type", "Rule Status", "Notes"]
VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
TABS = ("videos", "shorts", "streams")


def classify(title):
    lower = title.lower()
    for word, kind in (("smc", "SMC"), ("macd", "MACD"), ("rsi", "RSI"),
                       ("布林", "Bollinger"), ("均線", "Moving average"),
                       ("支撐", "Support/resistance"), ("壓力", "Support/resistance"),
                       ("趨勢線", "Trendline"), ("成交量", "Volume")):
        if word in lower:
            return kind
    return "UNCLASSIFIED"


def make_row(video_id, title, published="", source=""):
    if not VIDEO_ID.fullmatch(video_id) or not isinstance(title, str) or not title.strip():
        return None
    return {
        "Video ID": video_id, "Title": title.strip(),
        "URL": "https://www.youtube.com/watch?v=" + video_id,
        "Published Date": published, "Strategy Type": classify(title),
        "Rule Status": "RULES_PENDING",
        "Notes": "Metadata only; video rules not reviewed; source=" + source,
    }


def from_feed(open_url=urllib.request.urlopen):
    """Official Atom feed; covers only recent uploads, not full channel history."""
    url = "https://www.youtube.com/feeds/videos.xml?channel_id=" + CHANNEL_ID
    req = urllib.request.Request(url, headers={"User-Agent": "TradeTestVideoInventory/1.0"})
    with open_url(req, timeout=20) as response:
        data = response.read()
    root = ET.fromstring(data)
    ns = {"a": "http://www.w3.org/2005/Atom",
          "yt": "http://www.youtube.com/xml/schemas/2015"}
    actual_id = root.findtext("yt:channelId", default="", namespaces=ns)
    title = root.findtext("a:title", default="", namespaces=ns)
    if actual_id != CHANNEL_ID or "熊敖" not in title:
        raise ValueError("Official feed channel identity does not match @bh1908")
    rows = []
    for entry in root.findall("a:entry", ns):
        video_id = entry.findtext("yt:videoId", default="", namespaces=ns)
        video_title = entry.findtext("a:title", default="", namespaces=ns)
        published = entry.findtext("a:published", default="", namespaces=ns)
        row = make_row(video_id, video_title, published, "official-atom-recent")
        if row:
            rows.append(row)
    if not rows:
        raise RuntimeError("Official channel feed returned no valid videos")
    return rows, {"mode": "official_atom", "coverage": "PARTIAL_RECENT_ONLY",
                  "tabs_ok": [], "tabs_failed": []}


def from_ytdlp():
    """Enumerate all three public tabs; mark coverage unverified even on success."""
    from yt_dlp import YoutubeDL  # optional dependency, no credentials required
    rows = []
    ok, failed = [], []
    options = {"extract_flat": "in_playlist", "skip_download": True,
               "ignoreerrors": True, "quiet": True, "no_warnings": True}
    with YoutubeDL(options) as ydl:
        for tab in TABS:
            try:
                info = ydl.extract_info("https://www.youtube.com/" + HANDLE + "/" + tab,
                                        download=False)
                entries = info.get("entries", []) if isinstance(info, dict) else []
                tab_rows = []
                for entry in entries:
                    if not isinstance(entry, dict):
                        continue
                    video_id = str(entry.get("id") or "")
                    title = entry.get("title") or ""
                    date = str(entry.get("upload_date") or "")
                    if len(date) == 8 and date.isdigit():
                        date = date[:4] + "-" + date[4:6] + "-" + date[6:]
                    row = make_row(video_id, title, date, "yt-dlp-" + tab)
                    if row:
                        tab_rows.append(row)
                if not tab_rows:
                    raise RuntimeError("No valid entries in " + tab)
                rows.extend(tab_rows)
                ok.append(tab)
            except Exception as exc:
                failed.append({"tab": tab, "error_type": type(exc).__name__})
    if not rows:
        raise RuntimeError("yt-dlp returned no verified video metadata")
    return rows, {"mode": "yt_dlp", "coverage": "UNVERIFIED_COMPLETE" if not failed
                  else "PARTIAL_TABS_FAILED", "tabs_ok": ok, "tabs_failed": failed}


def merge_rows(new_rows, existing_rows):
    by_id = {row["Video ID"]: dict(row) for row in existing_rows
             if VIDEO_ID.fullmatch(row.get("Video ID", ""))}
    for row in new_rows:
        old = by_id.get(row["Video ID"])
        if old:
            # Do not erase manually reviewed rules or notes.
            for key in ("Rule Status", "Notes", "Strategy Type"):
                if old.get(key) and old.get(key) != "RULES_PENDING":
                    row[key] = old[key]
            if old.get("Published Date") and not row["Published Date"]:
                row["Published Date"] = old["Published Date"]
        by_id[row["Video ID"]] = row
    return sorted(by_id.values(), key=lambda r: (r["Published Date"], r["Video ID"]), reverse=True)


def main():
    errors = []
    try:
        rows, status = from_ytdlp()
    except (ImportError, RuntimeError, OSError, ValueError) as exc:
        errors.append("yt-dlp " + type(exc).__name__)
        rows, status = from_feed()
    existing = []
    if INVENTORY_FILE.exists():
        with INVENTORY_FILE.open(newline="", encoding="utf-8") as f:
            existing = list(csv.DictReader(f))
    merged = merge_rows(rows, existing)
    INVENTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with INVENTORY_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(merged)
    status.update({"channel": HANDLE, "channel_id": CHANNEL_ID,
                   "checked_at_utc": datetime.now(timezone.utc).isoformat(),
                   "newly_fetched_count": len({r["Video ID"] for r in rows}),
                   "inventory_total": len(merged),
                   "all_videos_confirmed": False, "backtests_completed": 0,
                   "fallback_reasons": errors})
    STATUS_FILE.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps(status, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("VIDEO_INVENTORY_FETCH_FAILED: " + type(exc).__name__ + ": " + str(exc)[:180],
              file=sys.stderr)
        sys.exit(1)
