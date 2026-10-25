## Summary

Omnigent (Databricks) runs agent tool calls inside a bubblewrap jail, and its own policies present that jail as the real security boundary. I found that five shipped executors grant the host `/tmp` directory as a sandbox write root. Because the bubblewrap backend mounts a private `--tmpfs /tmp` first and only then binds the write roots, the later bind of the host `/tmp` overmounts the private tmpfs and makes the real host `/tmp` writable from inside the sandbox. The host executed launcher script that omnigent writes into that same directory then becomes an overwrite target, which hands a sandboxed agent code execution on the host. Verified live against `omnigent==0.9.0` from PyPI.

## Where it lives

The `/tmp` grant sits right next to the launcher creation in each executor. From `omnigent/inner/goose_executor.py` (the same pattern appears in `pi_executor.py`, `qwen_executor.py`, `kimi_executor.py` and `acp_executor.py`):

<!-- bug: Path("/tmp"), :: grants the host /tmp as a sandbox write root -->
```python
sandbox = with_additional_write_roots(
    sandbox,
    [
        Path.home() / ".config" / "goose",
        Path.home() / ".local" / "share" / "goose",
        Path("/tmp"),
    ],
)
...
return create_exec_launcher(self._goose_path, sandbox)
```

`create_exec_launcher` in `omnigent/inner/sandbox.py` mints that launcher world executable:

<!-- bug: fd, path = tempfile.mkstemp(prefix="omnigent-sandbox-", suffix=".py") :: writes the host launcher into the shared /tmp -->
<!-- bug: os.chmod(path, 0o755) :: launcher is 0755, owned by the uid the sandbox shares -->
```python
fd, path = tempfile.mkstemp(prefix="omnigent-sandbox-", suffix=".py")  # :1112
...
os.chmod(path, 0o755)                                                  # :1129
```

The launcher runs on the host and only then re-execs into the wrap. The code comment at `sandbox.py:1006` states the exact assumption the `/tmp` grant breaks:

<!-- bug: bwrap mounts ``/tmp`` as a fresh tmpfs :: the assumption the /tmp grant breaks -->
```python
# bwrap mounts ``/tmp`` as a fresh tmpfs, so the host's
# ``/tmp/omnigent-sandbox-*.py`` written by
# ``create_exec_launcher`` is invisible inside the wrap.
```

`bwrap_sandbox.py` emits `--tmpfs /tmp` and then `--bind-try /tmp /tmp`; later bwrap ops win, so the host `/tmp` replaces the tmpfs. It also emits no `--unshare-user` and no `--uid`, so the sandboxed process shares the uid that owns the 0755 launcher and may overwrite it. Root is not required.

## Impact

This crosses the sandbox to host boundary, the one control omnigent names as its security boundary (`policies/builtins/safety.py` ships `enforce_sandbox`; the `blast_radius` docstring disclaims itself and points at sandboxing). The default is not narrowly opt in: `OSEnvSandboxSpec.type` defaults to `"linux_bwrap"`, so any agent whose `os_env` does not explicitly set `type: none` gets the affected sandbox.

My controlled PoC isolated the grant as the cause. With cwd write root `/work` and no `/tmp` grant, a sandboxed write failed and the host saw nothing. With `/tmp` granted the identical write succeeded and the host file appeared:

```
CONTROL  (no /tmp grant): sandboxed write rc=2   HOST sees file: False
AFFECTED (/tmp granted):  sandboxed write rc=0   HOST sees file: True
```

End to end, driven by the real executor, I enumerated the launcher from inside the sandbox, overwrote it, and the host side launcher then ran my content (`ATTACKER_CODE_ON_HOST`) as the host user, reproduced even with an unprivileged `--uid 65534`. `pi_executor` is deterministic: it mints the path once in `__init__` and re-execs it for every session and RPC restart, so no race is needed. The agent gains the host's filesystem, environment and credentials.

## Fix

Stop writing the host executed launcher into a directory the sandbox can reach. Place it under a `0700` directory outside every write root and chmod it `0700` rather than `0755`:

<!-- fix: launcher_dir = _private_launcher_dir() :: places the launcher in a private 0700 directory -->
<!-- fix: os.chmod(path, 0o700) :: sets the launcher mode to 0700 instead of 0755 -->
```python
launcher_dir = _private_launcher_dir()   # 0700, outside every write root
fd, path = tempfile.mkstemp(prefix="omnigent-sandbox-", suffix=".py", dir=launcher_dir)
...
os.chmod(path, 0o700)
```

Then narrow the `/tmp` grants to a per session subdirectory such as `/tmp/omnigent-<uuid>`, and have `with_additional_write_roots` reject or warn on any root that is an ancestor of the launcher directory so this class of mistake fails loudly. CWE-668 with CWE-732.
