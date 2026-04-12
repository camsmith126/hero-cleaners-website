# Changes Log — Hero Cleaners Website
## Every deployment logged here. Append only — never delete entries.

---

### Format
[Date] — [What changed] — [Why] — [Result]

---

[April 2026] — Initial log created. No changes yet.

[2026-04-11] — commit 00118b5 — GA4 install on 9 main pages
Added Google Analytics 4 (G-8RKK7PMPJ0) to the top of <head> on
index, about, contact, recurring-cleaning, deep-clean, commercial-
cleaning, window-washing, reviews, service-areas. Why: start
measuring traffic, conversions, and campaign performance. Result:
verified live on all 9 pages, HTTP 200, DOCTYPE intact.

[2026-04-11] — commit f9f27a6 — Live-site bug sweep
Fixed (a) exact hourly rates published on commercial-cleaning
pricing card (CLAUDE.md violation), (b) typo on line 199
"licensed, insured, and licensed and insured" -> "licensed,
insured, and background-checked", (c) broken HCP script tag on
commercial-cleaning, window-washing, recurring-cleaning,
deep-clean where close-nav JS was stuffed inside a script[src]
tag and silently ignored by browsers. Outside-click-to-close nav
was dead on those 4 pages — now restored. Why: hygiene + compliance
+ UX regression fix. Result: verified live on all 4 pages, close-
nav handler present in bottom script block, HTTP 200 across all
main pages.

[2026-04-11] — commit f791d5a — Maid Service launch + SEO refresh
NEW page /maid-service (new HTML file with full template, nav,
footer, HCP scripts, schema.org, OG tags, GA4). Added to sitemap
priority 0.9. Added "Maid Service" link to Services dropdown nav
+ footer Services list on all 10 main pages. Refreshed
commercial-cleaning.html with new title/meta/OG/H1/hero targeting
"commercial cleaning logan" + "office cleaning logan", added
Office Cleaning section + Businesses We Serve 6-card section.
Refreshed window-washing.html with new title/meta/OG/H1/hero
targeting "window cleaning logan utah" (title now leads with the
higher-volume "window cleaning" variant), added residential/
commercial two-card section + Cache Valley city grid, removed
misleading "gutter cleaning" from schema. Why: three HIGH-priority
Opportunities.md items. Result: verified live — all 11 main pages
return HTTP 200, maid-service page serves fully rendered, nav
link visible on all 10 main pages.

[2026-04-12] — SEO follow-ups (current commit)
Added GA4 to /faq (was missing). Added internal link to
/maid-service from homepage service quick-links card and from
recurring-cleaning hero intro. Added new "Move-Out Cleaning in
Logan" section to /deep-clean targeting "move out cleaning logan"
(GSC pos 27.7 baseline). Appended entries to SEO_Log.md. Why:
internal links boost discovery of the new maid-service page,
deep-clean move-out section captures a high-intent keyword with
zero effort beyond copy. Flagged (not fixed): recurring-cleaning
also publishes exact rates on plan cards — structural change,
needs Cam approval before touching.
