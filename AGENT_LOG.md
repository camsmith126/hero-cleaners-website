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
