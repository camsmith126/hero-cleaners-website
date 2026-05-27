# Domain Canonical Recommendation — Hero Cleaners

**Date:** 2026-05-09
**Author:** Website Agent (Claude Code)
**For:** Cam (decision), Conductor (cross-agent propagation), Residential
Research Agent (consume to unblock paid acquisition planning)
**Status:** Engineering already executed earlier today. This document
formalizes the canonical decision and records the evidence.

---

## Recommendation

**Canonical domain: `theherocleaners.com`**

The legacy domain `herocleanersllc.com` is to remain registered and
301-redirect everything to the canonical, indefinitely.

This is not a forward-looking proposal — this is the decision that has
already been implemented as of 2026-05-09. This document exists to make
the decision findable, defensible, and consumable by the Conductor and
other agents (notably the Residential Research Agent, which raised the
flag in its Phase 1 Discovery run).

## Why `theherocleaners.com` (evidence)

| Reason | Detail |
|---|---|
| Aligns with Google Workspace setup | Workspace was provisioned on `theherocleaners.com` per the 2026-05-06 Workspace Migration session log. The email infrastructure already anchors on this domain. |
| Cleaner brand expression | Drops the "LLC" suffix that was a structural artifact of the original registration, not a brand choice. Customers don't search for "Hero Cleaners LLC" — they search for "hero cleaners logan utah." |
| Active build target | All site engineering since the March 2026 launch has been on this domain. The Netlify project, GitHub repo, blog automation, GSC integration, GA4 integration, sitemap, and robots.txt all target this domain. Switching canonical to the legacy domain would require unwinding 2+ months of work. |
| Better ranking trajectory | GSC data over the last 28 days shows clicks +84% (56→103), impressions +119% (1,691→3,710), avg position 29.0→18.8 on this domain. Headline keyword "commercial cleaning logan" jumped from position 14.0 to 7.4 in the last 7 days alone. |
| Already in the citations that matter | GBP, Facebook, Yelp bio, Instagram bio all updated to theherocleaners.com per Cam's confirmation earlier in today's session. The high-traffic citation pages already align with this choice. |

## Why NOT `herocleanersllc.com`

| Counterargument | Why it doesn't win |
|---|---|
| "Older domain → more inherent authority" | Legacy authority is preserved by the 301 redirects pointing at the new domain. Google passes ~100% of PageRank through a 301. We don't lose authority by changing canonical; we *consolidate* it onto the cleaner domain. |
| "Old domain has more indexed pages" | True at moment of snapshot (Phase 1 Discovery flagged this), but the 301s mean those URLs will drop from Google's index over 4-8 weeks. The duplicate-content risk is transient. |
| "We've used herocleanersllc.com in print materials" | The 301 catches anyone who types or scans those. Print runs in circulation are not a reason to choose a worse domain going forward; they're a reason to keep the legacy domain registered so the redirect doesn't break. |

## Redirect Strategy — What Was Implemented

**Approach: page-level 301s with path preservation.**

Every URL on `herocleanersllc.com/*` and `www.herocleanersllc.com/*` 301-redirects to `theherocleaners.com/<same-path>`. The catch-all preserves the path via `:splat`. A handful of legacy slug-renames (e.g. `/about-us` → `/about`, `/Recurring-Clean` → `/recurring-cleaning`) are handled with explicit rules that take precedence over the catch-all.

This is the SEO-best option vs. blanket-to-homepage 301:
- **Page-level preserves topical relevance.** Old `herocleanersllc.com/window-washing` had backlinks and rankings specifically for window-washing intent — those should flow to the matching page, not the homepage.
- **Page-level passes authority more precisely.** Google's signals tied to specific URLs (anchor text, click-through patterns, topical clusters) survive intact.
- The blanket-to-homepage alternative would have dumped all legacy authority on the homepage and lost the per-page topical signal — a real loss.

## Implementation Detail (already done)

A dedicated Netlify redirect-only project was stood up earlier today
specifically to handle the legacy domain. Reason: when both domains
were aliases on the same Netlify site, `force = true` did not override
static-file resolution across alias hostnames, so paths like `/about`
served the new site's content instead of 301'ing. The dedicated
redirect-only project has an empty publish directory, so `force = true`
works correctly and the catch-all fires for every path.

Verified end-to-end via curl earlier today and re-verified at the start
of this audit session: every tested URL on the legacy domain returns
`HTTP/2 301` with `Location: https://theherocleaners.com/<same-path>`.

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Temporary ranking dip during Google's recrawl window | High | Medium (typically 1-3 weeks of jitter on transitional keywords) | Already underway; monitor via the baseline queries in the Consolidation Plan. Nothing to do but wait. |
| Legacy URLs continue appearing in Google's index for several weeks | High (already observed) | Low | Expected behavior. Verified the 301s are correct so Google will process them on next crawl. May take 4-8 weeks to fully clear. |
| Print materials still referencing legacy domain | Medium | Low | Catch-all redirect makes this safe; users still arrive at the right page. For future print runs, use canonical only. |
| Legacy domain registration lapses | Low | **CRITICAL** — would break every 301 immediately | Auto-renew on legacy domain at GoDaddy must be ON. Confirmed earlier in session. |
| Mailchimp or other external systems still send recipients to legacy URLs | Medium | Low | 301 catches it. Worth fixing the source for cleanliness but not urgent. |
| Weebly ghost site competes for branded search traffic and uses forbidden brand language | Medium | Medium (brand consistency, not SEO) | Independent of canonical decision. Recommend deletion. See audit doc. |

## What This Unblocks

The Residential Research Agent's Phase 1 finding cited "confused canonical URL setup" as a blocker for paid acquisition (LSAs + Google Ads). With the engineering complete:

- **Paid acquisition can proceed on theherocleaners.com.** All ad destinations should point at the canonical domain. Any ad creative inheriting the legacy URL from a past campaign should be updated, but no LSAs or Google Ads have actually been launched yet, so this is preventive, not corrective.
- **Future tracking will be clean.** GA4 is wired to the canonical domain only. GSC has the canonical as the verified property. Ad attribution and on-site behavioral tracking will not be split across two domains.

## Specific List of External Citations Still Needing Cam-Side Updates

See `Domain_Reference_Audit.md` for the full table. Summarized priorities here:

**Do soon (15-20 min total):**
1. LinkedIn company page → update URL to https://theherocleaners.com (currently `http://herocleanersllc.com`)
2. Yelp service description → remove driveway sealing + Christmas lights (URL itself is already correct)
3. Delete Weebly ghost site (heroc1eaners.weebly.com) — uses forbidden brand phrase, lists discontinued services
4. Spot-check Nextdoor, Thumbtack, Angi listings (verify URL is canonical)

**Verify but probably already clean:**
5. Mailchimp from-address and footer URLs (lives in Hero Dispatch agent — Cam to verify)
6. Homeaglow, Care.com (only matters if Hero has profiles there)
7. Chamber of Commerce directory listing

**Lower priority but worth knowing:**
8. Any business cards / vehicle wraps / printed invoices showing legacy URL — fine for in-circulation materials, use canonical for new prints
9. Create a BBB profile (separate citation-building task, not consolidation-related)
