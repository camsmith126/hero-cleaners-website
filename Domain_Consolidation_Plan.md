# Domain Consolidation Plan — Hero Cleaners

**Date:** 2026-05-09
**Status:** Re-cast as a VERIFICATION + MONITORING plan. The original
brief framed this as a pre-execution plan, but execution actually
happened earlier today in this session. The Phase 2 work is now
verification, monitoring, and cleaning up the long tail of external
citations.

---

## Phase 0 (already done today)

For reference, here's what was shipped this session:

- **Redirect-only Netlify site stood up** to handle legacy domain. Empty
  publish dir + 4-line netlify.toml with `/* → https://theherocleaners.com/:splat 301!`
- **Custom domain aliases moved** from the main theherocleaners.com site
  to the new redirect-only site (`herocleanersllc.com` and `www.herocleanersllc.com`).
- **SSL provisioned** automatically by Netlify on the new site.
- **End-to-end verified** via curl: all paths on the legacy domain
  return 301 with absolute Location to the canonical domain.
- **robots.txt added** to canonical site.
- **Sitemap.xml converted** to auto-generating template that includes
  all blog posts.

Source-of-truth commit ledger for today's work is in the section at the
bottom of `AGENT_LOG.md` dated 2026-05-09.

---

## Phase 1 — External Citation Cleanup (Cam-driven, ~30-45 min)

These are the only steps that still require human action. Most are
single-field URL updates in admin dashboards. Group them into a single
sitting:

### 1.1 LinkedIn (5 min)
- Log into LinkedIn as company admin for "Hero Cleaners"
- Edit Page → Page Info → Website URL
- Change from `http://herocleanersllc.com` to `https://theherocleaners.com`
- Save

### 1.2 Yelp listing service description (5-10 min)
- Log into Yelp for Business
- Find "Hero Cleaners — Logan, UT"
- Edit Services / Business Information
- Remove from descriptions: driveway sealing, Christmas light installation,
  gutter cleaning, pressure washing (all on CLAUDE.md DISCONTINUED list)
- URL field already correct — no change needed there
- Save

### 1.3 Weebly ghost site deletion (5-15 min)
- Log into Weebly (if Cam still has credentials)
- Find site `heroc1eaners.weebly.com`
- Either: delete the site entirely (recommended), OR redirect Weebly's
  domain settings to canonical
- If credentials are lost: contact Weebly support to claim/delete the
  site, or worst case ignore (it's a low-traffic free Weebly subdomain
  that Google probably treats as low-authority)

### 1.4 Spot-check the unverified directory listings (10 min)
For each, log in and confirm the website URL field shows
`https://theherocleaners.com`:
- Nextdoor business page
- Thumbtack listing
- Angi profile
- Homeaglow (if Hero has a profile)
- Care.com (if Hero has a profile)
- Cache Valley Chamber of Commerce directory

### 1.5 Mailchimp verification (5 min — coordinate with Hero Dispatch agent)
- Check that campaigns use a from-address on the canonical domain
- Check that the "View in browser" footer link points at the canonical
- This audit deliberately did not touch the Hero Dispatch folder; route
  this through the Conductor or open a session in that agent

### 1.6 Printed materials inventory (Cam-only — 5 min)
- List anything currently in circulation that prints `herocleanersllc.com`
  (business cards, vehicle magnets/wraps, invoices, signage)
- For each: 301 catches all hits, so no action needed on in-circulation
  materials. Just note for next reprint that the canonical domain should
  be used.

---

## Phase 2 — Verification (Agent-driven, automated where possible)

### 2.1 Confirm redirects still holding (weekly check)

Curl the 8 high-value old-domain URLs and confirm all return 301 with
absolute Location to theherocleaners.com. Already verified today; worth
re-running weekly until Google fully drops the legacy URLs from index.

Test set:
```
https://herocleanersllc.com/about
https://herocleanersllc.com/services
https://www.herocleanersllc.com/contact
https://herocleanersllc.com/window-washing
https://herocleanersllc.com/commercial-cleaning
https://herocleanersllc.com/about-us
https://herocleanersllc.com/some-page-that-never-existed
https://herocleanersllc.com/blog/why-biweekly-cleaning-is-the-most-popular-schedule-for-busy-families-in-logan/
```

Pass criteria: every response is `HTTP/2 301` with `Location:
https://theherocleaners.com/<same-path>`.

### 2.2 Confirm legacy domain renewal is still set to auto-renew

