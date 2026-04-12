#!/usr/bin/env python3
"""
weekly_report.py — Pull the last 7 days of GSC data and push a fresh weekly
report into the Hero Cleaners Google Sheet dashboard.

Tabs updated on each run:
  README                  — static explainer (refreshed each run, safe to edit)
  Weekly Metrics          — time series of week-ending totals (append)
  Top Queries             — top 10 by clicks (snapshot, refresh)
  Zero-Click Opportunities — queries with impressions but 0 clicks (snapshot)
  Activity Log            — recent git commits to the repo (snapshot)
  Next Up                 — prioritized action items (seeded on first run only)
  Blocked                 — items waiting on manual action from Cam (seeded)

GA4 traffic integration is pending. Requires GA4 Data API enablement on the
hero-cleaners-automation GCP project + service account added to the GA4
property as a Viewer. See the Blocked tab after first run.

Auth: same service account as gsc_report.py. Sheet ID comes from
scripts/gsc_config.json (gitignored) or GSC_SHEET_ID env var.

Run: /usr/bin/python3 scripts/weekly_report.py
"""

import json
import os
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

sys.path.insert(0, str(Path(__file__).parent))
from gsc_report import (
    fetch_queries,
    build_brief,
    resolve_credentials_path,
    resolve_site_url,
    load_config,
)

SCOPES = [
    "https://www.googleapis.com/auth/webmasters.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
]

LOOKBACK_DAYS = 7
REPORT_LAG_DAYS = 3

REPO_ROOT = Path(__file__).parent.parent


def get_sheet_id() -> str:
    env = os.environ.get("GSC_SHEET_ID")
    if env:
        return env
    cfg = load_config()
    sid = cfg.get("sheet_id")
    if not sid:
        raise ValueError(
            "No sheet_id in scripts/gsc_config.json and GSC_SHEET_ID not set"
        )
    return sid


def build_services():
    creds = service_account.Credentials.from_service_account_file(
        str(resolve_credentials_path()), scopes=SCOPES
    )
    gsc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
    sheets = build("sheets", "v4", credentials=creds, cache_discovery=False)
    return gsc, sheets


