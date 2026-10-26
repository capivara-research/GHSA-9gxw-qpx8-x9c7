# GHSA-9gxw-qpx8-x9c7 — Stored XSS no LaraDashboard via upload de SVG

> CVE atribuída: **[CVE-2026-90931](https://www.cve.org/CVERecord?id=CVE-2026-90931)**. O repositório CVE mantido está em [capivara-research/CVE-2026-90931](https://github.com/capivara-research/CVE-2026-90931).

[English](README.md) · [Advisory oficial](https://github.com/laradashboard/laradashboard/security/advisories/GHSA-9gxw-qpx8-x9c7)

Evidência pública e material seguro de reprodução local para stored XSS na biblioteca de mídia do LaraDashboard.

## Resumo técnico

| Campo | Valor |
|---|---|
| Produto | LaraDashboard |
| Versões afetadas | `>= 0.9.0, <= 1.2.2` |
| Revisão testada | `9dc1335835701651aef3adcb3e885acecb32402c` |
| CWE | CWE-79, CWE-434 |
| Severidade | Média — CVSS 3.1 `5.4` |
| Permissão necessária | `media.create` |
| Advisory | `GHSA-9gxw-qpx8-x9c7` |

Em produção, o pipeline de upload aceita SVG sem sanitizar scripts ou event handlers. O arquivo é armazenado na origem da aplicação e servido inline como `image/svg+xml`. Assim, um usuário de conteúdo com apenas `media.create` consegue armazenar JavaScript que será executado quando outro usuário abrir o SVG.

## PoC

O diretório [`poc/`](poc/) contém um verificador estático, um SVG marcador inofensivo e um helper de upload limitado a loopback. O payload apenas altera texto visível no próprio SVG e define o fragmento da URL; não lê cookies, tokens ou dados da aplicação.

## Correção recomendada

- sanitizar SVG com uma biblioteca mantida;
- alternativamente rejeitar SVG ou servi-lo como download;
- hospedar mídia controlada pelo usuário em origem separada;
- aplicar validação MIME também em produção;
- trocar blocklists de extensões por allowlist;
- usar CSP e `X-Content-Type-Options: nosniff` como defesa adicional.

## Divulgação

Reportado por [capivara-research](https://github.com/capivara-research) via GitHub Private Vulnerability Reporting e publicado pelo projeto em 30/08/2026.

## Aviso legal

Use somente em sistemas próprios ou com autorização explícita. O material destina-se a laboratórios locais e descartáveis.
