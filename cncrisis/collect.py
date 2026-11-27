"""Public discovery and page acquisition; model reasoning stays with the researcher.

CLI search results from the host's built-in tools enter through bridge; public
GitHub and Crossref discovery work without a linked account or an LLM API key.
"""
import argparse
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request

AGENT = "CN-Crisis-Workbench/0.2 (public research; no household records)"


def now():
    return datetime.now(timezone.utc).isoformat()


def canonical_url(url):
    u = urllib.parse.urlsplit(url)
    if u.scheme not in ("https", "http") or not u.hostname or u.username or u.password:
        raise ValueError("公开来源必须为不含凭据的 http(s) URL")
    query = [(k, v) for k, v in urllib.parse.parse_qsl(u.query, keep_blank_values=True)
             if not k.lower().startswith("utm_") and k.lower() not in {"fbclid", "gclid", "ref_src"}]
    host = u.hostname.lower()
    if u.port and not (u.scheme == "https" and u.port == 443 or u.scheme == "http" and u.port == 80):
        host += ":" + str(u.port)
    return urllib.parse.urlunsplit((u.scheme.lower(), host, u.path or "/", urllib.parse.urlencode(sorted(query)), ""))


class Extractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.in_title = False
        self.title = []
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript"}:
            self.skip += 1
        if tag == "title":
            self.in_title = True
        if tag in {"p", "div", "tr", "h1", "h2", "h3", "br"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript"} and self.skip:
            self.skip -= 1
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)
        if not self.skip:
            self.parts.append(data)


def request(url, limit=12_000_000):
    req = urllib.request.Request(canonical_url(url), headers={"User-Agent": AGENT, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=25) as response:
        raw = response.read(limit + 1)
        if len(raw) > limit:
            raise ValueError("来源超过大小限制；定向读取必要表格")
        return raw, response.geturl(), response.headers


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fetch(args):
    url = canonical_url(args.url)
    key = hashlib.sha256(url.encode()).hexdigest()[:20]
    base = args.workspace / "cache" / key
    record = {"url": url, "retrieved_at": now(), "publisher_family": args.family,
              "record_type": args.kind, "observation_period": args.period,
              "release_date": args.release_date, "event_id": args.event_id,
              "source_id": "SRC-" + key, "status": "retrieval_failed"}
    try:
        raw, final, headers = request(url)
        mime = headers.get_content_type()
        encoding = headers.get_content_charset() or "utf-8"
        text = raw.decode(encoding, errors="replace") if mime != "application/pdf" else ""
        title = ""
        if "html" in mime:
            page = Extractor()
            page.feed(text)
            text = re.sub(r"[ \t]+", " ", "".join(page.parts)).strip()
            title = " ".join(page.title).strip()
        base.mkdir(parents=True, exist_ok=True)
        (base / "raw.bin").write_bytes(raw)
        (base / "extracted.txt").write_text(text, encoding="utf-8")
        record.update(status="retrieved", final_url=final, content_type=mime,
                      sha256=hashlib.sha256(raw).hexdigest(), text_sha256=hashlib.sha256(text.encode()).hexdigest(),
                      title=title, bytes=len(raw), raw_path=str(base / "raw.bin"),
                      text_path=str(base / "extracted.txt"),
                      verification="采集完成；研究者按来源定位和口径核读后登记论据")
    except (OSError, ValueError, LookupError) as exc:
        record["error"] = str(exc)
    write_json(args.workspace / "acquisition" / (key + ".json"), record)
    if args.output:
        write_json(Path(args.output), record)
    return record


def discover(args):
    query = args.query
    result = {"provider": args.provider, "query": query, "executed_at": now(),
              "topic": args.topic, "period": args.period, "status": "failed", "results": []}
    try:
        if args.provider == "github":
            url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode({"q": query, "per_page": args.limit})
            raw, _, _ = request(url)
            body = json.loads(raw)
            for item in body.get("items", []):
                result["results"].append({"url": item["html_url"], "title": item["full_name"],
                                          "description": item.get("description"), "updated_at": item.get("updated_at"),
                                          "license": (item.get("license") or {}).get("spdx_id"),
                                          "interpretation": "代码候选，需读实际实现及许可"})
        elif args.provider == "crossref":
            url = "https://api.crossref.org/works?" + urllib.parse.urlencode({"query.bibliographic": query, "rows": args.limit})
            raw, _, _ = request(url)
            for item in json.loads(raw)["message"].get("items", []):
                result["results"].append({"url": item.get("URL"), "title": " ".join(item.get("title", [])),
                                          "doi": item.get("DOI"), "publisher": item.get("publisher"),
                                          "published": item.get("published"), "interpretation": "论文线索，需读作者原文"})
        result["status"] = "completed" if result["results"] else "zero_results"
    except (OSError, ValueError, KeyError) as exc:
        result["error"] = str(exc)
    key = hashlib.sha256((args.provider + query + args.period).encode()).hexdigest()[:20]
    write_json(args.workspace / "acquisition" / ("search-" + key + ".json"), result)
    if args.output:
        write_json(Path(args.output), result)
    return result


def bridge(args):
    source = json.loads(Path(args.file).read_text(encoding="utf-8"))
    if not isinstance(source, dict) or not isinstance(source.get("results"), list):
        raise ValueError("bridge需JSON对象及results数组")
    if not source.get("query") or not source.get("provider"):
        raise ValueError("bridge需原查询query和实际provider")
    executed = source.get("executed_at") or source.get("searched_at")
    if not executed:
        raise ValueError("bridge需原检索时间executed_at；不能把导入时间当检索时间")
    source["executed_at"] = executed
    source["imported_at"] = now()
    source.setdefault("status", "completed" if source["results"] else "zero_results")
    for row in source["results"]:
        row["url"] = canonical_url(row["url"])
        if not row.get("title"):
            raise ValueError("每条检索线索需标题")
    key = hashlib.sha256(json.dumps(source, sort_keys=True).encode()).hexdigest()[:20]
    write_json(args.workspace / "acquisition" / ("bridge-" + key + ".json"), source)
    return {"ok": True, "imported_results": len(source["results"]), "query": source["query"],
            "file": str(args.workspace / "acquisition" / ("bridge-" + key + ".json")),
            "next": "研究者核读原文、挑出事实/观点，再用ingest和search-log登记"}


def register_cli(subparsers):
    parser = subparsers.add_parser("collect", help="公共来源采集、无账号发现、内置工具结果桥接")
    subs = parser.add_subparsers(dest="collect_command", required=True)
    p = subs.add_parser("fetch")
    p.add_argument("--url", required=True)
    p.add_argument("--family", required=True)
    p.add_argument("--kind", choices=["fact", "viewpoint", "method", "policy"], required=True)
    p.add_argument("--period", required=True)
    p.add_argument("--release-date", default="")
    p.add_argument("--event-id", default="")
    p.add_argument("--output")
    p.set_defaults(func=fetch)
    p = subs.add_parser("discover")
    p.add_argument("--provider", choices=["github", "crossref"], required=True)
    p.add_argument("--query", required=True)
    p.add_argument("--topic", required=True)
    p.add_argument("--period", required=True)
    p.add_argument("--limit", type=int, choices=range(1, 21), default=5)
    p.add_argument("--output")
    p.set_defaults(func=discover)
    p = subs.add_parser("bridge")
    p.add_argument("--file", required=True)
    p.set_defaults(func=bridge)
