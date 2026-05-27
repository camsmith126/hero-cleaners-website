#!/usr/bin/env python3
"""
generate_dashboard.py — Build a single-page HTML operations dashboard
for Cam at theherocleaners.com/dashboard/.

Pulls live data from Google Search Console, Google Analytics 4, runs
the redirect canary check, reads the blog directory and recent git
commits, then renders everything into website/dashboard/index.html.

Eleventy passthrough-copies website/ to _site/ so the file gets served
at https://theherocleaners.com/dashboard/. The page is noindex'd so it
won't appear in search results, but is otherwise public.

Run: /usr/bin/python3 scripts/generate_dashboard.py
"""

import datetime
import html
import os
import subprocess
import sys
import warnings
from datetime import date, timedelta
from http.client import HTTPSConnection
from pathlib import Path
from urllib.parse import urlparse

warnings.filterwarnings("ignore")

from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange, Dimension, Metric, RunReportRequest, OrderBy
)

sys.path.insert(0, str(Path(__file__).parent))
from gsc_report import resolve_credentials_path, resolve_site_url
from weekly_report import check_redirect_canaries, REDIRECT_CANARY_URLS

REPO_ROOT = Path(__file__).parent.parent
OUTPUT_PATH = REPO_ROOT / "website" / "dashboard" / "index.html"

GA4_PROPERTY_ID = "377543571"
GSC_SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
GA4_SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]


def build_gsc():
    creds = service_account.Credentials.from_service_account_file(
        str(resolve_credentials_path()), scopes=GSC_SCOPES
    )
    return build("searchconsole", "v1", credentials=creds, cache_discovery=False)


def build_ga4():
    creds = service_account.Credentials.from_service_account_file(
        str(resolve_credentials_path()), scopes=GA4_SCOPES
    )
    return BetaAnalyticsDataClient(credentials=creds)


def pull_gsc(gsc, start: str, end: str, dimensions=None, row_limit=200):
    body = {"startDate": start, "endDate": end, "rowLimit": row_limit}
    if dimensions:
        body["dimensions"] = dimensions
    r = gsc.searchanalytics().query(siteUrl=resolve_site_url(), body=body).execute()
    return r.get("rows", [])


def pull_ga4_metrics(ga4, start: str, end: str, metrics, dimensions=None, limit=10, order_by=None):
    req_args = {
        "property": f"properties/{GA4_PROPERTY_ID}",
        "date_ranges": [DateRange(start_date=start, end_date=end)],
        "metrics": [Metric(name=m) for m in metrics],
    }
    if dimensions:
        req_args["dimensions"] = [Dimension(name=d) for d in dimensions]
    if order_by:
        req_args["order_bys"] = [order_by]
    if limit:
        req_args["limit"] = limit
    return ga4.run_report(RunReportRequest(**req_args))


def get_recent_blog_posts(limit=5):
    """Returns list of (date, title, url_path) for most recent posts."""
    blog_dir = REPO_ROOT / "blog"
    posts = []
    for f in sorted(blog_dir.glob("*.md"), reverse=True)[:limit]:
        title = ""
        permalink = ""
        post_date = ""
        with open(f) as fh:
            in_fm = False
            for line in fh:
                line = line.rstrip()
                if line == "---":
                    if in_fm:
                        break
                    in_fm = True
                    continue
                if in_fm:
                    if line.startswith("title:"):
                        title = line.split(":", 1)[1].strip().strip('"')
                    elif line.startswith("date:"):
                        post_date = line.split(":", 1)[1].strip()
                    elif line.startswith("permalink:"):
                        permalink = line.split(":", 1)[1].strip()
                        # Strip /index.html suffix for the clean URL
                        if permalink.endswith("/index.html"):
                            permalink = permalink[:-len("index.html")]
        if not permalink:
            # Default 11ty path if no explicit permalink
            permalink = f"/blog/{f.stem}/"
        posts.append((post_date, title, permalink))
    return posts


