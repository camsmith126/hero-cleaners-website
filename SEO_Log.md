# SEO Log — Hero Cleaners
## Running history of SEO activity. Append only — never delete entries.

---

### Format
[Date] — [What checked] — [What found] — [What done]

---

[April 2026] — Initial GSC audit
- 53 clicks, 1,610 impressions, 3.3% CTR, avg position 29.2
- All 10 main pages indexed correctly
- 4 noindex pages confirmed intentional (city SEO pages)
- Key finding: ranking well for brand + primary keywords
- Key problem: showing up for carpet cleaning, pressure washing
  (services we don't offer) dragging average position down
- Key opportunities: commercial cleaning (pos 22), maid service (pos 14),
  office cleaning (pos 26), window cleaning (pos 16)
- No action taken yet — baseline established

[2026-04-11] — GA4 install + live-site bug sweep
- Installed GA4 measurement ID G-8RKK7PMPJ0 on all 9 main pages
  (index, about, contact, recurring-cleaning, deep-clean,
  commercial-cleaning, window-washing, reviews, service-areas).
- Discovered 4 pages had a broken HCP booking script tag:
  close-nav-on-outside-click handler was stuffed inside a
  <script async src="..."> tag, which browsers ignore when src is
  set. Affected commercial-cleaning, window-washing, recurring-cleaning,
  deep-clean. Fixed by self-closing the script tag and moving the
  handler into the existing bottom <script> block where nl is defined.
  Outside-click-to-close nav is now working on all pages.
- Discovered commercial-cleaning.html was publishing exact hourly
  rates ($60/$55/$50) on the pricing card, violating CLAUDE.md.
  Replaced with scoped "we quote before work begins" language.
- Fixed typo on commercial-cleaning.html line 199.
- Commits: 00118b5 (GA4), f9f27a6 (bug sweep).

[2026-04-11] — HIGH-priority Opportunities.md shipped
- NEW page: /maid-service targeting "maid service logan utah"
  (GSC pos 14.5 baseline, 0 clicks, no dedicated page previously).
  Added to sitemap at priority 0.9. Linked from Services dropdown
  nav + footer on all 10 main pages.
- commercial-cleaning.html refreshed: new title/meta/OG/schema/H1/hero
  targeting "commercial cleaning logan" + "office cleaning logan"
  (GSC pos 22.4 baseline). Added "Office Cleaning in Logan & Cache
  Valley" section with 8-item checklist + "Businesses We Serve"
  6-card section.
- window-washing.html refreshed: new title/meta/OG/schema/H1/hero
  targeting "window cleaning logan utah" (GSC pos 16.8 baseline).
  Title now leads with "window cleaning" (higher volume than
  "window washing"). Added residential/commercial two-card section
  + Cache Valley city grid. Removed misleading "gutter cleaning"
  from schema.org description (not actually offered).
- Commit: f791d5a.

[2026-04-12] — SEO follow-ups
- Added GA4 (G-8RKK7PMPJ0) to /faq (was missing from original push
  because FAQ isn't in CLAUDE.md "9 main pages" list, but it's
  linked from nav and gets traffic).
- Added internal link to /maid-service from homepage service
  quick-links card and from recurring-cleaning hero intro copy —
  internal links help Google discover and weight the new page.
- NEW section on /deep-clean: "Move-Out Cleaning in Logan, Utah"
  targeting "move out cleaning logan" (GSC pos 27.7 baseline, 6
  impressions). Full two-col section with move-in/move-out checklist
  and dedicated CTA.
- Flagged but NOT changed: recurring-cleaning.html publishes exact
  rates ($60/hr, $119/visit, etc) on the plan cards — same CLAUDE.md
  violation as commercial page, but structural change (conversion-
  critical plan cards) — waiting for Cam's explicit call.
- Pending Cam-side manual items (can't be automated):
  - Submit sitemap to Search Console
  - Update Google Business Profile URL
  - Update Facebook/Yelp/Instagram bio links
  - Provide before/after photos for differentiator page
