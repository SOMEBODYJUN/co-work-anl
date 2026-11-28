"""Public author-archive inventories; metadata and reading are separate states."""
import hashlib
import html
import json
from pathlib import Path
import re
import urllib.parse

from .collect import now, request, write_json


def inventory(args):
    site = args.site.lower().strip()
    if not re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", site):
        raise ValueError("site须为公开WordPress站点域名，不含路径或凭据")
    path = Path(args.output)
    previous = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    if previous and previous.get("site") != site:
        raise ValueError("现有清单属于另一站点；请使用独立输出路径")
    old = {p["id"]: p for p in previous.get("posts", [])}
    posts, reported, pages = {}, None, 0
    for page in range(1, args.max_pages + 1):
        query = urllib.parse.urlencode({"number": 100, "page": page,
            "fields": "ID,URL,date,modified,title,categories,tags"})
        url = "https://public-api.wordpress.com/rest/v1.1/sites/" + site + "/posts/?" + query
        raw, _, _ = request(url)
        response = json.loads(raw)
        reported = response["found"] if reported is None else reported
        pages += 1
        for item in response.get("posts", []):
            metadata = {"id": item["ID"], "url": item["URL"],
                "published_at": item["date"], "modified_at": item.get("modified"),
                "title": html.unescape(item["title"]),
                "categories": sorted(item.get("categories", {}))}
            digest = hashlib.sha256(json.dumps(metadata, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
            prior = old.get(item["ID"], {})
            state = prior.get("reading_status", "metadata_only")
            if prior.get("metadata_sha256") not in (None, digest) and state != "metadata_only":
                state = "needs_reread"
            row = dict(metadata, metadata_sha256=digest, reading_status=state,
                       queue="topic_triage", claim_ids=prior.get("claim_ids", []))
            for key in ("reading_note", "exclusion_reason"):
                if prior.get(key):
                    row[key] = prior[key]
            posts[item["ID"]] = row
        if not response.get("posts") or page * 100 >= reported:
            break
    rows = sorted(posts.values(), key=lambda row: (row["published_at"], row["id"]))
    complete = len(rows) == reported
    def finished(row):
        return row["reading_status"] == "distilled_reviewed" or (
            row["reading_status"] == "excluded_with_reason" and bool(row.get("exclusion_reason")))
    result = {
        "schema": "cncrisis-author-corpus.v1", "site": site,
        "retrieved_at": now(), "reported_public_posts": reported,
        "inventoried_posts": len(rows), "pages_fetched": pages,
        "metadata_inventory_complete": complete,
        "full_article_distillation_complete": complete and all(finished(row) for row in rows),
        "scope": "Currently public posts at this site only; excludes private/deleted posts, paid research and other channels. Metadata does not establish that an article was read.",
        "posts": rows,
    }
    write_json(path, result)
    return {key: value for key, value in result.items() if key != "posts"} | {"output": str(path)}


def register_cli(subparsers):
    parser = subparsers.add_parser("analysts", help="分析者公开文章目录与逐篇学习队列")
    subs = parser.add_subparsers(dest="analyst_command", required=True)
    p = subs.add_parser("inventory-wordpress", help="盘点公开WordPress博客；不代替正文研读")
    p.add_argument("--site", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--max-pages", type=int, choices=range(1, 101), default=30)
    p.set_defaults(func=inventory)
    from . import reading
    reading.register_cli(subs)