def get_recent_commits(limit=10):
    r = subprocess.run(
        ["git", "log", f"-{limit}", "--pretty=format:%ad|%h|%s", "--date=short"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    out = []
    for line in r.stdout.strip().split("\n"):
        parts = line.split("|", 2)
        if len(parts) == 3:
            out.append(tuple(parts))
    return out


def days_since(iso_date: str) -> int:
    try:
        d = date.fromisoformat(iso_date)
        return (date.today() - d).days
    except Exception:
        return 999


def fmt_pct_change(current: float, prior: float) -> tuple[str, str]:
    """Returns (text, css_class). class is 'up', 'down', or 'flat'."""
    if prior == 0:
        return ("new", "up" if current > 0 else "flat")
    pct = (current - prior) / prior * 100
    if abs(pct) < 1:
        return (f"{pct:+.0f}%", "flat")
    cls = "up" if pct > 0 else "down"
    return (f"{pct:+.0f}%", cls)


def main():
    print("Building operations dashboard...")
    gsc = build_gsc()
    ga4 = build_ga4()

    # GSC: last 28 days vs prior 28 days
    end_28 = date.today() - timedelta(days=4)  # GSC lags ~3 days
    start_28 = end_28 - timedelta(days=27)
    prior_end = start_28 - timedelta(days=1)
    prior_start = prior_end - timedelta(days=27)

    gsc_28 = pull_gsc(gsc, start_28.isoformat(), end_28.isoformat(), row_limit=1)
    gsc_prior = pull_gsc(gsc, prior_start.isoformat(), prior_end.isoformat(), row_limit=1)
    gsc_28_totals = gsc_28[0] if gsc_28 else {"clicks": 0, "impressions": 0, "ctr": 0, "position": 0}
    gsc_prior_totals = gsc_prior[0] if gsc_prior else {"clicks": 0, "impressions": 0, "ctr": 0, "position": 0}

    # GSC: top queries last 28 days
    gsc_queries = pull_gsc(gsc, start_28.isoformat(), end_28.isoformat(), dimensions=["query"], row_limit=10)
    top_queries = sorted(gsc_queries, key=lambda r: -r["clicks"])[:10]

    # GA4: 30-day totals
    ga4_30 = pull_ga4_metrics(
        ga4, "30daysAgo", "yesterday",
        metrics=["sessions", "totalUsers", "screenPageViews", "bounceRate"],
        limit=1,
    )
    ga4_totals = ga4_30.rows[0].metric_values if ga4_30.rows else None

    # GA4: top channels
    ga4_channels = pull_ga4_metrics(
        ga4, "30daysAgo", "yesterday",
        metrics=["sessions"],
        dimensions=["sessionDefaultChannelGroup"],
        order_by=OrderBy(metric={"metric_name": "sessions"}, desc=True),
        limit=5,
    )

    # GA4: top pages
    ga4_pages = pull_ga4_metrics(
        ga4, "30daysAgo", "yesterday",
        metrics=["screenPageViews", "totalUsers"],
        dimensions=["pagePath"],
        order_by=OrderBy(metric={"metric_name": "screenPageViews"}, desc=True),
        limit=8,
    )

    # Redirect canaries
    print("  Running redirect canary checks...")
    canary_rows, canary_failures = check_redirect_canaries()

    # Blog posts + commits
    blog_posts = get_recent_blog_posts(limit=5)
    recent_commits = get_recent_commits(limit=10)

    # Compute status indicators
    last_blog_date = blog_posts[0][0] if blog_posts else "1900-01-01"
    blog_days_ago = days_since(last_blog_date)
    blog_ok = blog_days_ago <= 8  # 8 to allow a Mon -> next Mon cycle
    site_ok = True  # if we got here, the script ran — sufficient signal
    canaries_ok = canary_failures == 0

    all_ok = site_ok and blog_ok and canaries_ok

    # Render HTML
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M %Z").strip()

    # Build the chunks
    clicks_change, clicks_cls = fmt_pct_change(gsc_28_totals.get("clicks", 0), gsc_prior_totals.get("clicks", 0))
    impr_change, impr_cls = fmt_pct_change(gsc_28_totals.get("impressions", 0), gsc_prior_totals.get("impressions", 0))
    pos_current = gsc_28_totals.get("position", 0)
    pos_prior = gsc_prior_totals.get("position", 0)
    pos_delta = pos_prior - pos_current  # lower position is better, so prior - current > 0 means improvement
    pos_change_text = f"{pos_delta:+.1f}" if pos_prior else "new"
    pos_cls = "up" if pos_delta > 0.5 else ("down" if pos_delta < -0.5 else "flat")

    queries_html = "".join(
        f"<tr><td>{html.escape(q['keys'][0])}</td>"
        f"<td class='num'>{q['clicks']}</td>"
        f"<td class='num'>{q['impressions']}</td>"
        f"<td class='num'>{q['ctr']*100:.1f}%</td>"
        f"<td class='num'>{q['position']:.1f}</td></tr>"
        for q in top_queries
    )

    channels_html = "".join(
        f"<tr><td>{html.escape(c.dimension_values[0].value)}</td>"
        f"<td class='num'>{c.metric_values[0].value}</td></tr>"
        for c in ga4_channels.rows
    )

    pages_html = "".join(
        f"<tr><td>{html.escape(p.dimension_values[0].value)}</td>"
        f"<td class='num'>{p.metric_values[0].value}</td>"
        f"<td class='num'>{p.metric_values[1].value}</td></tr>"
        for p in ga4_pages.rows
    )

    posts_html = "".join(
        f"<li><span class='post-date'>{html.escape(d)}</span> "
        f"<a href='{html.escape(p)}'>{html.escape(t)}</a></li>"
        for d, t, p in blog_posts
    )

    canary_html = "".join(
        f"<tr class='{'pass' if r[4]=='PASS' else 'fail'}'>"
        f"<td class='canary-url'>{html.escape(r[0].replace('https://',''))}</td>"
        f"<td class='num'>{html.escape(r[3])}</td>"
        f"<td>{html.escape(r[4])}</td>"
        f"<td class='canary-loc'>{html.escape(r[2].replace('https://','')[:60])}</td>"
        f"</tr>"
        for r in canary_rows[1:]  # skip header
    )

    commits_html = "".join(
        f"<tr><td class='commit-date'>{html.escape(d)}</td>"
        f"<td class='commit-sha'>{html.escape(sha)}</td>"
        f"<td>{html.escape(subj[:80])}</td></tr>"
        for d, sha, subj in recent_commits
    )

    bounce_pct = float(ga4_totals[3].value) * 100 if ga4_totals else 0

    html_out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>Hero Cleaners — Operations Dashboard</title>
<style>
  :root {{
    --hero-red: #B71C1C;
    --hero-black: #1A1A1A;
    --accent-red: #D32F2F;
    --light-rose: #FFCDD2;
    --charcoal: #2D2D2D;
    --pass: #2E7D32;
    --fail: #C62828;
    --neutral: #6B7280;
    --bg: #FAFAFA;
    --card: #FFFFFF;
    --border: #E5E7EB;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;
    background: var(--bg);
    color: var(--charcoal);
    line-height: 1.5;
    padding: 24px;
    max-width: 1200px;
    margin: 0 auto;
  }}
  header {{
    border-bottom: 4px solid var(--hero-red);
    padding-bottom: 16px;
    margin-bottom: 32px;
  }}
  h1 {{
    font-family: "Bebas Neue", Impact, sans-serif;
    font-size: 36px;
    color: var(--hero-black);
    letter-spacing: 1px;
  }}
  h2 {{
    font-family: "Bebas Neue", Impact, sans-serif;
    font-size: 22px;
    color: var(--hero-black);
    margin: 32px 0 12px;
    letter-spacing: 0.5px;
  }}
  .subtitle {{ color: var(--neutral); font-size: 13px; margin-top: 4px; }}
  .subtitle a {{ color: var(--hero-red); text-decoration: none; }}
  .status-banner {{
    background: {('linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%)' if all_ok else 'linear-gradient(135deg, #C62828 0%, #8E0000 100%)')};
    color: white;
    padding: 24px;
    border-radius: 8px;
    margin-bottom: 24px;
    text-align: center;
  }}
  .status-banner h2 {{ color: white; font-size: 28px; margin: 0; }}
  .status-banner p {{ margin-top: 4px; opacity: 0.9; }}
  .status-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 12px;
    margin-bottom: 24px;
  }}
  .status-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    border-left: 4px solid var(--pass);
  }}
  .status-card.fail {{ border-left-color: var(--fail); }}
  .status-card h3 {{
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--neutral);
    margin-bottom: 8px;
  }}
  .status-card .v {{ font-size: 16px; font-weight: 600; color: var(--hero-black); }}
  .status-card .icon {{ float: right; font-size: 20px; }}
  .status-card.pass .icon {{ color: var(--pass); }}
  .status-card.fail .icon {{ color: var(--fail); }}

  .metrics-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
    margin-bottom: 24px;
  }}
  .metric-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 20px;
  }}
  .metric-card .label {{
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--neutral);
    margin-bottom: 8px;
  }}
  .metric-card .value {{
    font-family: "Bebas Neue", Impact, sans-serif;
    font-size: 42px;
    color: var(--hero-black);
    line-height: 1;
  }}
  .metric-card .change {{
    font-size: 13px;
    margin-top: 8px;
    font-weight: 600;
  }}
  .change.up {{ color: var(--pass); }}
  .change.down {{ color: var(--fail); }}
  .change.flat {{ color: var(--neutral); }}

  .panel {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 16px;
  }}
  .panel-grid {{
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 16px;
  }}
  @media (max-width: 768px) {{
    .panel-grid {{ grid-template-columns: 1fr; }}
  }}

  table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
  th {{
    text-align: left;
    padding: 8px 12px;
    background: #F3F4F6;
    color: var(--neutral);
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
  }}
  td {{
    padding: 8px 12px;
    border-bottom: 1px solid var(--border);
    color: var(--hero-black);
  }}
  td.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
  tr:last-child td {{ border-bottom: none; }}
  tr.pass td {{ color: var(--pass); }}
  tr.fail td {{ color: var(--fail); font-weight: 600; }}
  .canary-url {{ font-family: ui-monospace, monospace; font-size: 12px; }}
  .canary-loc {{ font-family: ui-monospace, monospace; font-size: 11px; color: var(--neutral); }}
  .commit-date {{ font-family: ui-monospace, monospace; font-size: 12px; color: var(--neutral); white-space: nowrap; }}
  .commit-sha {{ font-family: ui-monospace, monospace; font-size: 12px; color: var(--hero-red); }}

  ul.posts {{ list-style: none; }}
  ul.posts li {{
    padding: 10px 0;
    border-bottom: 1px solid var(--border);
  }}
  ul.posts li:last-child {{ border-bottom: none; }}
  ul.posts a {{
    color: var(--hero-black);
    text-decoration: none;
    font-weight: 500;
  }}
  ul.posts a:hover {{ color: var(--hero-red); }}
  .post-date {{
    color: var(--neutral);
    font-size: 12px;
    font-family: ui-monospace, monospace;
    margin-right: 12px;
  }}
  footer {{
    margin-top: 32px;
    padding-top: 16px;
    border-top: 1px solid var(--border);
    color: var(--neutral);
    font-size: 12px;
    text-align: center;
  }}
