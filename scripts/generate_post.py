#!/usr/bin/env python3
import os, sys, json, re, datetime
import anthropic

ROOT_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPICS_FILE  = os.path.join(ROOT_DIR, "topics.json")
TRACKER_FILE = os.path.join(ROOT_DIR, "scripts", "topics_tracker.json")
BLOG_DIR     = os.path.join(ROOT_DIR, "blog")

SYSTEM_PROMPT = """You are a professional SEO content writer for Hero Cleaners LLC, a locally owned cleaning company in Logan, Utah serving all of Cache Valley.

BRAND FACTS:
- Business: Hero Cleaners LLC | Logan, UT 84321
- Phone: (435) 277-0370 | Website: herocleanersllc.com
- Services: Recurring house cleaning, deep cleans, move-out cleans, commercial cleaning, window washing
- Service cities: Logan, North Logan, Smithfield, Hyrum, Nibley, Providence, River Heights, Hyde Park, Wellsville, Richmond, Lewiston, Clarkston
- Founded 2019 | 4.9-star rating | 7,800+ homes cleaned
- Pricing: Starting ~$54/hr, highly flexible and customized

BRAND VOICE: Warm, approachable, genuine — like a friendly neighbor. Never corporate or salesy.
Phrases to USE: "We clean, you relax" · "take the load off" · "Cache Valley" · "heroes"
Phrases to AVOID: "luxury" · "Property Solutions" · anything cold or pushy

SEO RULES:
1. Title: include keyword + Logan UT or Cache Valley — max 60 chars
2. Meta description: 140-155 chars, keyword + location + warm CTA
3. Use H2 subheadings every 200-300 words
4. Mention Logan UT and Cache Valley naturally 3-5 times each
5. Word count: 900-1,100 words
6. End with a warm CTA paragraph linking to herocleanersllc.com and (435) 277-0370

OUTPUT: Return ONLY raw Markdown with this exact front matter:
---
title: "TITLE HERE"
date: YYYY-MM-DD
description: "META DESCRIPTION HERE"
slug: "url-slug-here"
tags: ["post", "house cleaning", "Logan UT", "Cache Valley", "ADDITIONAL TAG"]
---

[Blog post body in Markdown]

No code fences. No preamble. Raw Markdown only."""

TOPIC_GEN_PROMPT = """You generate SEO blog topic ideas for Hero Cleaners LLC, a locally owned cleaning company in Logan, Utah serving Cache Valley.

Services: recurring house cleaning, deep cleaning, move-in/move-out cleaning, commercial cleaning, window washing.
Service cities: Logan, North Logan, Smithfield, Hyrum, Nibley, Providence, River Heights, Hyde Park, Wellsville, Richmond, Lewiston, Clarkston.

Generate exactly 20 new blog topic titles. Each should:
- Target a specific local SEO keyword (e.g. "house cleaning Logan Utah", "maid service Cache Valley", "deep clean Smithfield UT")
- Cover a mix of: cleaning tips, seasonal topics, city-specific topics, recurring cleaning benefits, move-out cleaning, window washing, commercial cleaning, and home maintenance
- Be natural and engaging — not stuffed with keywords
- NEVER repeat or closely paraphrase any topic from the list below

Return ONLY a JSON array of 20 strings. No commentary, no code fences, no numbering."""

def slugify(text):
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")[:80]

def get_used_topics(topics, tracker):
    """Collect all topics that have been used or are queued."""
    used = set()
    for t in topics:
        used.add(t.strip().lower())
    for entry in tracker.get("published", []):
        used.add(entry["topic"].strip().lower())
    return used

def generate_new_topics(client, used_topics):
    """Call Claude API to generate 20 new unique topics."""
    used_list = "\n".join(f"- {t}" for t in sorted(used_topics))
    prompt = f"Here are all previously used or queued topics — do NOT repeat any:\n\n{used_list}\n\nGenerate 20 new topics now."

    print("Generating 20 new blog topics...")
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        system=TOPIC_GEN_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = message.content[0].text.strip()

    # Strip code fences if present
    if raw.startswith("```"):
        raw = re.sub(r"^```\w*\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw)

    new_topics = json.loads(raw)

    # Filter out any duplicates that slipped through
    filtered = [t for t in new_topics if t.strip().lower() not in used_topics]
    print(f"Generated {len(filtered)} new unique topics.")
    return filtered

def main():
    topics  = json.load(open(TOPICS_FILE))
    tracker = json.load(open(TRACKER_FILE)) if os.path.exists(TRACKER_FILE) else {"next_index": 0, "published": []}
    idx     = tracker.get("next_index", 0)
    remaining = len(topics) - idx

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    # Auto-generate new topics when fewer than 5 remain
    if remaining < 5:
        print(f"Only {remaining} topics remaining — auto-generating more.")
        used = get_used_topics(topics, tracker)
        new_topics = generate_new_topics(client, used)
        if new_topics:
            topics.extend(new_topics)
            json.dump(topics, open(TOPICS_FILE, "w"), indent=2, ensure_ascii=False)
            print(f"topics.json now has {len(topics)} total topics ({len(topics) - idx} remaining).")

    if idx >= len(topics):
        print("ERROR: No topics available and generation failed.")
        sys.exit(1)

    topic    = topics[idx]
    date_str = datetime.date.today().isoformat()
    slug     = slugify(topic)

    print(f"Generating post #{idx+1}: {topic}")

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f'Write a full SEO blog post for Hero Cleaners on this topic:\n\n"{topic}"\n\nReturn only raw Markdown.'}],
    )
    content = message.content[0].text

    # Strip any frontmatter the AI may have written (between --- markers) and replace with correct one
    body = content
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            body = content[end+3:].lstrip("\n")

    # Build correct frontmatter
    frontmatter = f"""---
title: "{topic} | Logan UT"
date: {date_str}
description: "Hero Cleaners Cache Valley — {topic[:100]}"
slug: "{slug}"
tags: ["post", "house cleaning", "Logan UT", "Cache Valley"]
layout: post.njk
permalink: /blog/{slug}/index.html
---

"""
    final_content = frontmatter + body

    os.makedirs(BLOG_DIR, exist_ok=True)
    filename = f"{date_str}-{slug}.md"
    open(os.path.join(BLOG_DIR, filename), "w").write(final_content)

    tracker["next_index"] = idx + 1
    tracker["published"].append({"index": idx, "topic": topic, "file": filename, "date": date_str})
    json.dump(tracker, open(TRACKER_FILE, "w"), indent=2)

    print(f"Done! Saved: blog/{filename}")

if __name__ == "__main__":
    main()
