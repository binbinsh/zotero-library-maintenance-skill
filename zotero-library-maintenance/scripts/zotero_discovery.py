#!/usr/bin/env python3
import json
import os
import urllib.request


DEFAULT_CANDIDATE_BASES = [
    "http://127.0.0.1:23119",
    "http://localhost:23119",
]


def _probe_api_root(base_url, timeout=2.0):
    req = urllib.request.Request(f"{base_url.rstrip('/')}/api/")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        headers = dict(r.headers.items())
        body = r.read().decode("utf-8", "ignore")
    if "X-Zotero-Version" not in headers or "Zotero-API-Version" not in headers:
        raise RuntimeError("not a Zotero local API root")
    return {"headers": headers, "body": body}


def _resolve_user(base_url, timeout=2.0):
    req = urllib.request.Request(f"{base_url.rstrip('/')}/api/users/0/items?limit=1")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        headers = dict(r.headers.items())
        payload = json.loads(r.read().decode("utf-8", "ignore"))
    resolved_user_id = None
    if payload:
        resolved_user_id = payload[0].get("library", {}).get("id")
    if not resolved_user_id:
        link = headers.get("Link", "")
        marker = "users/"
        if marker in link:
            try:
                resolved_user_id = int(link.split(marker, 1)[1].split("/", 1)[0])
            except Exception:
                resolved_user_id = None
    return {"user_alias": "0", "resolved_user_id": resolved_user_id}


def discover_local_api(candidate_bases=None, timeout=2.0):
    bases = []
    env_base = os.environ.get("ZOTERO_BASE_URL")
    if env_base:
        bases.append(env_base)
    bases.extend(candidate_bases or [])
    for base in DEFAULT_CANDIDATE_BASES:
        if base not in bases:
            bases.append(base)

    attempts = []
    for base_url in bases:
        try:
            probe = _probe_api_root(base_url, timeout=timeout)
            user = _resolve_user(base_url, timeout=timeout)
            return {
                "base_url": base_url.rstrip("/"),
                "headers": probe["headers"],
                "user_alias": user["user_alias"],
                "resolved_user_id": user["resolved_user_id"],
                "attempts": attempts + [{"base_url": base_url, "ok": True}],
            }
        except Exception as e:
            attempts.append({"base_url": base_url, "ok": False, "error": str(e)})

    raise RuntimeError(f"Unable to discover a working Zotero local API base URL: {attempts}")