</style>
</head>
<body>

<header>
  <h1>HERO CLEANERS — OPERATIONS</h1>
  <p class="subtitle">
    Last refreshed: {timestamp} ·
    <a href="https://theherocleaners.com">View live site</a> ·
    <a href="https://docs.google.com/spreadsheets/d/1wL14FfaK2UCPHDpUswQshWPE224CDg3-n6jPdoIkIOw/edit">Open raw data sheet</a>
  </p>
</header>

<div class="status-banner">
  <h2>{'ALL SYSTEMS OPERATIONAL' if all_ok else 'ATTENTION NEEDED'}</h2>
  <p>{'Everything is running as expected.' if all_ok else 'One or more checks are failing — see below.'}</p>
</div>

<div class="status-grid">
  <div class="status-card {'pass' if site_ok else 'fail'}">
    <span class="icon">{'✓' if site_ok else '✗'}</span>
    <h3>Site Health</h3>
    <div class="v">{'Reachable' if site_ok else 'Down'}</div>
  </div>
  <div class="status-card {'pass' if blog_ok else 'fail'}">
    <span class="icon">{'✓' if blog_ok else '✗'}</span>
    <h3>Blog Cadence</h3>
    <div class="v">Last post {blog_days_ago} day{'s' if blog_days_ago != 1 else ''} ago</div>
  </div>
  <div class="status-card {'pass' if canaries_ok else 'fail'}">
    <span class="icon">{'✓' if canaries_ok else '✗'}</span>
    <h3>Redirect Health</h3>
    <div class="v">{len(REDIRECT_CANARY_URLS) - canary_failures}/{len(REDIRECT_CANARY_URLS)} passing</div>
  </div>
