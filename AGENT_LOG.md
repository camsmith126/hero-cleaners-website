# Website Agent Log

This log is read by the Conductor (the coordination layer for the Hero Cleaners agent ecosystem) at the start of every session. Keep entries terse, decision-focused, and current.

## Purpose

This log is how this agent stays connected to the rest of the Hero Cleaners ecosystem. The Conductor reads it to understand what's happened here, what decisions have been made, what's been learned, and what other agents should know.

## What to log

- **Decisions made** during a session ("decided X over Y because Z")
- **Work completed** that meaningfully changes the state of this agent or its outputs
- **Insights or learnings** — patterns noticed, problems solved, gotchas discovered
- **Signals for other agents** — things that affect the website, marketing, brand work, etc.
- **Open questions** waiting on Cam
- **Things that broke** and how they were resolved (or not)

## What NOT to log

- Routine commands or trivial edits
- Detailed technical traces (those belong in git commits)
- Repetition of what's already in CLAUDE.md or other docs
- Long paragraphs — keep it bullets

## Format

Most recent entries at the top. Each session adds a dated entry. If you have multiple sessions on the same day, append to that day's entry.

```
## YYYY-MM-DD
- Decision: [what was decided and brief why]
- Completed: [what shipped or got done]
- Learned: [insight or signal worth preserving]
- For Conductor: [anything cross-cutting other agents should know]
- Open: [pending question for Cam]
```

Sections can be omitted if empty for a given session. Keep entries short. Future-Cam and the Conductor will thank you.

---

## Entries

## 2026-06-08 (latest) — Cam review pass: F1/F3 rewording + full Brand Vault icon rollout + keyword H2 weave (commit 3e3da5e)

- Decision (F3 trust-bar): Cam ruled the canonical phrase "we fix it before we go" reads odd without its conditional setup; the trust-bar context truncated it. Replaced trust-bar item with "Background-Checked Team" + bullet_check icon. CTA trust row keeps "If it's not right, we fix it" (conditional intact) and FAQ keeps the full sentence — both read fine.
- Decision (F1 headline): Cam reworded "WE DON'T DO IT ALL. WE DO ONE THING EXCELLENTLY." to "WE CLEAN HOMES. AND WE'RE REALLY GOOD AT IT." (two-line device, whole second line wrapped in <em> red per VisualSystemSpec §3 headline-device convention).
- Decision (F1 subhead): Cam — "we don't need to stress the fact that we dropped all these other services to focus on one thing. people don't care." Dropped the turning-point/jack-of-all-trades framing. New subhead leads with what we actually do ("7,800+ homes across Cache Valley since 2019") and lands the canonical anchor "People pay for a clean. They stay for the people" verbatim. Page Brief Body-layer anchor preserved; the why-we-focused frame removed.
- Completed: full Brand Vault icon rollout on the homepage. Copied 9 new canonical icons from `Brand Vault/assets/icons/svg/{variant}/` into `website/assets/icons/`, picking variant by background per assets/README §"Which variant on which background":
  - Trust bar (red bg, mono_white): trust_insured, trust_scheduling, bullet_check, trust_local.
  - Hero card service quick-links (white bg, onlight): service_recurring, service_maid, service_deepclean, service_window.
  - Services grid cards (white bg, onlight): service_recurring, service_deepclean, service_window.
  - CTA trust row (red bg, mono_white): bullet_check, trust_wecall, trust_makeitright (already in place), trust_local.
  - 15 canonical icon references in index.html, 10 unique SVG files; all serve 200 on the Deploy Preview.
- Completed (SEO): secondary-keyword H2 weave on the services grid section header: "SERVICES BUILT FOR REAL LIFE" -> "HOUSE CLEANING SERVICES BUILT FOR REAL LIFE." Per Page Brief structural-layer secondary keyword list ("cleaning services logan ut", "residential cleaning logan utah" etc.). Title/meta/H1 unchanged — head term still anchors the structural layer there.
- Verification: clean build (48 files, 0 errors), single H1, DOCTYPE intact, 0 retired hex, 10 canonical icons in build output, all serve 200 on preview, F1 anchor + new trust-bar phrase + new H2 wording all present on the rendered preview.
- For Conductor:
  - **Brand-canon F3 phrasing readability**: the canonical phrase fails the short-context comprehension test (trust bar). Works fine when the conditional is intact (CTA trust row, FAQ). Worth a Brand Vault revisit on whether the homepage trust-bar truncation pattern should drive a phrase rework, or whether the rule is just "always carry the conditional."
  - **No `trust_background_check` icon in the arsenal** — used `bullet_check_mono_white.svg` as the closest semantic fit. Possible addition to the arsenal next time the Brand Foundation Project ships icons.
  - **F2 site-wide still pending** (recurring-cleaning, maid-service, service-areas). Out of scope here.
  - **Commercial cleaning footprint still on the homepage** — quick-link + service card both untouched here; both removed by Phase B.1 PR #2.
