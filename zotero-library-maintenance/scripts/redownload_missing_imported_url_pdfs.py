#!/usr/bin/env python3
import argparse
import json
import os
import ssl
import urllib.parse
import urllib.request
from pathlib import Path

from zotero_discovery import discover_local_api


def build_base(base_url, user_id):
    return f"{base_url.rstrip('/')}/api/users/{user_id}/items"


def fetch_all(base_url):
    start = 0
    limit = 200
    items = []
    while True:
        with urllib.request.urlopen(f"{base_url}?limit={limit}&start={start}") as r:
            batch = json.load(r)
        if not batch:
            break
        items.extend(batch)
        if len(batch) < limit:
            break
        start += limit
    return items


def enclosure_path(obj):
    href = obj.get("links", {}).get("enclosure", {}).get("href", "")
    if href.startswith("file://"):
        return urllib.parse.unquote(href[7:])
    return ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url")
    parser.add_argument("--user-id")
    parser.add_argument("--timeout", type=float, default=2.0)
    args = parser.parse_args()

    if args.base_url:
        base_url = args.base_url
        user_id = args.user_id or os.environ.get("ZOTERO_USER_ID", "0")
    else:
        discovered = discover_local_api(timeout=args.timeout)
        base_url = discovered["base_url"]
        user_id = args.user_id or discovered["user_alias"]

    items = fetch_all(build_base(base_url, user_id))
    ssl_ctx = ssl.create_default_context()
    headers = {"User-Agent": "Mozilla/5.0"}

    log = {"base_url": base_url, "user_id": user_id, "totalPlanned": 0, "downloaded": [], "errors": []}

    candidates = []
    for obj in items:
        d = obj["data"]
        if d.get("itemType") != "attachment":
            continue
        if d.get("contentType") != "application/pdf":
            continue
        if d.get("linkMode") != "imported_url":
            continue
        url = d.get("url") or ""
        if not url.startswith(("http://", "https://")):
            continue
        path = enclosure_path(obj)
        if not path or os.path.exists(path):
            continue
        candidates.append({"key": d["key"], "url": url, "path": path})

    log["totalPlanned"] = len(candidates)

    for c in candidates:
        try:
            req = urllib.request.Request(c["url"], headers=headers)
            with urllib.request.urlopen(req, timeout=60, context=ssl_ctx) as r:
                content_type = r.headers.get("Content-Type", "")
                data = r.read()
            if not data:
                raise RuntimeError("empty response")
            if not (data.startswith(b"%PDF-") or "pdf" in content_type.lower()):
                raise RuntimeError(f"not pdf: {content_type}")

            path = Path(c["path"])
            path.parent.mkdir(parents=True, exist_ok=True)
            tmp = path.with_suffix(path.suffix + ".tmp")
            tmp.write_bytes(data)
            tmp.replace(path)
            log["downloaded"].append(
                {"key": c["key"], "path": str(path), "bytes": len(data)}
            )
        except Exception as e:
            log["errors"].append({"key": c["key"], "url": c["url"], "error": str(e)})

    print(json.dumps(log, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