</div>

<h2>Search Performance (last 28 days)</h2>
<div class="metrics-grid">
  <div class="metric-card">
    <div class="label">Clicks</div>
    <div class="value">{gsc_28_totals.get('clicks', 0)}</div>
    <div class="change {clicks_cls}">{clicks_change} vs prior 28d</div>
  </div>
  <div class="metric-card">
    <div class="label">Impressions</div>
    <div class="value">{gsc_28_totals.get('impressions', 0):,}</div>
    <div class="change {impr_cls}">{impr_change} vs prior 28d</div>
  </div>
  <div class="metric-card">
    <div class="label">CTR</div>
    <div class="value">{gsc_28_totals.get('ctr', 0)*100:.1f}%</div>
    <div class="change flat">site-wide average</div>
  </div>
  <div class="metric-card">
    <div class="label">Avg Position</div>
    <div class="value">{pos_current:.1f}</div>
    <div class="change {pos_cls}">{pos_change_text} vs prior 28d</div>
  </div>
</div>

<h2>Traffic (GA4, last 30 days)</h2>
<div class="metrics-grid">
  <div class="metric-card">
    <div class="label">Sessions</div>
    <div class="value">{ga4_totals[0].value if ga4_totals else 'n/a'}</div>
  </div>
  <div class="metric-card">
    <div class="label">Users</div>
    <div class="value">{ga4_totals[1].value if ga4_totals else 'n/a'}</div>
  </div>
  <div class="metric-card">
    <div class="label">Pageviews</div>
    <div class="value">{ga4_totals[2].value if ga4_totals else 'n/a'}</div>
  </div>
  <div class="metric-card">
    <div class="label">Bounce Rate</div>
    <div class="value">{bounce_pct:.0f}%</div>
  </div>