- Open: Cam reviews the updated Deploy Preview on PR #3.

## 2026-06-08 (later) — Brand Vault verify + canonical icon swap + F1 anchor

- Completed: ran the verification + finish-up loop the prior session could not. Read the four canonical docs the sandbox could not reach (page-briefs/homepage.md, WebsiteStrategicBrief_v1.md §0/§2/§3/§4, BrandFoundation_v1.md §1/§5/§6/§8, Hero_VisualSystemSpec_v1.md + assets/README.md). Continued on branch `homepage-f1-f4-layering`; pushed commit cbb051c on top of the prior session's ad6d47b + 02d5cb3.
- Verified against canon:
  - **Layering Rule** — H1 plain head term + brand device demoted to `<p>` + descriptive logo alt: all correct vs Page Brief §"H1 direction" + brief §0 Worked example. No change.
  - **F1 headline** — "WE DO ONE THING EXCELLENTLY" is on-canon per v1.1 §8. **F1 subhead refined** to land the canonical anchor phrase "People pay for a clean. They stay for the people" (v1.1 §2) per Page Brief Body-layer §"Headline angle" — the prior subhead had the right angle but did not land the canonical line.
  - **F3 copy** — "We Fix It Before We Go" / "if it's not right, we fix it" in all three sites (trust bar, CTA trust row, FAQ). On-canon vs brief §2 F3.
  - **F3 icon** — **swapped the stand-in circle-check SVG for the canonical `trust_makeitright_mono_white.svg`** in both red-background sites (trust bar + CTA trust row). Variant choice per assets/README §"Which variant on which background" (red CTA blocks → mono_white). Asset copied from Brand Vault → `website/assets/icons/`; Vault stays read-only.
  - **F4 colors** — 0 retired hex remain (verified across all 13 pages). No change needed.
  - **F2** — confirmed not applicable on the homepage. Only "same cleaner" reference is FAQ answer using honest §5 phrasing.
- Verification: clean Eleventy build (48 files, 0 errors), `/assets/icons/trust_makeitright_mono_white.svg` ships, single H1, DOCTYPE intact. Deploy Preview re-built and smoke-tested live at deploy-preview-3 URL: F1 anchor present, both icon references resolve, asset serves 200.
- For Conductor:
  - **F2 site-wide cleanup pending** — three pages still carry the "Same Cleaner Every Visit" absolute (recurring-cleaning.html, maid-service.html, service-areas.html). Out of scope for the homepage PR; future Page Brief loops on those pages should land it.
  - **Commercial cleaning still visible on the homepage** at the time of this PR (og:description, service quick-link, COMMERCIAL CLEANING service card, footer Services list). This is the Phase B.1 PR's job (#2 on `phase-b1-remove-commercial`). Both PRs touch the homepage; whichever merges second will need a quick reconcile.
- Open: Cam reviews the updated Deploy Preview on PR #3, approves merge.

## 2026-06-08 — Homepage brand-fix execution (first Page Brief loop run)

