#!/usr/bin/env python3
"""
gsc_report.py — Weekly Google Search Console brief for theherocleaners.com.

Pulls the last 28 days of query-level performance data from GSC, identifies
top-performing keywords and zero-click opportunities, and returns a structured
dict ready to push to Google Sheets.

Auth: service account credentials.json. The service account must be added as
a GSC user on the property (already done:
hero-cleaners-sheets@hero-cleaners-automation.iam.gserviceaccount.com has
Full access to theherocleaners.com).

Configuration (first match wins):
  1. Environment variables: GSC_CREDENTIALS, GSC_SITE_URL
  2. scripts/gsc_config.json next to this file
  3. Hardcoded fallbacks

Run:   python3 scripts/gsc_report.py
Import: from scripts.gsc_report import run; brief = run()
"""

import json
import os
from datetime import date, timedelta
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
LOOKBACK_DAYS = 28
# GSC data lags ~2-3 days; end the window there for complete rows.
REPORT_LAG_DAYS = 3

CONFIG_PATH = Path(__file__).parent / "gsc_config.json"
DEFAULT_CREDENTIALS = "~/Desktop/HCP Automation/credentials.json"
DEFAULT_SITE_URL = "https://theherocleaners.com/"


def load_config() -> dict:
    if CONFIG_PATH.is_file():
        with CONFIG_PATH.open() as f:
            return json.load(f)
    return {}


def resolve_credentials_path() -> Path:
    env_path = os.environ.get("GSC_CREDENTIALS")
    if env_path:
        return Path(env_path).expanduser()
    cfg = load_config()
    return Path(cfg.get("credentials_path", DEFAULT_CREDENTIALS)).expanduser()


def resolve_site_url() -> str:
    env_url = os.environ.get("GSC_SITE_URL")
    if env_url:
        return env_url
    cfg = load_config()
    return cfg.get("site_url", DEFAULT_SITE_URL)


def build_service():
    creds_path = resolve_credentials_path()
    if not creds_path.is_file():
        raise FileNotFoundError(
            f"credentials.json not found at {creds_path}. "
            "Set GSC_CREDENTIALS to override."
        )
    creds = service_account.Credentials.from_service_account_file(
        str(creds_path), scopes=SCOPES
    )
    return build("searchconsole", "v1", credentials=creds, cache_discovery=False)


def fetch_queries(service, start: str, end: str) -> list[dict]:
    """Paginate all query rows for the window."""
    rows: list[dict] = []
    start_row = 0
    batch = 5000
    while True:
        resp = (
            service.searchanalytics()
            .query(
                siteUrl=resolve_site_url(),
                body={
                    "startDate": start,
                    "endDate": end,
                    "dimensions": ["query"],
                    "rowLimit": batch,
                    "startRow": start_row,
                },
            )
            .execute()
        )
        page = resp.get("rows", [])
        rows.extend(page)
        if len(page) < batch:
            break
        start_row += batch
    return rows


def normalize(rows: list[dict]) -> list[dict]:
    out = []
    for r in rows:
        out.append(
            {
                "query": r["keys"][0],
                "clicks": int(r.get("clicks", 0)),
                "impressions": int(r.get("impressions", 0)),
                "ctr_pct": round(r.get("ctr", 0.0) * 100, 2),
                "position": round(r.get("position", 0.0), 1),
            }
        )
    return out


def build_brief(rows: list[dict], start: str, end: str) -> dict:
    normalized = normalize(rows)
    total_clicks = sum(r["clicks"] for r in normalized)
    total_impr = sum(r["impressions"] for r in normalized)
    totals = {
        "clicks": total_clicks,
        "impressions": total_impr,
        "queries": len(normalized),
        "ctr_pct": round((total_clicks / total_impr * 100) if total_impr else 0.0, 2),
    }
    top_10 = sorted(
        normalized, key=lambda x: (-x["clicks"], -x["impressions"])
    )[:10]
    zero_click = sorted(
        [r for r in normalized if r["clicks"] == 0 and r["impressions"] > 0],
        key=lambda x: -x["impressions"],
    )
    return {
        "site": resolve_site_url(),
        "generated_at": date.today().isoformat(),
        "date_range": {"start": start, "end": end, "days": LOOKBACK_DAYS},
        "totals": totals,
        "top_10_by_clicks": top_10,
        "zero_click_opportunities": zero_click[:25],
        "zero_click_total_count": len(zero_click),
    }


def format_brief(brief: dict) -> str:
    lines = []
    lines.append("=" * 78)
    lines.append(f"GSC WEEKLY BRIEF — {brief['site']}")
    dr = brief["date_range"]
    lines.append(f"Range: {dr['start']} to {dr['end']} ({dr['days']} days)")
    lines.append(f"Generated: {brief['generated_at']}")
    lines.append("=" * 78)
    t = brief["totals"]
    lines.append("")
    lines.append(
        f"TOTALS: {t['clicks']:,} clicks · {t['impressions']:,} impressions "
        f"· {t['ctr_pct']}% CTR · {t['queries']:,} unique queries"
    )
    lines.append("")
    lines.append("TOP 10 KEYWORDS BY CLICKS")
    lines.append(f"  {'#':<3}{'Query':<46}{'Clicks':>8}{'Impr':>8}{'CTR%':>8}{'Pos':>6}")
    lines.append(f"  {'-'*3}{'-'*46}{'-'*8}{'-'*8}{'-'*8}{'-'*6}")
    for i, r in enumerate(brief["top_10_by_clicks"], 1):
        q = (r["query"][:43] + "...") if len(r["query"]) > 43 else r["query"]
        lines.append(
            f"  {i:<3}{q:<46}{r['clicks']:>8}{r['impressions']:>8}"
            f"{r['ctr_pct']:>8}{r['position']:>6}"
        )
    lines.append("")
    z = brief["zero_click_opportunities"]
    lines.append(
        f"ZERO-CLICK OPPORTUNITIES — queries with impressions but 0 clicks "
        f"(showing top 25 of {brief['zero_click_total_count']})"
    )
    lines.append(f"  {'#':<3}{'Query':<55}{'Impr':>8}{'Pos':>6}")
    lines.append(f"  {'-'*3}{'-'*55}{'-'*8}{'-'*6}")
    for i, r in enumerate(z, 1):
        q = (r["query"][:52] + "...") if len(r["query"]) > 52 else r["query"]
        lines.append(f"  {i:<3}{q:<55}{r['impressions']:>8}{r['position']:>6}")
    lines.append("")
    lines.append("=" * 78)
    return "\n".join(lines)


def run() -> dict:
    """Entry point — returns the brief dict ready for Sheets push."""
    end = date.today() - timedelta(days=REPORT_LAG_DAYS)
    start = end - timedelta(days=LOOKBACK_DAYS - 1)
    service = build_service()
    rows = fetch_queries(service, start.isoformat(), end.isoformat())
    return build_brief(rows, start.isoformat(), end.isoformat())


def main():
    brief = run()
    print(format_brief(brief))
    print()
    print("--- STRUCTURED BRIEF (JSON — ready for Sheets push) ---")
    print(json.dumps(brief, indent=2, default=str))


if __name__ == "__main__":
    main()
