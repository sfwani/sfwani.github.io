---
title: "GHSA-qrjx-72xx-xhmh"
heading: "GHSA-qrjx-72xx-xhmh"
role: "Path Traversal in DiskKnowledgeStore via Incorrect startswith Path Containment Check"
seo_title: "GHSA-qrjx-72xx-xhmh: Path Traversal in DiskKnowledgeStore via Incorrect startswith Path Containment… - Sanaan Fayaz Wani"
ghsa_id: "GHSA-qrjx-72xx-xhmh"
cve_id: ""
published_at: "2026-09-25"
permalink: /advisories/ghsa-qrjx-72xx-xhmh/
layout: c2
description: "Path Traversal in DiskKnowledgeStore via Incorrect startswith Path Containment Check"
comments: false
last_modified_at: 2026-10-22T01:22:55+00:00
---
<section class="sec g" id="writeup" aria-labelledby="h-writeup">
  <div class="sec-head">
    <p class="idx idx--none">—</p>
    <h2 id="h-writeup">GHSA-qrjx-72xx-xhmh</h2>
    <p class="sec-sub">Published, fixed and credited. Root cause, the vulnerable code, reproduction and the fix, as published in the advisory itself.</p>
  </div>
  <div class="col-body prose" markdown="1">

| | |
|:--|:--|
| Advisory | [GHSA-qrjx-72xx-xhmh](https://github.com/ag2ai/ag2/security/advisories/GHSA-qrjx-72xx-xhmh) |
| CVE | not assigned |
| Severity | High (7.5) |
| CVSS vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| CWE | CWE-22 (Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')) |
| Published | 2026-09-25 |

GitHub published this advisory as High with no CVSS score and no vector, in v3 or v4. The score and vector above are my own assessment of the finding as published.

### Affected versions

| Package | Ecosystem | Vulnerable | Fixed in |
|:--|:--|:--|:--|
| `ag2` | pip | >= 0.12.2, < 1.1.0 | n/a |
| `autogen` | pip | >= 0.12.2, <= 0.14.1 | n/a |

## Summary

`DiskKnowledgeStore._resolve()` uses `str(resolved).startswith(str(self._root.resolve()))` to validate that file paths stay within the root directory. This is a well-known anti-pattern: a sibling directory whose name shares a prefix with the root directory bypasses the check, allowing read, write, and delete operations outside the intended root.

## Affected File

- `autogen/beta/knowledge/disk.py:151`

## Steps to Reproduce

```python
import tempfile
from pathlib import Path

# Setup: create root and sibling with shared prefix
tmpdir = tempfile.mkdtemp()
root = Path(tmpdir) / "store"
root.mkdir()
evil = Path(tmpdir) / "store_evil"
evil.mkdir()
(evil / "secret.txt").write_text("API_KEY=sk-1234567890")

# The vulnerable check
traversal_path = "../store_evil/secret.txt"
resolved = (root / traversal_path).resolve()

# startswith check PASSES (bug)
print(str(resolved).startswith(str(root.resolve())))
# True -- because "/tmp/.../store_evil/secret.txt".startswith("/tmp/.../store")

# is_relative_to check CORRECTLY BLOCKS
print(resolved.is_relative_to(root.resolve()))
# False
```

### Standalone Verification Script

```python
import tempfile, asyncio
from pathlib import Path

def _normalize(path):
    return path.replace("\\", "/")

def _resolve_vulnerable(root, path):
    normalized = _normalize(path).lstrip("/")
    resolved = (root / normalized).resolve() if normalized else root.resolve()
    if not str(resolved).startswith(str(root.resolve())):
        raise ValueError(f"Path traversal blocked: {path}")
    return resolved

tmpdir = tempfile.mkdtemp()
root = Path(tmpdir) / "store"
root.mkdir()
evil = Path(tmpdir) / "store_evil"
evil.mkdir()
(evil / "secret.txt").write_text("SENSITIVE DATA")

try:
    result = _resolve_vulnerable(root, "../store_evil/secret.txt")
    print(f"BYPASSED: {result}")
    print(f"Content: {result.read_text()}")
except ValueError as e:
    print(f"Blocked: {e}")
```

## Root Cause

`disk.py:151`:
```python
if not str(resolved).startswith(str(self._root.resolve())):
    raise ValueError(f"Path traversal blocked: {path}")
```

When `root` resolves to `/data/store`, the path `../store_evil/secret.txt` resolves to `/data/store_evil/secret.txt`. The string `"/data/store_evil/secret.txt"` starts with `"/data/store"`, so the check passes.

The correct approach (used elsewhere in the AG2 codebase at `filesystem.py:246` and `apply_patch_tool.py:245`) is:
```python
if not resolved.is_relative_to(self._root.resolve()):
    raise ValueError(f"Path traversal blocked: {path}")
```

## Impact

An LLM agent using the knowledge tool (exposed via `_make_knowledge_tool` at `agent.py:1331`) can read, write, and delete files in sibling directories that share a prefix with the knowledge store root. This can lead to unauthorized data access or modification depending on the filesystem layout.

## Suggested Fix

```python
# Before (vulnerable):
if not str(resolved).startswith(str(self._root.resolve())):

# After (fixed):
if not resolved.is_relative_to(self._root.resolve()):
```

## CVSS

CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N (7.5 High)

## About this writeup

Sanaan Fayaz Wani (GitHub [`sfwani`](https://github.com/sfwani)) reported this vulnerability to the `ag2` maintainers under coordinated disclosure and is credited as a reporter in [GHSA-qrjx-72xx-xhmh](https://github.com/ag2ai/ag2/security/advisories/GHSA-qrjx-72xx-xhmh), published 2026-09-25.

All published findings: [advisory index](/advisories/).


  </div>
</section>