The single most catastrophic failure mode is the legacy domain
registration lapsing — that would break every 301 immediately. Confirm
GoDaddy auto-renewal is ON for both domains. This is a quarterly
spot-check, not a weekly one.

---

## Phase 3 — SEO Monitoring (the actual SEO work)

The redirect engineering is done. Now we watch Google process it.

### 3.1 Pre-redirect snapshot (this is the baseline)

Today's GSC + GA4 numbers ARE the baseline because the redirects went
live today. Captured in `SEO_Log.md` entry dated 2026-05-09 plus the
real-time GSC data accessible via `scripts/gsc_report.py`.

Key baseline numbers as of 2026-05-09:
- Total clicks (last 28 days): 103
- Total impressions (last 28 days): 3,710
- Avg position (last 28 days): 18.8
- CTR: 2.78%

### 3.2 Baseline ranking set — 12 queries to monitor

Pulled from observed GSC data for theherocleaners.com over the last 28
days. These are the queries to track week-over-week to confirm the
canonical consolidation produces ranking lift (or at minimum no
regression) over the next 4-8 weeks:

| Query | Current position | Type |
|---|---|---|
| hero cleaners | 2.8 | branded |
| hero cleaners logan utah | 1.1 | branded |
| house cleaning logan utah | 1.8 | primary |
| cleaners logan utah | 3.3 | primary |
| cleaning services logan utah | 3.1 | primary |
| cleaning services near me | 2.2 | primary (variable by searcher location) |
| house cleaners logan utah | 2.3 | residential variant |
| commercial cleaning logan | 7.4 | commercial — biggest opportunity |
| commercial cleaning services in logan | 21.5 | commercial variant |
| maid service logan utah | 14.5 (April baseline) | maid-service page |
| window cleaning logan utah | 16.8 | window vertical |
| move out cleaning logan | 27.7 | deep-clean page section |

Cadence: pull these via `scripts/gsc_report.py` weekly for the next 4-8
weeks. Expect (a) the branded and primary terms to hold or improve,
(b) the commercial cluster to continue climbing (already moving from
14.0 to 7.4), and (c) some transitional jitter on a subset of queries
as Google re-evaluates which domain to attribute signals to.

### 3.3 Deindexing watch

Run `site:herocleanersllc.com` on Google approximately weekly. The
count of indexed URLs should trend down to zero over 4-8 weeks. If it
plateaus above zero past week 8, dig into which specific URLs are still
indexed and why (most likely: backlinks from external sites that
haven't been re-crawled).

### 3.4 Backstop monitoring — GSC

Add the legacy domain `herocleanersllc.com` as a separate property in
Google Search Console (if not already done). This lets us see in GSC's
own data:
- How many impressions the legacy domain is still getting
- The "Crawled - currently not indexed" report for legacy URLs
- The "Indexed, though blocked by robots.txt" or "Page with redirect"
  classifications on the legacy domain

This data lives in Cam's Google account. If service account
`hero-cleaners-sheets@hero-cleaners-automation.iam.gserviceaccount.com`
is added as a Restricted user on the legacy-domain GSC property, the
GSC scripts can pull both properties' data programmatically.

---

## Phase 4 — Close-out criteria

Domain consolidation is officially "done" when ALL of the following
are true:

- [ ] All Phase 1 citation updates complete (LinkedIn, Yelp services,
      Weebly deleted, directory spot-checks, Mailchimp verified)
- [ ] Phase 2 redirect verification passes for 4 consecutive weeks
- [ ] `site:herocleanersllc.com` Google query returns zero results, OR
      has plateaued at a low number for 2+ weeks
- [ ] Baseline ranking set shows no net regression vs 2026-05-09 baseline
      (some individual queries may wobble — net position should hold or
      improve)
- [ ] Both Cam and the Residential Research Agent have confirmation that
      paid acquisition can proceed without canonical-confusion risk

When all five are checked, post a "closed" entry in AGENT_LOG.md, flag
to Conductor, and the Residential Research Agent's blocker is officially
cleared.

---

## What this plan does NOT cover

- Creating a BBB profile (citation-building, separate task)
- Launching LSAs or Google Ads (downstream of this work, not part of it)
- Resolving Yelp service-description staleness (called out here but it's
  a brand-consistency fix, not a canonical-URL fix)
- Long-term backlink building on the canonical domain (ongoing SEO work,
  separate stream)