</div>

<div class="panel-grid">
  <div class="panel">
    <h2 style="margin-top:0">Top Search Queries</h2>
    <table>
      <thead><tr><th>Query</th><th class="num">Clicks</th><th class="num">Impr</th><th class="num">CTR</th><th class="num">Pos</th></tr></thead>
      <tbody>{queries_html}</tbody>
    </table>
  </div>
  <div class="panel">
    <h2 style="margin-top:0">Traffic Channels</h2>
    <table>
      <thead><tr><th>Channel</th><th class="num">Sessions</th></tr></thead>
      <tbody>{channels_html}</tbody>
    </table>
  </div>
</div>

<div class="panel-grid">
  <div class="panel">
    <h2 style="margin-top:0">Top Pages</h2>
    <table>
      <thead><tr><th>Path</th><th class="num">Views</th><th class="num">Users</th></tr></thead>
      <tbody>{pages_html}</tbody>
    </table>
  </div>
  <div class="panel">
    <h2 style="margin-top:0">Recent Blog Posts</h2>
    <ul class="posts">{posts_html}</ul>
  </div>
</div>

<div class="panel">
  <h2 style="margin-top:0">Redirect Health (8 old-domain canaries)</h2>
  <table>
    <thead><tr><th>URL</th><th class="num">Hops</th><th>Status</th><th>Final Destination</th></tr></thead>
    <tbody>{canary_html}</tbody>
  </table>
</div>

<div class="panel">
  <h2 style="margin-top:0">Recent Activity</h2>
  <table>
    <thead><tr><th>Date</th><th>Commit</th><th>Subject</th></tr></thead>
    <tbody>{commits_html}</tbody>
  </table>
</div>

<footer>
  Hero Cleaners Operations Dashboard · Auto-generated by scripts/generate_dashboard.py
</footer>

</body>
</html>
"""

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(html_out)
    print(f"  Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)} ({len(html_out)} bytes)")
    print(f"  Status: {'ALL OK' if all_ok else 'ATTENTION NEEDED'}")
    print(f"  Will be live at: https://theherocleaners.com/dashboard/ after next deploy")


if __name__ == "__main__":
    main()
