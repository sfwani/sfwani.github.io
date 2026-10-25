## Summary

AG2's beta `LocalShellEnvironment` (formerly Microsoft AutoGen) advertises three ways to constrain what an agent can run in a shell: an `allowed` whitelist, a `blocked` blacklist, and a `readonly` mode backed by a curated `READONLY_COMMANDS` list. Every one of them is a prefix check applied to the raw command string, and the command is then handed to `subprocess.run(..., shell=True)`. Because the OS shell, not the filter, decides where one command ends and the next begins, any allowed prefix can be followed by `;`, `&&`, `|`, or `$(...)` to run arbitrary commands. The restriction is cosmetic.

## Where it lives

The filter, in `autogen/beta/tools/shell/environment/base.py`, only looks at how the string begins:

<!-- bug: if not stripped.startswith(pattern): :: only checks how the command string begins -->
```python
def matches(pattern: str, command: str) -> bool:
    stripped = command.strip()
    if not stripped.startswith(pattern):
        return False
    rest = stripped[len(pattern):]
    return rest == "" or rest[0] == " "
```

`LocalShellEnvironment.run()` in `environment/local.py` runs whatever passes that check through a full shell:

<!-- bug: shell=True, :: runs the filtered string through a full shell -->
```python
if self._allowed is not None and not any(matches(p, command) for p in self._allowed):
    return f"Command not allowed: {command!r}"
...
result = subprocess.run(
    command,
    shell=True,
    cwd=self._workdir,
    ...
)
```

The code already knows. The comment above `READONLY_COMMANDS` in `base.py` calls the list "best-effort" and notes that "`echo` can still redirect output (`echo x > file`), because `shell=True` processing happens inside the OS shell after our prefix check." That caveat understates it: the same mechanism allows arbitrary execution, not just redirection.

## Impact

The security boundary the API promises does not exist. A caller who trusts `readonly=True`, or an allow list, to pen in an LLM-driven or otherwise untrusted command string gets full OS command execution under the process's privileges instead.

**readonly / allow list bypass.** `echo x; id` begins with the allowed `echo`, so it passes, and the shell then runs `id`. `git --version && id` passes an `allowed=["git"]` gate the same way. `cat /dev/null | id` passes `readonly=True` and pipes into an arbitrary program.

**blocklist bypass.** `blocked=["rm", "curl"]` is evaded by `echo $(rm -rf /)`, which never starts with a blocked prefix yet executes `rm` inside a subshell.

I confirmed each of these against a faithful copy of `matches()` and `READONLY_COMMANDS` driving a real `subprocess.run(..., shell=True)`: in every case the filter returned "allowed" and the injected `id` produced `uid=` output.

## Fix

Stop treating a prefix of a shell string as a security boundary. Either tokenize with `shlex.split()` and execute argv-style with `shell=False`, validating the resolved program against the allow list, or run inside a real sandbox. If `shell=True` must stay, reject any command containing shell metacharacters (`;`, `&`, `|`, `$`, backticks, redirections, newlines) before it reaches `subprocess.run`, and document that the prefix lists are not a privilege boundary.
