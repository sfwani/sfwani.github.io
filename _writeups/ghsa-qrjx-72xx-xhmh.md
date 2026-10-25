## Summary

AG2's beta `DiskKnowledgeStore` maps agent-supplied virtual paths onto real files under a root directory, and tries to keep every operation inside that root with a single containment check. The check compares the resolved path against the root with `str.startswith`, which is a classic path-confinement anti-pattern: a sibling directory whose name merely shares a prefix with the root satisfies the test. So a path like `../store_evil/secret.txt` resolves outside the intended root yet passes validation, and every read, write, list, delete, and append in the store inherits the hole.

## Where it lives

The containment logic is one line in `autogen/beta/knowledge/disk.py`, inside `_resolve()`:

<!-- bug: if not str(resolved).startswith(str(self._root.resolve())): :: string prefix check lets prefix-sharing sibling directories through -->
```python
def _resolve(self, path: str) -> Path:
    """Map virtual path to real filesystem path."""
    normalized = _normalize(path).lstrip("/")
    resolved = (self._root / normalized).resolve() if normalized else self._root.resolve()
    if not str(resolved).startswith(str(self._root.resolve())):
        raise ValueError(f"Path traversal blocked: {path}")
    return resolved
```

`_resolve()` is the single gate for the whole store: `read`, `write`, `list`, `delete`, `exists`, `append`, `read_range`, and `on_change` all route their path argument through it. Whatever `_resolve()` lets out, those methods will operate on.

The rest of the codebase already knows the right way to do this. `is_relative_to()` is the correct, prefix-safe containment check, and it is used elsewhere for exactly this purpose (for example `filesystem.py:246` and `apply_patch_tool.py:245`), making `disk.py` the outlier.

## Impact

With `root="/data/store"`, the virtual path `../store_evil/secret.txt` resolves to `/data/store_evil/secret.txt`. The guard asks whether `"/data/store_evil/secret.txt".startswith("/data/store")`, which is `True`, so the traversal is "blocked" only in name. The caller then reads, overwrites, or deletes a file in a directory that was never meant to be reachable.

Because `_resolve()` backs every operation, the primitive is read and write and delete, not read alone. An attacker who influences the path an agent passes to the knowledge store can exfiltrate files from, or clobber files in, any sibling directory sharing the root's name prefix, escaping the sandbox the store is supposed to provide.

I verified this against a faithful copy of the vulnerable `_resolve()`: the traversal path was accepted, resolved into a sibling directory, and read back a planted secret file, while the `is_relative_to()` version rejected the same path.

## Fix

Replace the `startswith` test with a true ancestor check:

<!-- fix: if not resolved.is_relative_to(self._root.resolve()): :: compares path components instead of string prefixes -->
```python
if not resolved.is_relative_to(self._root.resolve()):
    raise ValueError(f"Path traversal blocked: {path}")
```

`Path.is_relative_to` compares path components rather than string prefixes, so `/data/store_evil` is correctly recognized as outside `/data/store`. This matches what the project already does in `filesystem.py` and `apply_patch_tool.py`.