- Completed: first end-to-end run of the Page Brief production loop, executed against `../../Residential Research Agent/page-briefs/homepage.md`. Branch `homepage-f1-f4-layering`, commit ad6d47b. Draft-first: committed, NOT pushed — awaiting Cam to push + approve the Netlify preview before merge.
- F1: reframed "Hero Difference" headline breadth->depth ("we do one thing excellently"). F3: generic "satisfaction guaranteed" -> "if something isn't right, we fix it before we go" (trust bar, CTA row, FAQ). F4: retired-hex swap across ALL 13 pages -> locked VisualSystemSpec values.
- Decision (Layering Rule markup resolution): the homepage H1 was the brand device "WE CLEAN. YOU RELAX." — a body-layer line in a structural slot. Resolved by making the H1 the plain head term "House Cleaning in Logan, Utah" and demoting the brand line to `<p class="hero-brand-device">` (visually identical, body layer). Chose minimal-disruption preservation of the hero visual over a layout restructure.
- Decision (F2): the live homepage trust bar carried NO "Same Cleaner Every Visit" absolute; the service card already reads "Same trusted team every visit" and the FAQ already uses the conditioned §5 phrasing. No change made — per brief §2 "don't over-correct good pages."
- Decision (F4 scope): there is NO shared stylesheet — every page has its own inline `<style>`, contrary to the brief's "single stylesheet swap" assumption. Per Cam, ran the swap mechanically across all 13 `website/*.html` (exact-hex, color-only). Verified 0 retired hex remain, DOCTYPE intact, clean Eleventy build.
- For Conductor / cross-agent:
  - **Brand Vault + Residential Research Agent folders were NOT connected this session** — only the three agent folders are. Executed from canon embedded in CLAUDE.md + the session brief; could not read the Page Brief / BrandFoundation / VisualSystemSpec verbatim, and could not use the canonical `trust_makeitright` arsenal icon. Used an on-pattern circle-check inline SVG as a stand-in. **Follow-up: swap in the canonical `trust_makeitright` asset once Brand Vault is connected.**
  - **Commercial cleaning is still visible on the homepage** (nav dropdown, a service card, footer links, OG + LocalBusiness schema "commercial services") — out of scope here but contradicts residential-first / commercial-off-website (Phase B.1). Flagging for the dedicated commercial-removal session.
  - **Retired hex was site-wide** (B71C1C x54, D32F2F x79, 1A1A1A x29, rgb 183,28,28 x101 across 13 files) — all fixed on this branch. New pages must start from the locked values.
- Open for Cam:
  - **Push the branch** (sandbox has no GitHub creds): `git push -u origin homepage-f1-f4-layering` -> Netlify generates the Deploy Preview. Review, then merge if good.
  - **Stale git locks**: sandbox left 0-byte `.git/index.lock`, `.git/HEAD.lock`, `.git/objects/maintenance.lock` it couldn't delete. They don't block `push`, but clear them before any local checkout/merge: `rm -f .git/index.lock .git/HEAD.lock .git/objects/maintenance.lock`.
  - Confirm the F1 headline + the new plain H1 read right to you.

## 2026-06-02 (latest) — Visual Arsenal + VisualSystemSpec v1.1 propagated

