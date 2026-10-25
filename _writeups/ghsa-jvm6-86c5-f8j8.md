## Summary

Teable ships its own SSRF guard (`createSsrfSafeFetch` / `safeFetch`) and wires it into the import and attachment paths. The AI provider path does not use it. `POST /api/space/:spaceId/test-llm` builds an LLM provider from a fully user-controlled `baseUrl` and makes the server issue an outbound request to it, through a plain global `fetch` with no host or scheme allowlist. Any authenticated user can reach the endpoint, and the error responses distinguish open ports from closed ones, giving a server-side internal port-scan and reachability oracle against hosts the attacker cannot reach directly. This is a server-side request forgery (CWE-918).

## Where it lives

The route carries `@Permissions('space|update')`, which sounds privileged but is held by every user on a space they create: `POST /api/space` needs only `space|create` (a default capability), and the creator becomes `Role.Owner`, which has `space|update`. The handler ignores the path `spaceId` entirely and acts on the request body, so an attacker's own throwaway space satisfies the gate. `baseUrl` is validated only as `z.url()`, with no host or scheme restriction.

`testLLM` in `apps/nestjs-backend/src/features/setting/open-api/setting-open-api.service.ts` takes `baseUrl` straight from the request body, builds the provider, and calls `generateText`, which performs the outbound request:

<!-- bug: baseURL: baseUrl, apiKey :: user supplied baseUrl becomes the provider endpoint -->
```ts
async testLLM(testLLMRo: ITestLLMRo): Promise<ITestLLMVo> {
  const { type, baseUrl, apiKey, models, ... } = testLLMRo;
  ...
  const providerOptions = getAdaptedProviderOptions(type, { name: model, baseURL: baseUrl, apiKey });
  const modelProvider = provider({ ...providerOptions } as never) as OpenAIProvider;
```

The provider fetch is defined in `apps/nestjs-backend/src/features/ai/util.ts`, and it is the unguarded global `fetch`, not `safeFetch`:

<!-- bug: const response = await fetch(input, init); :: plain global fetch with no SSRF guard -->
```ts
const createFixingFetch = (): typeof fetch => {
  return async (input, init) => {
    const response = await fetch(input, init);   // plain global fetch, no SSRF guard
    ...
```

The other provider factories in `modelProviders` use the AI SDK's own default fetch, also unfiltered. None of them route through the `safeFetch` that imports and external-DB connections already enforce.

## Impact

I confirmed the oracle live against `ghcr.io/teableio/teable:latest` as a non-admin user, probing docker-network services the attacker has no direct route to:

```
baseUrl teable-db:5432    (internal Postgres, OPEN) -> "Cannot connect to API: other side closed"  (connected)
baseUrl teable-db:1       (CLOSED port)             -> "Cannot connect to API: bad port"
baseUrl teable-cache:6379 (internal Redis, OPEN)    -> "other side closed"                         (connected)
```

The distinct error per target proves the server performed the attacker-directed outbound connection and reflected the result. An unprivileged tenant in a multi-tenant deployment can enumerate and fingerprint internal services, databases, caches and cloud metadata endpoints that are otherwise unreachable from its network position, and an endpoint returning OpenAI-shaped JSON reflects its body back to the caller.

## Fix

Route the AI provider path through the existing guard: pass a `createSsrfSafeFetch()`-based fetch into every entry of `modelProviders` (not only the OpenAI-compatible wrapper) and into `createGateway`, or install it as a global undici dispatcher. Restrict `baseUrl` to public https hosts via an allowlist, and return a generic failure message instead of the raw connection error so the port oracle disappears.
