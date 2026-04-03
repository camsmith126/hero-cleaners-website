# Hero Cleaners LLC — Claude Code Master Context

## Business Identity
- **Legal Name:** Hero Cleaners LLC
- **Address:** 1034 RSI Dr Suite 100, Logan, Utah 84321
- **Phone:** (435) 277-0370
- **Email:** herocleanersinfo@gmail.com
- **Owner:** Cameron Smith
- **Founded:** 2019 | LLC registered 2021
- **Rating:** 4.9 stars
- **Live site:** theherocleaners.com (Netlify)
- **Old site:** herocleanersllc.com (301 redirects to theherocleaners.com)
- **GitHub:** camsmith126/hero-cleaners-website
- **Netlify team:** slamenterprises23

## Mission & Vision
Provide consistent, amazing home and commercial cleaning that genuinely makes people's lives easier. Vision: become THE home service provider in Cache Valley. Revenue goal: $1M within ~3 years.

## Service Area
Logan, Utah + all of Cache Valley: North Logan, Smithfield, Hyrum, Nibley, Providence, River Heights, Hyde Park, Wellsville, Richmond, Lewiston, Clarkston

## Three Departments
- **Residential** — managed by Jaylee (GM, primary revenue driver)
- **Windows** — managed by Abbey (also handles all billing) — seasonal March–November only
- **Commercial** — managed by Laura

## Active Services — Always Promote
House Cleaning, Maid Service, Recurring Cleaning, Deep Cleaning, Move-In/Move-Out Cleaning, Commercial Cleaning, Window Washing

## DISCONTINUED — Never Mention or Promote
Power washing, driveway sealing, Christmas lights, Airbnb turnovers, apartment complexes, contractor/construction cleanup

## Pricing (Internal Only — Never Publish Exact Rates)
- All recurring plans: $60/hr
- Weekly visits: 2hr | Bi-weekly: 2.5hr
- Weekly costs less per visit only because less work is needed — NOT a better rate
- Never use "best rate," "best value," or imply one plan is cheaper per hour

## Brand Identity
**Colors:**
- Hero Red: #B71C1C | Hero Black: #1A1A1A | Clean White: #FFFFFF
- Accent Red: #D32F2F | Light Rose: #FFCDD2 | Charcoal: #2D2D2D

**Fonts:** Bebas Neue / Impact (headings) · Open Sans / Helvetica Neue (body)

**Logo:** Black superhero figure with red cape + "Hero" (black bold) + "Cleaners" (red bold) + squeegee icon

## Brand Voice
- Warm, personal, local — "like the neighbor who shows up without being asked"
- Friendly, hardworking, down-to-earth, genuine, confident but not cocky
- Always Cache Valley / Logan Utah local — never implies national reach
- Never corporate, cold, salesy, or franchise-sounding
- Recurring residential is always the nudge — every page guides toward recurring

**Use these phrases:** "We clean, you relax" · "Take the load off" · Hero/heroes · Cache Valley · Trust, relationships, experience

**Never use:** "Property Solutions" · luxury-focused language · corporate/cold tone · condescending language · one-size-fits-all messaging

## The Core Positioning
The people ARE the product. Customers don't just love clean homes — they love having someone they know and trust. Jaylee has transformed the customer experience. Recurring customers build genuine relationships with their cleaners. This is the competitive edge.

## Customer Hesitations — Never Contradict in Copy
- "Cleaning is a luxury" → It's not; it's about getting time back
- "I'm lazy if I hire a cleaner" → Everyone could use an extra hand
- "I'm nervous about someone in my home" → Trust and relationships are core
- "I'm embarrassed about my house" → No judgment, ever

## Site Architecture
- All main HTML pages in /website/
- Stack: Static HTML/CSS/JS + Eleventy (11ty)
- Netlify auto-deploys on every push to main
- 9 main pages: index, about, contact, recurring-cleaning, deep-clean, commercial-cleaning, window-washing, reviews, service-areas
- 10 hidden city SEO pages (noindex) in /website/ — never make indexable, never add to nav
- Blog posts live in /blog/ as Markdown files with front matter

