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

BRAND VOICE: Warm, approachable, genuine â like a friendly neighbor. Never corporate or salesy.
Phrases to USE: "We clean, you relax" Â· "take the load off" Â· "Cache Valley" Â· "heroes"
Phrases to AVOID: "luxury" Â· "Property Solutions" Â· anything cold or pushy

SEO RULES:
1. Title: include keyword + Logan UT or Cache Valley â max 60 chars
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

def slugify(text):
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")[:80]

def main():
    topics  = json.load(open(TOPICS_FILE))
    tracker = json.load(open(TRACKER_FILE)) if os.path.exists(TRACKER_FILE) else {"next_index": 0, "published": []}
    idx     = tracker.get("next_index", 0)

    if idx >= len(topics):
        print("All topics published! Add more to topics.json.")
        sys.exit(0)

    topic    = topics[idx]
    date_str = datetime.date.today().isoformat()
    slug     = slugify(topic)

    print(f"Generating post #{idx+1}: {topic}")

    client  = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f'Write a full SEO blog post for Hero Cleaners on this topic:\n\n"{topic}"\n\nReturn only raw Markdown.'}],
    )
    content = message.content[0].text

    os.makedirs(BLOG_DIR, exist_ok=True)
    filename = f"{date_str}-{slug}.md"
    open(os.path.join(BLOG_DIR, filename), "w").write(content)

    tracker["next_index"] = idx + 1
    tracker["published"].append({"index": idx, "topic": topic, "file": filename, "date": date_str})
    json.dump(tracker, open(TRACKER_FILE, "w"), indent=2)

    print(f"Done! Saved: blog/{filename}")

if __name__ == "__main__":
    main()
