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

[2026-05-09] — commit 71ffc36 — Blog permalinks fix (7 weeks of
posts unlocked)
Discovered that all auto-generated weekly blog posts from
2026-03-23 through 2026-05-04 were silently 404ing on the live
site. Root cause: scripts/generate_post.py wrote
`permalink: /blog/{slug}/` (trailing slash, no /index.html).
In Eleventy that produces an output file at _site/blog/{slug}
with no extension, so requests to /blog/{slug}/ get 404 because
Netlify can't find _site/blog/{slug}/index.html. The blog index
page kept listing all 9 post URLs because the markdown files
were detected, which masked the problem — every link 404'd.
Fixed (a) generate_post.py line 150 to emit /index.html on new
posts going forward, (b) back-filled the same fix into all 7
broken posts:
  - 2026-03-23-recurring-house-cleaning-vs-one-time-cleaning...
  - 2026-03-30-5-signs-your-logan-home-needs-a-professional-clean...
  - 2026-04-06-how-to-prepare-your-home-before-the-cleaners-arrive
  - 2026-04-13-the-real-cost-of-cleaning-your-own-home-every-week...
  - 2026-04-20-move-out-cleaning-checklist-for-logan-ut-renters...
  - 2026-04-27-is-hiring-a-house-cleaner-a-luxury-the-truth...
  - 2026-05-04-why-biweekly-cleaning-is-the-most-popular-schedule...
Result: all 7 posts verified HTTP 200 on the live site after
deploy. 7 weeks of SEO content that had been written and never
visible is now publicly indexed. Future weekly auto-publishes
will work without intervention.

[2026-05-09] — commits 435c68e, 28de1bc, 24b0d43 — Old-domain
redirect investigation (multi-attempt)
Cam reported old-site inner pages (/about, /window-washing,
/commercial-cleaning, /contact) still serving 200 on
herocleanersllc.com instead of redirecting. Found the catch-all
in netlify.toml was sending everything to / instead of preserving
the path with :splat (commit 435c68e fixed that). After deploy,
catch-all worked for paths that don't exist as static files
(e.g. /some-fake-path, /blog/foo) but DID NOT work for paths
that exist as files in _site/ (/about, /window-washing, etc.) —
Netlify served the static file because force=true does not
override static-file resolution across alias hostnames on the
same project. Also discovered specific old-slug rules
(/about-us -> /about, /services -> /) were returning RELATIVE
Location headers, leaving the user on the old hostname after the
301. Tried switching to conditions={Host=[...]} (commit 28de1bc)
to bypass both behaviors — that approach silently broke ALL
redirects because Host is not a documented Netlify condition
(only Country, Language, Cookie, Role are). Reverted to the
hostname-prefix + :splat form (commit 24b0d43). The complete
fix had to happen at the Netlify dashboard layer, not in
netlify.toml — see next entry.

[2026-05-09] — commit 0aea4d8 — robots.txt + templated sitemap
Audit follow-up: robots.txt was returning 404 and the static
website/sitemap.xml only listed 12 URLs (the 11 main pages +
the /blog index) — none of the 9 individual blog posts.
Fixes:
- Added website/robots.txt (3 lines) with Allow: / and an
  explicit Sitemap: pointer so crawlers find the sitemap on
  first visit instead of guessing.
- Replaced the static sitemap.xml with sitemap.njk at the
  repo root. The new template iterates collections.post in
  reverse-chronological order and emits a <url> entry with
  <lastmod> from each post's date. Sitemap now self-updates
  on every build — every future weekly auto-publish lands
  in the sitemap with zero maintenance.
Verified live: robots.txt 200 with correct content, sitemap
now contains 22 URLs (12 main + 10 blog posts, including
today's Monday auto-publish 76ffdd2 "Commercial Cleaning vs
Residential Cleaning"). Confirms blog automation is end-to-
end healthy post the earlier 71ffc36 permalink fix.

[2026-05-09] — Netlify dashboard — Redirect-only site cutover
Created a separate Netlify site (`hero-cleaners-redirect`) whose
only purpose is to 301-redirect every URL on herocleanersllc.com
and www.herocleanersllc.com to the matching path on
theherocleaners.com. Site has an empty publish dir + a 4-line
netlify.toml with one /* -> https://theherocleaners.com/:splat
catch-all. Removed herocleanersllc.com and www.herocleanersllc.com
as domain aliases on the theherocleaners.com site. Added them as
custom domains on the new redirect-only site. SSL provisioned
automatically. Why: with no static files in _site/ on the
redirect-only site, force=true now correctly overrides nothing
(there's nothing to override) and the cross-project destination
keeps the Location header absolute. Result: verified all
previously-broken URLs now return HTTP/2 301 with absolute
Location to theherocleaners.com:
  /about, /services, /window-washing, /commercial-cleaning,
  /about-us, /some-fake-path, /blog/why-biweekly-... — all
  single-hop 301 to theherocleaners.com/<same-path>.
  www./contact has a benign 2-hop chain (www -> apex -> new
  domain) due to Netlify's auto www-to-apex redirect on the
  redirect-only site; functionally correct, optimization for
  later if desired. Note: the long block of [[redirects]] in
  the main site's netlify.toml that targets herocleanersllc.com
  is now dead code (the old hostname no longer hits this site).
  Worth pruning in a future cleanup commit but not urgent —
  the rules are no-ops, not harmful.
