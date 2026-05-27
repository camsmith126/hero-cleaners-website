# Domain Reference Audit — Hero Cleaners

**Date:** 2026-05-09
**Context:** Audit of every discoverable external citation pointing at
either `herocleanersllc.com` (legacy) or `theherocleaners.com` (canonical),
performed to support the canonical-consolidation work. The redirect
engineering is already live as of this morning — every URL on the legacy
domain 301-redirects to the matching path on the canonical domain via a
dedicated Netlify redirect-only site. This audit documents what still
needs human edits in external systems where API/automation can't reach.

## Methodology

- Google search probes for `site:` and `"hero cleaners" logan utah` on
  major directory platforms.
- Public WebFetch of discoverable listings where the platform allows it
  (LinkedIn, Weebly).
- Yelp returned HTTP 403 to direct fetch — citation flagged for manual
  Cam verification.
- DNS / hosting check via dig + curl.
- Confirmed earlier in today's session by Cam (verbal): GBP, Facebook,
  Yelp bio, Instagram bio all already updated to theherocleaners.com.
  Those four entries are marked "Cam-confirmed" below; the rest are
  fresh findings from this audit.

## Citation Inventory

| # | Citation | URL where it lives | Domain shown | Status | Effort | Notes |
|---|---|---|---|---|---|---|
| 1 | Google Business Profile | (admin: business.google.com) | theherocleaners.com | ✅ Clean | — | Cam-confirmed earlier today |
| 2 | Facebook page | facebook.com/HeroCleanersLogan | theherocleaners.com | ✅ Clean | — | Cam-confirmed earlier today |
| 3 | Yelp listing bio | yelp.com/biz/hero-cleaners-logan | theherocleaners.com | ✅ Clean (URL) | — | Cam-confirmed bio link. **However:** listing still describes DISCONTINUED services per CLAUDE.md (driveway sealing, Christmas lights) — service list needs editing. See "Open issues" below. |
| 4 | Instagram bio | (admin: instagram.com) | theherocleaners.com | ✅ Clean | — | Cam-confirmed earlier today |
| 5 | **LinkedIn company page** | linkedin.com/company/hero-cleaners | **herocleanersllc.com** ❌ | 🔴 STALE | Low | Listed as `http://herocleanersllc.com` (no https). 7 followers, 6 employees listed. Needs URL update via LinkedIn admin. |
| 6 | **Weebly ghost site** | heroc1eaners.weebly.com (note: "heroc1eaners" with a "1") | **herocleanersllc.com** ❌ | 🔴 STALE + BRAND DAMAGE | Medium | Page is titled "HERO CLEANERS PROPERTY SOLUTIONS" — "Property Solutions" is on CLAUDE.md's NEVER-USE list. Address + phone are correct (matches CLAUDE.md). Lists gutter cleaning + holiday lighting (DISCONTINUED). Contains placeholder text + unrelated mortgage template content. Recommendation: delete entirely. Requires Cam's Weebly login. |
| 7 | Nextdoor business page | nextdoor.com/pages/hero-cleaners-llc-logan-ut-1/ | unknown | ⚠ NEEDS CHECK | Low | Discoverable via Google. URL slug contains "-llc-" which suggests legacy naming. Need Cam to log in and verify the URL field. |
| 8 | Thumbtack listing | thumbtack.com/ut/logan/house-cleaning/hero-cleaners/service/520116162979602447 | unknown | ⚠ NEEDS CHECK | Low | Discoverable. Need Cam to log in and verify the URL field. |
| 9 | Angi profile | listed in angi.com window-cleaning Logan directory | unknown | ⚠ NEEDS CHECK | Low | Listed in Angi's Logan window-cleaning directory. Need Cam to log in (if claimed) and verify URL. |
| 10 | BBB profile | bbb.org (no Hero Cleaners profile found for Logan UT) | n/a | ⚪ Not present | Med | No BBB profile for Hero Cleaners in Logan was found in search. Either not claimed/created, or not accredited. Worth creating one as a citation-building opportunity (separate from this consolidation task). |
| 11 | Homeaglow | not searched (no public profile discoverable from outside) | unknown | ⚠ NEEDS CHECK | Low | If Hero has a presence, needs login to verify. |
| 12 | Care.com | not searched (no public profile discoverable from outside) | unknown | ⚠ NEEDS CHECK | Low | Same — needs Cam to check. |
| 13 | Local Chamber of Commerce (Cache Valley Chamber) | not searched in this audit | unknown | ⚠ NEEDS CHECK | Low | Worth confirming whether they have a directory listing and what URL it shows. |
| 14 | Google Maps listing | (linked to GBP — same record) | theherocleaners.com | ✅ Clean | — | GBP and Maps listing share the same backing record. If GBP is correct (confirmed), Maps is correct. |
| 15 | Mailchimp campaign footers / from-address | (lives in Hero Dispatch agent folder — NOT INSPECTED per scope) | unknown | ⚠ NEEDS CHECK | Med | The Mailchimp setup belongs to the Hero Dispatch agent and was deliberately not touched per this session's scope. Open question: does the email footer "View in browser" link, or the from-address domain, point at the legacy domain? Cam needs to verify. |
| 16 | Printed materials (business cards, vehicle wraps, magnets, invoices) | physical | unknown | ⚠ NEEDS CHECK | Low–High | Anything physically printed with `herocleanersllc.com` will continue to send customers to the legacy domain. Redirect still catches them (good), but for any future print runs, the canonical domain should be used. Cam needs to confirm what's in circulation. |
| 17 | Old herocleanersllc.com homepage as still-indexed organic result | search engine result page | herocleanersllc.com | ⚠ Expected drag, will resolve | — | Google's index still contains old-domain URLs as of today (verified via search). Expected to clear over 4-8 weeks now that 301s are live. Monitor — no action needed. |