- Completed: VisualSystemSpec is now at **v1.1** in the Vault — adds **Slate Gray `#5B6B7A`** as a locked structural-support color (alongside Hero Red `#D92429`, Hero Black `#171E26`, white). Slate is for organize/recede contexts (secondary buttons, dividers, footers, muted badges), never for emphasis (red owns emphasis).
- Completed: Production-ready **Visual Arsenal** wired into Brand & Strategy Sources as a new section 2a. `Brand Vault/assets/README.md` is the authoritative day-to-day usage guide; this CLAUDE.md routes there rather than restating.
- Asset inventory: 15 standardized icons × 4 color variants (`onlight` / `ondark` / `mono_white` / `slate`), SVG + PNG. Covers 6 service icons, 5 trust-bar icons, 4 bullet/feature icons. **This set replaces the current ad-hoc service-grid icons** per WebsiteStrategicBrief.
- Specific pairing locked: **`trust_makeitright` icon ↔ "if something isn't right, we fix it before we go" line.** This is the F3 fix (homepage trust bar's generic "satisfaction guaranteed" → specific operational guarantee + the matching icon). The homepage Page Brief (`Residential Research Agent/page-briefs/homepage.md`) already specs the F3 copy; the icon is what completes it visually.
- Variant rules for the dark hero and red CTA blocks: `ondark` (white + red) on dark/navy hero grounds; `mono_white` (all white) on red CTA blocks and over photos. Don't recolor on the fly — the correctly-colored asset already exists.
- INTERIM web-use logos available in `assets/logos/` (Hero Icon in black/white/slate + full-color lockup). **Full-color lockup works on LIGHT backgrounds only — disappears on red/navy.** Do not use it on dark grounds or for print. Gaps still needing a designer: reversed white lockup, true vector masters, one-color lockups, favicon set. Do not improvise these.
- For Conductor: no conflicts in this CLAUDE.md with the new arsenal — additive only. The inline color block was already removed in the 2026-06-02 (earlier) pointer-pattern propagation, so there's no hardcoded hex to swap here. The live-site CSS color rollout remains a separate Phase B work item (still pending).
- Open: when executing the homepage Page Brief, the F3 fix should use the `trust_makeitright` icon in whichever variant matches the homepage trust bar's background (likely `onlight` if the bar is on light ground, or `ondark` if it sits inside the dark hero strip).

## 2026-06-02 (later) — Strategic Brief landed + Layering Rule lifted as canon

- Completed: `Residential Research Agent/WebsiteStrategicBrief_v1.md` landed (shipped from the Brand Foundation Project). Brand-aware strategic brief that sits between brand canon and per-page execution. Per-page verdicts (KEEP/FIX/ADD/REMOVE), F1–F5 site-wide brand fixes, the brand-vs-SEO layering rule, build-order sequence.
- Completed: **The Layering Rule** lifted from the strategic brief §0 into this CLAUDE.md as a permanent canonical governing rule. Lives in a new top-level section. Rule: "Keywords live in the structural layer (URL, title, meta, H1, headers, alt, schema). Brand voice lives in the body (subheads, paragraphs, CTAs, testimonials, FAQ answers)." Quote it and apply it to every page, forever.
- Completed: Brand & Strategy Sources section expanded — added WebsiteStrategicBrief, `Residential Research Agent/page-briefs/` (per-page execution specs the Research Agent will produce), and a conflict-resolution rule (brief wins on brand framing; RecommendationsPacket wins on research/keyword specifics).
- For Conductor: Page Briefs are now this agent's required input for any page-level work. When picking up a session, the agent should check whether the page has a Page Brief in `Residential Research Agent/page-briefs/`. If not, stop and ask Cam to schedule a Research Agent session to produce one — don't freelance.
- For Conductor: per WebsiteStrategicBrief §3, the homepage chip list (currently 12 cities) needs reconciling against the real city-page set once the Phase B city pages ship. Cam confirmed 2026-06-02 that Preston ID, Brigham City, and Mendon are all served — city-page set unblocked.
- For Conductor: Brand fixes F1–F5 from §2 of the brief are the first sequenced work item (low-risk, no dependencies). When the first Website Agent execution session runs, these are the obvious starting point. F1 specifically is the "we're great at all of them" homepage headline that brags about breadth — directly off-strategy per v1.1 §8 ("we do one thing excellently"). High priority.
- Open: WebsiteStrategicBrief §4 flags the cleaner interviews + consent as the critical-path unblock for Meet Your Team page + photography rollout. Everything else can proceed without them.
- Open: WebsiteStrategicBrief §6 calls for re-reading Phase B items written pre-v1.1 against the brief where they conflict. Most relevant: Phase B.8 (pricing) is now sanctioned-as-public per the brief, not "pre-frame no rates" as Phase B.8 originally framed. Worth a one-line note added to Phase B.8 the next time the RecommendationsPacket gets touched.

## 2026-06-02 — v1.1 + VisualSystemSpec propagation + pricing policy reversal

- Completed: CLAUDE.md "Brand Voice" and "Brand Identity" sections REMOVED and replaced with a single "Brand Voice + Identity" pointer block that defers to `Brand Vault/BrandFoundation_v1.md` §6 + `Brand Vault/Hero_VisualSystemSpec_v1.md`. Rationale: those inline blocks were sourced from the now-retired 2025 brand guide (Cam confirmed retirement 2026-06-02) and v1.1 retired hex `#B71C1C` that the inline block was treating as canonical — proof that inline duplication actively works against us. Vault is now single source of truth, no inline duplication.
- Completed: "Brand & Strategy Sources" section at top of CLAUDE.md expanded — Hero_VisualSystemSpec_v1.md added as a third canonical doc alongside BrandFoundation_v1.md and RecommendationsPacket.md. Includes explicit note that `#B71C1C` is retired, `#D92429` is the new Hero Red — every hex reference in the codebase needs to swap.
- Decision (Cam 2026-06-02): **Pricing policy reversed.** Prior "Never Publish Exact Rates" rule retired. Hero is going public with pricing (Breezy Fresh model). CLAUDE.md `## Pricing` section rewritten to reflect: rates are now public, frame with value pre-frame per RecommendationsPacket Phase B.8, voice rules ("never use 'best rate' / 'best value'") still apply per BrandFoundation §6. Current rates documented in the section (canonical, confirm with Cam before publishing changes).
- For Conductor: live-site CSS color rollout (`#B71C1C` → `#D92429`, plus `#1A1A1A` → `#171E26` if Hero Black is hardcoded) is a Phase B Website Agent work item. The CLAUDE.md no longer hardcodes these — but the actual CSS / page templates almost certainly do. Worth flagging in the next Website Agent session brief.
- For Conductor: RecommendationsPacket Phase B.8 was built on the no-public-rates assumption. The value pre-frame still applies — the page now needs rates ON it with the value framing AROUND them, not just the value framing. Worth a small note added to B.8 (this agent's CLAUDE.md flagged it; the packet itself wasn't edited).
- Open: Website Agent session brief covering: "Same Cleaner Every Visit" copy fix to canon, generic "satisfaction guaranteed" tightening, public-pricing implementation (B.8 update), two QA bugs (Deep Clean em-dash mojibake + duplicate insured-FAQ), color rollout across site CSS (`#B71C1C` → `#D92429`, `#1A1A1A` → `#171E26`). Drafting next.

## 2026-06-01 — Conductor wiring update (Phase 0.1 of RecommendationsPacket)

- Completed: CLAUDE.md updated by the Conductor to bake the Brand Vault + active strategy into this agent's auto-loaded context.
- Completed: New **"Brand & Strategy Sources — READ BEFORE PRODUCING ANY BRAND-FACING OUTPUT"** section added near the top, pointing to `Brand Vault/BrandFoundation_v1.md` (canonical) and `Residential Research Agent/RecommendationsPacket.md` (active strategy). Both must be read before any brand-facing output. If anything in this CLAUDE.md contradicts the Vault, the Vault wins.
- Completed: Residential-only direction locked in. Mission, Service Area, Three Departments, and Active Services blocks updated to reflect 2026-06-01 decision — commercial removed from website framing (ride-down via attrition operationally), Avon UT + Mantua UT added to service area context (travel fee, higher-income targeting), Preston ID demoted to bonus-only.
- Completed: New **"AI / Generative Engine Optimization (GEO)"** section added as an explicit discipline this agent owns alongside classic SEO. Lists B.11.a through B.11.g sub-items with one-line summaries; full checklist lives in RecommendationsPacket Phase B.11.
- Completed: New **"Draft-First Deployment Standard"** section added. Every discretionary website change ships as a Netlify Deploy Preview / PR branch first; Cam previews before merge to main. Monday blog auto-publish (GitHub Actions) explicitly preserved as scheduled-automation exception.
- For Conductor: where the new draft-first standard conflicts with the existing Tier 2 ("auto-deploy, no approval needed") list, the new standard wins. Tier 2 effectively collapses for discretionary edits during the Phase B rebuild period. Cleanup pass on the Tier 2 list is deferred but worth a follow-up.
- For Conductor: Phase B of the RecommendationsPacket is now this agent's active workstream — B.1 (commercial removal), B.2 (de-noindex 10 city pages), B.3 (5 net-new city pages), B.4–B.7 (move-out, move-in, post-construction, Meet Your Team), B.8 (pricing pre-frame), B.9 (referral), B.11 (full GEO discipline). Cam will trigger execution in dedicated Cowork sessions in this folder.
- For Conductor: this CLAUDE.md still has known-stale operational content from before today's edit (the "9 main pages" / "likely not posting" / "#2 organic" notes called out in the 2026-05-09 log entry). Not fixing those today — too easy to introduce drift. Worth a focused cleanup pass.
- Open: Cam to confirm whether Monday blog auto-publish should continue auto-deploying or also flip to draft-first. Current behavior preserved pending decision.

## 2026-05-09 (later, same day) — Domain canonical investigation

- Decision: Documented `theherocleaners.com` as canonical and produced three formal artifacts: `Domain_Reference_Audit.md`, `Domain_Canonical_Recommendation.md`, `Domain_Consolidation_Plan.md`. Engineering side of consolidation was already executed earlier today (separate AGENT_LOG entry below).
- Completed: External citation audit — confirmed 4 platforms clean (GBP, FB, Yelp URL, IG bio per Cam), flagged 3 stale citations (LinkedIn URL, Weebly ghost site, Yelp service description), flagged 6 unverified citations needing Cam-side login (Nextdoor, Thumbtack, Angi, Homeaglow, Care.com, Chamber). Mailchimp deliberately not audited per scope (lives in Hero Dispatch agent folder).
- Completed: Re-verified all redirects still firing correctly at start of audit. 5 test URLs all return HTTP/2 301 with absolute Location to canonical.
- Learned: `heroc1eaners.weebly.com` (note the "1" typo in subdomain) is an active Weebly ghost site titled "HERO CLEANERS PROPERTY SOLUTIONS" — uses the exact forbidden brand phrase from CLAUDE.md and advertises DISCONTINUED services. Independent of canonical work, this is brand-damage risk worth deleting.
- Learned: Yelp listing URL is correct but service description still advertises driveway sealing + Christmas lights + gutter cleaning + pressure washing (all DISCONTINUED). Stale on a different axis than canonical-URL.
- Learned: Google index still contains old-domain URLs as expected (typical 4-8 week lag after 301s go live). Phase 1 Discovery's finding will remain visibly true in SERP during this window even though the engineering is resolved.
- For Conductor: Paid acquisition is unblocked from a canonical-URL standpoint. Residential Research Agent's Phase 1 SEO finding can be marked "engineering resolved 2026-05-09, observable resolution in Google index expected 4-8 weeks out." All LSA / Google Ads destinations should target theherocleaners.com only.
- For Conductor: Hero Dispatch agent should verify its Mailchimp config — campaign from-address and footer URLs should use canonical domain. Worth a separate session in that folder.
- Open: Cam to do ~30-45 min of citation cleanup per Phase 1 of Domain_Consolidation_Plan.md (LinkedIn URL, Yelp service desc, Weebly deletion, directory spot-checks).
- Open: Where does Cam want the BBB profile creation task to live (separate citation-building work, not part of consolidation).
- Open: Printed materials inventory — anything with `herocleanersllc.com` printed on it (cards, vehicle wraps, invoices). 301 catches all hits so non-urgent, but useful for future reprints.
- Decision point: Cam to formally approve the canonical recommendation as recorded. Recommendation is effectively a rubber-stamp since execution is already live, but the doc exists so the choice is findable and defensible cross-agent.

## 2026-05-09 — CLAUDE.md drift resolution

- Decision: Resolved CLAUDE.md vs Website_CLAUDE.md drift via merge. CLAUDE.md is now the single canonical file; Website_CLAUDE.md deleted.
- Completed: Merged 6 operational frameworks from Website_CLAUDE.md into CLAUDE.md verbatim (no content rewrites): Files to read every session, Startup Checklist, Competitor Intelligence, Website Vision, Autonomy Tiers, Deployment Safety Protocol, Self-Improvement Protocol. CLAUDE.md grew 11.3 KB → 18.7 KB (224 → 455 lines).
- Confirmed intact: Conductor coordination section + AGENT_LOG.md logging responsibility, verbatim from prior version at lines 3-67 of new CLAUDE.md.
- For Conductor: This agent now has a single canonical context file. Operational frameworks (autonomy tiers, deployment safety, self-improvement) are now part of auto-loaded context — previously stranded in Website_CLAUDE.md and likely ignored by past sessions.
- Open: Known-stale content in the merged CLAUDE.md, deliberately NOT fixed in this session (separate task):
  - "9 main pages" — actual is 11 (omits maid-service, faq)
  - Blog Automation status "likely not posting" — actually posts every Monday, 10/10 weeks
  - SEO Context "#2 organic" — current is position 1.8 for primary keyword "house cleaning logan utah"
  - Pending Work list (April 2026) — 7 of 8 items already done; in-file note added pointing here

## YYYY-MM-DD
- Log started. Prior history captured in MasterContext.md from initial ecosystem bootstrap.
