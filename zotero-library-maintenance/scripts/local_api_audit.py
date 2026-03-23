#!/usr/bin/env python3
import argparse
import json
import os
import urllib.parse
import urllib.request
from collections import Counter


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
    parser.add_argument("--base-url", default=os.environ.get("ZOTERO_BASE_URL", "http://localhost:23119"))
    parser.add_argument("--user-id", default=os.environ.get("ZOTERO_USER_ID", "0"))
    args = parser.parse_args()

    items = fetch_all(build_base(args.base_url, args.user_id))

    top_level_nonattachment_unfiled = []
    top_level_attachments = []
    top_level_missing_date = []
    missing_pdf_attachments = []

    for obj in items:
        d = obj["data"]
        item_type = d.get("itemType")
        is_top_level = not d.get("parentItem")

        if is_top_level and item_type not in {"attachment", "note", "annotation"} and not d.get("collections"):
            top_level_nonattachment_unfiled.append(d)

        if is_top_level and item_type == "attachment":
            top_level_attachments.append(d)

        if is_top_level and item_type not in {"attachment", "note", "annotation"} and not (d.get("date") or "").strip():
            top_level_missing_date.append(d)

        if item_type == "attachment" and d.get("contentType") == "application/pdf":
            path = enclosure_path(obj)
            if not (path and os.path.exists(path)):
                missing_pdf_attachments.append(
                    {
                        "key": d["key"],
                        "title": d.get("title", ""),
                        "parentItem": d.get("parentItem"),
                        "linkMode": d.get("linkMode", ""),
                        "url": d.get("url", ""),
                    }
                )

    summary = {
        "total_items": len(items),
        "top_level_nonattachment_unfiled": len(top_level_nonattachment_unfiled),
        "top_level_attachments": len(top_level_attachments),
        "top_level_missing_date": len(top_level_missing_date),
        "missing_pdf_attachments": len(missing_pdf_attachments),
        "missing_pdf_by_link_mode": Counter(x["linkMode"] for x in missing_pdf_attachments),
        "samples": {
            "unfiled": top_level_nonattachment_unfiled[:20],
            "attachments": top_level_attachments[:20],
            "missing_date": top_level_missing_date[:20],
            "missing_pdf": missing_pdf_attachments[:40],
        },
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, default=list))


if __name__ == "__main__":
    main()
