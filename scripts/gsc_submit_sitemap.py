#!/usr/bin/env python3
"""
gsc_submit_sitemap.py — Submit a sitemap to Google Search Console and list
all sitemaps the property currently knows about.

Auth and config share the same setup as gsc_report.py — service account at
~/Desktop/HCP Automation/credentials.json, site URL from scripts/gsc_config.json
or GSC_SITE_URL env var. The only difference is this script needs the read/write
scope (webmasters) instead of readonly.

Run:   /usr/bin/python3 scripts/gsc_submit_sitemap.py
       /usr/bin/python3 scripts/gsc_submit_sitemap.py --list
       /usr/bin/python3 scripts/gsc_submit_sitemap.py --submit https://theherocleaners.com/sitemap.xml
"""

import argparse
import json
import os
import sys
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/webmasters"]  # read/write

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


def list_sitemaps(service, site_url: str) -> list[dict]:
    resp = service.sitemaps().list(siteUrl=site_url).execute()
    return resp.get("sitemap", [])


def submit_sitemap(service, site_url: str, sitemap_url: str) -> None:
    service.sitemaps().submit(siteUrl=site_url, feedpath=sitemap_url).execute()


def format_sitemap_row(s: dict) -> str:
    path = s.get("path", "?")
    last_submitted = s.get("lastSubmitted", "never")
    last_downloaded = s.get("lastDownloaded", "never")
    is_pending = s.get("isPending", False)
    errors = s.get("errors", 0)
    warnings = s.get("warnings", 0)
    status = "pending" if is_pending else "processed"
    return (
        f"  {path}\n"
        f"    status: {status} | errors: {errors} | warnings: {warnings}\n"
        f"    last submitted: {last_submitted}\n"
        f"    last downloaded: {last_downloaded}"
    )


def main():
    parser = argparse.ArgumentParser(description="Submit/list GSC sitemaps")
    parser.add_argument(
        "--submit",
        metavar="URL",
        help="Sitemap URL to submit (default: <site_url>/sitemap.xml)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Only list current sitemaps, don't submit",
    )
    args = parser.parse_args()

    site_url = resolve_site_url()
    default_sitemap = site_url.rstrip("/") + "/sitemap.xml"
    sitemap_to_submit = args.submit or default_sitemap

    service = build_service()

    print(f"Property: {site_url}")
    print()

    if args.list:
        print("Current sitemaps in Search Console:")
        sitemaps = list_sitemaps(service, site_url)
        if not sitemaps:
            print("  (none)")
        else:
            for s in sitemaps:
                print(format_sitemap_row(s))
        return

    # Default path: submit, then list to confirm
    print(f"Submitting: {sitemap_to_submit}")
    try:
        submit_sitemap(service, site_url, sitemap_to_submit)
        print("  SUCCESS (submit call returned 200)")
    except HttpError as e:
        print(f"  FAILED: {e}")
        print()
        print(
            "If this is a 403 'does not match with the site url', the issue "
            "is the siteUrl format — GSC expects the property exactly as it's "
            "registered. Try setting GSC_SITE_URL to the sc-domain form "
            "('sc-domain:theherocleaners.com') or the exact URL prefix."
        )
        sys.exit(1)

    print()
    print("Current sitemaps in Search Console:")
    for s in list_sitemaps(service, site_url):
        print(format_sitemap_row(s))


if __name__ == "__main__":
    main()