## Blog Automation — ACTIVE PRIORITY
The blog is a core SEO strategy. Weekly posts targeting local cleaning keywords help rank for "house cleaning Logan Utah" and surrounding Cache Valley city searches.

### How It Works
- `generate_post.py` — Python script that uses the Claude API to write a new blog post
- `topics.json` — Queue of upcoming blog post topics/keywords to write about
- GitHub Actions workflow — scheduled to run weekly and auto-publish new posts
- Posts are Markdown files fed through Eleventy and published to /blog/ on the live site

### Current Status — NEEDS ATTENTION
The blog automation is likely not posting. When starting a session, check:
1. When was the last blog post published? (check /blog/ directory for most recent file date)
2. Is the GitHub Actions workflow running? (check .github/workflows/ and Actions tab on GitHub)
3. Is topics.json populated with upcoming topics?
4. Are there any errors in the workflow logs?

### Blog Post Standards
Every post must:
- Target a specific local keyword naturally (e.g. "house cleaning Logan Utah," "maid service Cache Valley," "deep clean Smithfield UT")
- Be 600–900 words minimum for SEO value
- Match Hero Cleaners brand voice — warm, local, helpful, never salesy
- Include a CTA toward recurring cleaning or booking
- Never mention discontinued services
- Have proper Eleventy front matter (title, date, description, tags including "post")

### Blog Topic Direction
Good topics to cover:
- "How often should you deep clean your home in Logan, UT"
- "Best recurring cleaning schedule for Cache Valley families"
- "What to expect from your first professional house cleaning"
- "Spring cleaning checklist for Logan Utah homeowners"
- "How to prepare your home for a move-out clean"
- City-specific pages: "House cleaning in [Smithfield/Providence/North Logan/etc.]"
- Window washing seasonal topics (spring/fall)
- Commercial cleaning tips for Logan businesses

### Monitoring Responsibility
At the start of every session, check if a new blog post has gone out in the past 7 days. If not, flag it and either fix the automation or manually generate and publish a post. Weekly cadence is the goal — this directly impacts SEO ranking.

## SEO Context
- Primary keyword: "house cleaning Logan Utah"
- Current position: #2 organic (behind Clean Freak at cleanfreakut.com)
- All 9 main pages have: canonical tags, Open Graph tags, structured data schema
- Sitemap at /sitemap.xml — update when adding pages
- Blog posts should be included in sitemap

**Target homepage title:** `Hero Cleaners | #1 House Cleaning in Logan, UT | Book Online`
**Target homepage meta:** `Cache Valley's most trusted house cleaning team. Recurring, deep clean & move-out services. Friendly, reliable, locally owned. Book online in minutes — (435) 277-0370.`

**Competitors:** Clean Freak (cleanfreakut.com) · ACDC Cleaning · Clean & Tide · Special House Cleaning · Queens Cleaning

## Pending Work (as of April 2026)
- [ ] Favicon code still needs adding to all 9 main HTML pages
- [ ] Blog automation needs audit — likely not posting, needs diagnosis and fix
- [ ] _redirects file needs creating in Netlify
- [ ] herocleanersllc.com needs adding as redirect domain in Netlify
- [ ] theherocleaners.com DNS needs pointing to Netlify as primary
- [ ] Google Business Profile URL needs updating
- [ ] Facebook, Yelp, Instagram bio links need updating
- [ ] theherocleaners.com needs submitting to Google Search Console

## Embeds — Never Remove or Alter
- HCP (Housecall Pro) booking widget — must remain on site
- HCP chat bubble — must remain on site
- Both must stay functional after any change

## Critical Technical Rules
1. Surgical edits only — no full rewrites unless explicitly asked
2. Never alter nav logic — outside-click-to-close is on ALL pages
3. Mobile nav uses navLinks.style.display toggled by .hamburger — do not overwrite
4. Always verify file still starts with <!DOCTYPE html> after any edit
5. Em dashes in HTML = &mdash; — never use literal — character
6. Flag downstream issues BEFORE making changes, not after
7. "Done" means ALL affected pages fixed, not just one
8. Never change existing page URLs — they are indexed by Google
9. Never add city SEO pages to navigation

## Git Workflow
- Commit with descriptive messages explaining what changed and why
- Push to main triggers automatic Netlify deploy
- Never force push to main
