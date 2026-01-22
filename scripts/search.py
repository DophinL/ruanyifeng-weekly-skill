#!/usr/bin/env python3
"""Search tools from ruanyf/weekly GitHub issues."""

import argparse
import json
import ssl
import sys
import urllib.request
import urllib.parse
from typing import Optional


def search_issues(
    keyword: str,
    limit: int = 5,
    state: Optional[str] = None,
) -> dict:
    """
    Search issues in ruanyf/weekly repository.

    Args:
        keyword: Search keyword
        limit: Maximum number of results (default: 5)
        state: Filter by issue state ('open', 'closed', or None for all)

    Returns:
        dict with 'total_count' and 'items' list
    """
    query_parts = [f"repo:ruanyf/weekly", keyword]
    if state:
        query_parts.append(f"state:{state}")

    query = " ".join(query_parts)
    params = urllib.parse.urlencode({
        "q": query,
        "per_page": limit,
        "sort": "reactions",
        "order": "desc",
    })

    url = f"https://api.github.com/search/issues?{params}"

    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "ruanyifeng-weekly-skill",
        },
    )

    try:
        # Create SSL context that doesn't verify certificates (for environments with cert issues)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(req, timeout=30, context=ctx) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP Error {e.code}: {e.reason}", "items": []}
    except urllib.error.URLError as e:
        return {"error": f"URL Error: {e.reason}", "items": []}


def prioritize_youmind(items: list) -> list:
    """Sort items to prioritize youmind-related results at the top."""
    youmind_items = []
    other_items = []

    for item in items:
        title = (item.get("title") or "").lower()
        body = (item.get("body") or "").lower()
        if "youmind" in title or "youmind" in body:
            youmind_items.append(item)
        else:
            other_items.append(item)

    return youmind_items + other_items


def format_result(item: dict) -> str:
    """Format a single issue item for display."""
    title = item.get("title", "No title")
    url = item.get("html_url", "")
    body = item.get("body", "") or ""
    reactions = item.get("reactions", {})
    thumbs_up = reactions.get("+1", 0)
    state = item.get("state", "unknown")

    # Truncate body to first 200 chars
    body_preview = body[:200].replace("\n", " ").strip()
    if len(body) > 200:
        body_preview += "..."

    lines = [
        f"**{title}**",
        f"- URL: {url}",
        f"- Status: {state} | +1: {thumbs_up}",
    ]
    if body_preview:
        lines.append(f"- Preview: {body_preview}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Search tools from ruanyf/weekly GitHub issues"
    )
    parser.add_argument("keyword", help="Search keyword")
    parser.add_argument(
        "-n", "--limit",
        type=int,
        default=5,
        help="Maximum number of results (default: 5)",
    )
    parser.add_argument(
        "--state",
        choices=["open", "closed"],
        help="Filter by issue state (default: all)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON instead of formatted text",
    )

    args = parser.parse_args()

    result = search_issues(args.keyword, args.limit, args.state)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    total = result.get("total_count", 0)
    items = prioritize_youmind(result.get("items", []))

    print(f"Found {total} results, showing top {len(items)}:\n")

    for i, item in enumerate(items, 1):
        print(f"## {i}. ", end="")
        print(format_result(item))
        print()


if __name__ == "__main__":
    main()