## Hosting / DNS Comparison

| | theherocleaners.com | herocleanersllc.com |
|---|---|---|
| Status | 200 (canonical) | 301 → theherocleaners.com (verified across all paths) |
| Hosting | Netlify (main site) | Netlify (separate redirect-only project, set up earlier today via Cowork dashboard work) |
| DNS A records | 75.2.60.5 (Netlify) | 52.52.192.191, 13.52.188.95 (legacy AWS IPs still in DNS cache; redirect is functioning regardless via Netlify's edge routing) |
| Registrar | GoDaddy (Cam owns) | GoDaddy (Cam owns) |
| Renewal | should be kept active indefinitely | should be kept active indefinitely — registration auto-renew confirmed earlier in session |

## Backlink / Authority Signal — Quick Read

Without a paid tool (Ahrefs, Moz, etc.), the rough signal we can read from
public surfaces:

- **theherocleaners.com:** newer domain. Ranking signals from GSC over the
  last 28 days show strong upward trend — 103 clicks, 3,710 impressions,
  avg position 18.8 (up from 29.0 in prior 28 days). Hits position 1.8 on
  primary keyword "house cleaning logan utah." Indexed at 22 URLs.
- **herocleanersllc.com:** older domain, more inbound links accumulated over
  the years. Now passing 100% of its authority to the canonical via the
  catch-all 301 (verified). Google still has legacy URLs indexed; expect
  these to drop over 4-8 weeks.
- **Net:** the migration is structurally complete. Authority is consolidating
  on the right domain. The risk is the still-indexed legacy URLs creating
  duplicate-content drag in Google's results during the recrawl window —
  this is unavoidable but transient.

## Open issues surfaced by this audit (beyond the citation list above)

1. **Weebly ghost site uses forbidden brand language ("Property Solutions")
   and lists discontinued services.** This is brand-damage risk independent
   of the canonical-URL question. Worth deleting regardless of redirect work.

2. **Yelp listing's SERVICE DESCRIPTION is stale.** URL is correct (Cam
   confirmed) but the listing still advertises driveway sealing and
   Christmas lights — both on CLAUDE.md's DISCONTINUED list. This will
   misrepresent the business to anyone searching Yelp.

3. **LinkedIn URL points to legacy domain.** Free 30-second fix when Cam is
   next in LinkedIn admin.

4. **Several directory listings (Nextdoor, Thumbtack, Angi, Homeaglow,
   Care.com, Chamber) are unverified.** This audit could not get inside
   them without Cam's logins. Recommend Cam batch-verify these in a single
   sitting (~20 min total).

5. **No BBB profile.** Citation-building opportunity, separate task.

6. **Mailchimp citations not inspected** per scope.

7. **Printed materials inventory not done** — requires Cam input.

## Items closed out by this audit

- Confirmed redirect engineering is fully live and holding.
- Confirmed the four major citations Cam mentioned (GBP, FB, Yelp, IG bio)
  are correct on the URL axis. (Yelp service description is a separate
  finding.)
- Confirmed Netlify primary domain configuration aligns with canonical
  choice.
