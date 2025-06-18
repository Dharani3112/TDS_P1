#!/usr/bin/env python3
"""
Process Discourse Data for TDS Virtual TA

1. Scans scripts/raw directory for topic-*.json files (exported from Discourse).
2. Builds a consolidated data/discourse_data.json file containing:
   - topics: {topic_id, title, url, full_content}
   - all_qa_pairs: Extracts simple Q&A pairs where staff answers follow student questions.

The script is VERBOSE: prints progress, counts, and missing fields.
Run: python scripts/process_discourse_data.py
"""

import json
import re
import html
from pathlib import Path
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RAW_DATA_DIR = Path("scripts/raw")
OUTPUT_DATA_FILE = Path("data/discourse_data.json")

# A set of known staff usernames for identifying answers
STAFF_USERNAMES = {
    "anand", "anand.s", "anands", "tds_staff"
}

HTML_TAG_PATTERN = re.compile(r"<[^>]+>")


def sanitize_html(text: str) -> str:
    """Remove HTML tags, unescape entities, and normalize whitespace."""
    if not text:
        return ""
    # Unescape HTML entities like &amp;
    text = html.unescape(text)
    # Remove all HTML tags
    text = HTML_TAG_PATTERN.sub(" ", text)
    # Normalize whitespace to single spaces
    return re.sub(r"\s+", " ", text).strip()


def process_single_topic_file(file_path: Path) -> Dict[str, Any]:
    """Loads a single topic JSON file and extracts key information."""
    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Could not read or parse {file_path.name}: {e}")
        return {}

    topic_id = data.get("topic_id") or data.get("id")
    if not topic_id:
        logger.warning(f"Skipping {file_path.name}: missing topic_id.")
        return {}

    title = data.get("title", f"Untitled Topic {topic_id}")
    slug = data.get("slug") or data.get("topic_slug") or re.sub(r"[\W_]+", "-", title).strip("-").lower()
    url = f"https://discourse.onlinedegree.iitm.ac.in/t/{slug}/{topic_id}"

    posts = data.get("post_stream", {}).get("posts", [])
    content_parts: List[str] = []
    qa_pairs: List[Dict[str, Any]] = []

    first_post_content = None
    is_answer_found = False

    for post in posts:
        post_content = sanitize_html(post.get("cooked", ""))
        if not post_content:
            continue
        
        content_parts.append(post_content)

        # Heuristic: First post is the question
        if first_post_content is None:
            first_post_content = post_content
            continue

        # Heuristic: First reply from a staff member is the answer
        if not is_answer_found and post.get("username", "").lower() in STAFF_USERNAMES:
            qa_pairs.append({
                "question": first_post_content,
                "answer": post_content,
                "source_topic_id": topic_id,
                "source_topic_title": title,
                "source_url": url
            })
            is_answer_found = True

    full_content = "\n\n".join(content_parts)

    topic_data = {
        "topic_id": topic_id,
        "title": title,
        "url": url,
        "full_content": full_content
    }

    return {"topic": topic_data, "qa_pairs": qa_pairs}


def main():
    """Main function to process all raw discourse files."""
    if not RAW_DATA_DIR.exists():
        logger.error(f"Raw data directory not found: {RAW_DATA_DIR}")
        return

    all_topics: List[Dict[str, Any]] = []
    all_qa_pairs: List[Dict[str, Any]] = []

    topic_files = sorted(RAW_DATA_DIR.glob("topic-*.json"))
    file_count = len(topic_files)
    logger.info(f"Found {file_count} raw Discourse topic files to process.")

    for i, file_path in enumerate(topic_files, 1):
        logger.info(f"Processing file {i}/{file_count}: {file_path.name}...")
        processed_data = process_single_topic_file(file_path)
        if processed_data:
            if "topic" in processed_data:
                all_topics.append(processed_data["topic"])
            if "qa_pairs" in processed_data:
                all_qa_pairs.extend(processed_data["qa_pairs"])

    logger.info("\nDiscourse data processing summary:")
    logger.info(f"  - Total topics processed: {len(all_topics)}")
    logger.info(f"  - Q&A pairs extracted: {len(all_qa_pairs)}")

    # Ensure the output directory exists
    OUTPUT_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the consolidated data to the output file
    consolidated_data = {
        "topics": all_topics,
        "qa_pairs": all_qa_pairs
    }
    
    with OUTPUT_DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(consolidated_data, f, indent=2, ensure_ascii=False)
        
    logger.info(f"Successfully saved consolidated data to {OUTPUT_DATA_FILE}")


if __name__ == "__main__":
    main()