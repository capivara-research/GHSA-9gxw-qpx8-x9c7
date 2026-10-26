# GHSA-9gxw-qpx8-x9c7 — LaraDashboard stored XSS via SVG upload

> CVE assigned: **[CVE-2026-90931](https://www.cve.org/CVERecord?id=CVE-2026-90931)**. The maintained CVE repository is [capivara-research/CVE-2026-90931](https://github.com/capivara-research/CVE-2026-90931).

[Português do Brasil](README.pt-BR.md) · [Official advisory](https://github.com/laradashboard/laradashboard/security/advisories/GHSA-9gxw-qpx8-x9c7)

Public research evidence and safe local-lab reproduction material for stored cross-site scripting in LaraDashboard's media library.

## At a glance

| Field | Value |
|---|---|
| Product | LaraDashboard |
| Product repository | [`laradashboard/laradashboard`](https://github.com/laradashboard/laradashboard) |
| Affected versions | `>= 0.9.0, <= 1.2.2` |
| Tested revision | `9dc1335835701651aef3adcb3e885acecb32402c` |
| Weakness | CWE-79, CWE-434 |
| Severity | Medium — CVSS 3.1 `5.4` |
| CVSS vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:L/I:L/A:N` |
| Required permission | `media.create` |
| Advisory | `GHSA-9gxw-qpx8-x9c7` |

## Summary

The production upload pipeline accepts SVG files without sanitizing active content. The files are stored under the application's origin and served inline as `image/svg+xml`. A content-level user holding only `media.create` can therefore store JavaScript that executes when another user opens the file.

## Root cause

Outside demo mode, `MediaUploadRequest` applies only generic file and size validation. SVG is explicitly recognized as `image/svg+xml`, while the subsequent checks validate extension/MIME consistency but never sanitize the SVG DOM or reject scripts and event handlers.

## Technical targets

| Item | Value |
|---|---|
| Upload endpoint | `POST /admin/media` |
| Attacker-controlled parameter | Multipart field `files[]` |
| Request validation | `app/Http/Requests/MediaUploadRequest.php` |
| Media processing | `app/Concerns/HandlesMediaOperations.php` |
| Dangerous input | Active SVG content, including `<script>` and event handlers |

## Reproduction

The original coordinated disclosure validated the issue end to end using a custom role with only `media.create` and `media.view`.

The [`poc/`](poc/) directory contains:

- a non-invasive source verifier;
- a harmless SVG marker payload;
- a loopback-only upload helper requiring explicit `--execute`.

The marker changes visible text in the SVG document and sets the fragment to `XSS_MARKER`; it does not read cookies, tokens, or other application data.

## Impact

JavaScript executes in the dashboard origin after user interaction. When opened by an authenticated administrator, same-origin script can act with that user's browser privileges. The published advisory conservatively scores the issue as CVSS 3.1 `5.4`.

## Remediation

- Sanitize SVG content using a maintained SVG sanitizer.
- Alternatively reject SVG uploads or force them to download as attachments.
- Serve user-controlled media from a separate origin.
- Apply MIME validation in production, not only demo mode.
- Replace executable-extension blocklists with a strict allowlist.
- Add `Content-Security-Policy` and `X-Content-Type-Options: nosniff` as defense in depth.

## Disclosure

Reported through GitHub Private Vulnerability Reporting and published by the project on 2026-08-30. Reporter credit: [capivara-research](https://github.com/capivara-research).

## References

- [LaraDashboard product repository](https://github.com/laradashboard/laradashboard)
- [Published GitHub Security Advisory](https://github.com/laradashboard/laradashboard/security/advisories/GHSA-9gxw-qpx8-x9c7)
- [CWE-79](https://cwe.mitre.org/data/definitions/79.html)
- [CWE-434](https://cwe.mitre.org/data/definitions/434.html)

## Legal and safety notice

Use this material only on systems you own or are explicitly authorized to test. The PoCs are intended for isolated, disposable lab environments.
