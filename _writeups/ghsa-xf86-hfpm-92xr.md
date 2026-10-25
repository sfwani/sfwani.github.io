## Summary

Directus (versions `<= 11.17.4`) ships two different ways to call its AI tools: the MCP server and the AI chat route. The MCP server guards the five tools marked `admin: true` (`collections`, `fields`, `relations`, `flows`, `operations`), but the chat route does not. Any authenticated user with `app_access` can ask the chat endpoint to run admin tools the MCP path would refuse them, so the two entry points disagree on who is allowed to do what.

## Where it lives

The chat route converts each requested tool into an AI SDK tool in `api/src/ai/chat/utils/chat-request-tool-to-ai-sdk-tool.ts`. At lines 21 to 26 it looks the tool up by name from `ALL_TOOLS` and wires it in, but it never reads `directusTool.admin`:

<!-- bug: // no check of directusTool.admin anywhere here :: the admin flag is never read on this path -->
```typescript
// api/src/ai/chat/utils/chat-request-tool-to-ai-sdk-tool.ts:21-26
// looks up the tool by name from ALL_TOOLS
// and builds the AI SDK tool
// no check of directusTool.admin anywhere here
```

The MCP server, by contrast, enforces the flag in both the listing and the execution path:

```typescript
// api/src/ai/mcp/server.ts:200  (listing)
if (req.accountability?.admin !== true && tool.admin === true) continue;

// api/src/ai/mcp/server.ts:223  (execution)
if (req.accountability?.admin !== true && tool.admin === true)
    throw new ForbiddenError(...);
```

So the same tool definitions carry an `admin: true` flag that one dispatcher honors and the other ignores. The flag is the intended control; the chat route simply skips it.

## Impact

This is an incorrect authorization flaw (CWE-863). A non-admin user who holds `app_access` can drive the chat route to invoke `collections`, `fields`, `relations`, `flows`, and `operations`, the schema and automation tooling that Directus reserves for admins. The MCP server denies these to non-admins, which confirms the intended trust boundary and makes the chat route's omission a genuine bypass rather than a design choice. A low privilege `app_access` user, with no further interaction, gains read access to the schema and flow metadata that should be admin-only. The maintainers scored the impact as limited disclosure with no integrity impact (`C:L/I:N`), and because the runtime run below was not completed I do not claim any write effect beyond that.

I want to be precise about what I verified. The missing check is confirmed at the code level by comparing the two dispatchers line for line. The live end-to-end run was not completed because exercising the chat route needs a configured AI provider key, so I did not capture a runtime transcript for this one. The authorization gap in the source is unambiguous; the runtime proof is the piece I flag as outstanding.

## Fix

Mirror the MCP server's guard in the chat route. After the tool lookup at line 26, reject admin tools for non-admin callers before the tool is ever handed to the model:

<!-- fix: if (directusTool.admin && accountability.admin !== true) { :: rejects admin tools for non-admin callers -->
```typescript
if (directusTool.admin && accountability.admin !== true) {
    throw new ForbiddenError({
        reason: 'You must be an admin to access this tool',
    });
}
```

Better still, both dispatchers should share one admin-enforcement helper so the `admin` flag cannot be honored in one place and forgotten in another.