def git_activity(limit: int = 50) -> list[list[str]]:
    """Return list of [date, shortsha, subject] rows."""
    r = subprocess.run(
        ["git", "log", f"-{limit}", "--pretty=format:%ad|%h|%s", "--date=short"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    rows = []
    for line in r.stdout.strip().split("\n"):
        parts = line.split("|", 2)
        if len(parts) == 3:
            rows.append(parts)
    return rows


def ensure_tabs(sheets, sid: str, required: list[str]) -> None:
    """Create any missing tabs."""
    meta = sheets.spreadsheets().get(spreadsheetId=sid).execute()
    existing = {s["properties"]["title"] for s in meta["sheets"]}
    missing = [t for t in required if t not in existing]
    if missing:
        reqs = [{"addSheet": {"properties": {"title": t}}} for t in missing]
        sheets.spreadsheets().batchUpdate(
            spreadsheetId=sid, body={"requests": reqs}
        ).execute()
    # Delete the default "Sheet1" if it exists and isn't in our required set.
    if "Sheet1" in existing and "Sheet1" not in required:
        meta2 = sheets.spreadsheets().get(spreadsheetId=sid).execute()
        for s in meta2["sheets"]:
            if s["properties"]["title"] == "Sheet1":
                try:
                    sheets.spreadsheets().batchUpdate(
                        spreadsheetId=sid,
                        body={"requests": [{"deleteSheet": {"sheetId": s["properties"]["sheetId"]}}]},
                    ).execute()
                except HttpError:
                    pass  # can't delete the last sheet; safe to ignore
                break


def tab_has_data(sheets, sid: str, tab: str) -> bool:
    resp = (
        sheets.spreadsheets()
        .values()
        .get(spreadsheetId=sid, range=f"{tab}!A1:A1")
        .execute()
    )
    return bool(resp.get("values"))


def write_tab(sheets, sid: str, tab: str, values: list[list]) -> None:
    """Clear the tab and write values from A1."""
    sheets.spreadsheets().values().clear(
        spreadsheetId=sid, range=f"{tab}!A:Z"
    ).execute()
    sheets.spreadsheets().values().update(
        spreadsheetId=sid,
        range=f"{tab}!A1",
        valueInputOption="USER_ENTERED",
        body={"values": values},
    ).execute()


def append_row(sheets, sid: str, tab: str, row: list) -> None:
    sheets.spreadsheets().values().append(
        spreadsheetId=sid,
        range=f"{tab}!A:Z",
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body={"values": [row]},
    ).execute()


def weighted_avg_position(queries: list[dict]) -> float:
    total_impr = sum(q["impressions"] for q in queries)
    if not total_impr:
        return 0.0
    weighted = sum(q["position"] * q["impressions"] for q in queries)
    return round(weighted / total_impr, 2)


def main():
    sid = get_sheet_id()
    gsc, sheets = build_services()

    required_tabs = [
        "README",
        "Weekly Metrics",
        "Top Queries",
        "Zero-Click Opportunities",
        "Activity Log",
        "Next Up",
        "Blocked",
    ]
    print(f"Sheet ID: {sid}")
    print("Ensuring tabs exist...")
    ensure_tabs(sheets, sid, required_tabs)

    print(f"Pulling GSC data ({LOOKBACK_DAYS}-day window)...")
    end = date.today() - timedelta(days=REPORT_LAG_DAYS)
    start = end - timedelta(days=LOOKBACK_DAYS - 1)
    rows = fetch_queries(gsc, start.isoformat(), end.isoformat())
    brief = build_brief(rows, start.isoformat(), end.isoformat())

    totals = brief["totals"]
    top = brief["top_10_by_clicks"]
    zero = brief["zero_click_opportunities"]
    all_queries_for_pos = top + zero
    avg_pos = weighted_avg_position(all_queries_for_pos) if all_queries_for_pos else 0.0

    # --- README ---
    readme = [
        ["Hero Cleaners — Weekly Report Dashboard"],
        [""],
        ["This sheet is auto-populated by scripts/weekly_report.py."],
        ["Data source: Google Search Console. GA4 integration pending."],
        [""],
        ["TABS:"],
        ["  Weekly Metrics — append-only time series. One row per run."],
        ["  Top Queries — current top 10 queries by clicks. Refreshed each run."],
        ["  Zero-Click Opportunities — ranked but not clicking. Refreshed each run."],
        ["  Activity Log — recent git commits to theherocleaners.com."],
        ["  Next Up — prioritized action items (editable by hand)."],
        ["  Blocked — items waiting on manual action from Cam."],
        [""],
        ["To refresh the Sheet:"],
        ["  /usr/bin/python3 scripts/weekly_report.py"],
        [""],
        [f"Last refreshed: {date.today().isoformat()}"],
        [f"Data window: {start.isoformat()} to {end.isoformat()}"],
        [""],
        ["NEXT STEP: Build a Looker Studio dashboard on top of this sheet + GA4 + GSC."],
        ["Looker Studio: https://lookerstudio.google.com/"],
    ]
    write_tab(sheets, sid, "README", readme)

    # --- Weekly Metrics (append row) ---
    metrics_header = [
        [
            "week_ending",
            "clicks",
            "impressions",
            "ctr_pct",
            "avg_position",
            "unique_queries",
            "notes",
        ]
    ]
    if not tab_has_data(sheets, sid, "Weekly Metrics"):
        write_tab(sheets, sid, "Weekly Metrics", metrics_header)
    append_row(
        sheets,
        sid,
        "Weekly Metrics",
        [
            end.isoformat(),
            totals["clicks"],
            totals["impressions"],
            totals["ctr_pct"],
            avg_pos,
            totals["queries"],
            "auto",
        ],
    )

    # --- Top Queries ---
    tq = [["rank", "query", "clicks", "impressions", "ctr_pct", "position"]]
    for i, r in enumerate(top, 1):
        tq.append(
            [
                i,
                r["query"],
                r["clicks"],
                r["impressions"],
                r["ctr_pct"],
                r["position"],
            ]
        )
    write_tab(sheets, sid, "Top Queries", tq)

    # --- Zero-Click Opportunities ---
    zc = [["rank", "query", "impressions", "position"]]
    for i, r in enumerate(zero, 1):
        zc.append([i, r["query"], r["impressions"], r["position"]])
    write_tab(sheets, sid, "Zero-Click Opportunities", zc)

    # --- Activity Log ---
    al = [["date", "commit", "subject"]]
    al.extend(git_activity(50))
    write_tab(sheets, sid, "Activity Log", al)

    # --- Next Up (only seed on first run) ---
    if not tab_has_data(sheets, sid, "Next Up"):
        next_up = [
            ["priority", "item", "status", "notes"],
            ["HIGH", "Build Looker Studio dashboard on top of GA4 + GSC + this Sheet", "open", "~15 min drag-and-drop once GA4 is connected"],
            ["HIGH", "Enable GA4 Data API + add service account to GA4 property", "blocked on Cam", "Unlocks traffic data in this report"],
            ["MED", "Before/After differentiator page", "blocked on photos", "Biggest Clean Freak differentiator"],
            ["MED", "Monitor rankings of new maid-service page (2-3 week check)", "open", "Baseline pos 14.5, 0 clicks"],
            ["MED", "Monitor commercial-cleaning ranking change post-refresh", "open", "Baseline pos 22.4"],
            ["MED", "Monitor window-washing ranking change post-refresh", "open", "Baseline pos 16.8"],
            ["LOW", "Track impact of logo migration on Lighthouse / Core Web Vitals", "open", "9 pages dropped from 680KB to ~30KB"],
        ]
        write_tab(sheets, sid, "Next Up", next_up)

    # --- Blocked (only seed on first run) ---
    if not tab_has_data(sheets, sid, "Blocked"):
        blocked = [
            ["item", "waiting_on", "since"],
            ["Update Google Business Profile URL to theherocleaners.com", "Cam", "2026-04-11"],
            ["Update Facebook bio link to theherocleaners.com", "Cam", "2026-04-11"],
            ["Update Yelp profile URL to theherocleaners.com", "Cam", "2026-04-11"],
            ["Update Instagram bio link to theherocleaners.com", "Cam", "2026-04-11"],
            ["Provide before/after photos for differentiator page", "Cam", "2026-04-11"],
            ["Enable GA4 Data API and share GA4 property with service account", "Cam", "2026-04-12"],
        ]
        write_tab(sheets, sid, "Blocked", blocked)

    print()
    print(f"Sheet URL: https://docs.google.com/spreadsheets/d/{sid}/edit")
    print(
        f"Data window: {start} to {end}  "
        f"| clicks: {totals['clicks']}  "
        f"| impressions: {totals['impressions']}  "
        f"| CTR: {totals['ctr_pct']}%  "
        f"| unique queries: {totals['queries']}"
    )


if __name__ == "__main__":
    main()
