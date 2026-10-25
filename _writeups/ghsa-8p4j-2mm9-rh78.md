## Summary

Tracecat's `core.cases.upload_attachment_from_url` registry action takes a URL from an authenticated workflow author, fetches it with `httpx`, and stores the full response body as a case attachment the author can read back. There is no URL validation of any kind: no scheme allowlist, no private or link local IP blocking, no DNS rebinding guard. That makes it a clean full read SSRF, where the response is handed straight back to the attacker rather than merely triggered blind.

## Where it lives

The action is defined in `packages/tracecat-registry/tracecat_registry/core/cases.py`. The `url` parameter is a plain `str`, and the fetch runs with no checks between input and request:

<!-- bug: response = await client.get(url, headers=headers) :: fetches the author supplied url with no validation -->
<!-- bug: return await _upload_attachment(case_id, file_name, content, content_type) :: stores the full response body as a readable attachment -->
```python
async def upload_attachment_from_url(
    case_id: Annotated[str, Doc("The ID of the case to attach the file to.")],
    url: Annotated[str, Doc("The URL of the file to upload.")],
    headers: Annotated[dict[str, str] | None, Doc("The headers to use when downloading the file.")] = None,
    file_name: Annotated[str | None, Doc("...")] = None,
) -> types.CaseAttachmentRead:
    """Upload a file attachment to a case from a URL."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        content = response.content
        content_type = response.headers.get("Content-Type")
    ...
    return await _upload_attachment(case_id, file_name, content, content_type)
```

Two details sharpen it. The `headers` parameter is attacker controlled, so a request can carry the `X-aws-ec2-metadata-token` header needed for IMDSv2 token based metadata access. And `content` is persisted through `_upload_attachment`, so whatever the internal service returns becomes a downloadable attachment on the case. The same gap in reflected form sits in the `core.http_request` family in `core/http.py`, where Pydantic `HttpUrl` validates URL shape but never rejects private ranges.

## Impact

My own findings pair this with Tracecat's default of `TRACECAT__DISABLE_NSJAIL=true`, which ships across `.env.example`, both executor services in `docker-compose.yml`, and `tracecat/config.py`. With the sandbox off the executor has no network isolation, so the SSRF reaches everything on the Docker network. I live validated reachability from the executor to Redis (received `+PONG`), PostgreSQL (TCP connect on 5432), and MinIO (HTTP 200). On a cloud deployment the same action reaches `169.254.169.254` for IAM credential theft, with the custom `headers` covering IMDSv2. Because the full body is stored and retrievable, this is exfiltration, not a pingback. One mitigating note: `httpx` does not follow redirects by default, so redirect based pivots do not work out of the box.

## Fix

Validate before the request, not just the format. Resolve the hostname, reject any resolved address inside `127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16`, `::1/128`, `fc00::/7` and `fe80::/10`, and restrict the scheme to `http` and `https`. Apply that same check in `upload_attachment_from_url` and across the `core.http_request` and `core.http_paginate` actions, since the paginator can emit arbitrary follow up URLs that skip even the `HttpUrl` format check.
