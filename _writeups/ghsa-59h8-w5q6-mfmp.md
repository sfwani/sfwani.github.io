## Summary

trigger.dev's realtime streams let a running task push data (logs, AI token chunks, progress) to clients subscribed to a run. The POST ingest handler at `apps/webapp/app/routes/realtime.v1.streams.$runId.$streamId.ts` carries no authentication at all. Anyone who can reach the webapp and knows a run's `friendlyId` can inject arbitrary bytes into that run's realtime stream, and those bytes are delivered to every subscriber as if they came from the task itself.

## Where it lives

The `action` handler is explicitly a plain Remix action with no auth wrapper. The comment on the function says the quiet part out loud:

<!-- bug: export async function action({ request, params }: ActionFunctionArgs) { :: plain action with no authentication wrapper -->
<!-- bug: friendlyId: runId, :: looks up the run by id with no environment scoping -->
```typescript
// Plain action for backwards compatibility with older clients that don't send auth headers
export async function action({ request, params }: ActionFunctionArgs) {
  const parsedParams = ParamsSchema.safeParse(params);
  ...
  const { runId, streamId } = parsedParams.data;

  // Look up the run without environment scoping for backwards compatibility
  const run = await $replica.taskRun.findFirst({
    where: {
      friendlyId: runId,
    },
    ...
  });
```

Compare this with the GET `loader` in the same file, which is built through `createLoaderApiRoute` with `allowJWT`, a `findResource` that scopes on `runtimeEnvironmentId: auth.environment.id`, and an `authorization` block. The read path is authenticated and tenant scoped. The write path is not. The lookup deliberately drops environment scoping, so the only thing standing between an attacker and a stream is knowledge of the `friendlyId`. The handler then feeds the raw request body straight into the stream:

<!-- bug: request.body, :: raw request body goes straight into the stream -->
```typescript
return realtimeStream.ingestData(
  request.body,
  run.friendlyId,
  streamId,
  clientId,
  resumeFromChunkNumber
);
```

The `friendlyId` is not a secret. It is a `run_` prefix plus a nanoid (`packages/core/src/v3/isomorphic/friendlyId.ts`), and it surfaces in dashboard URLs, API responses, SSE payloads and logs. It behaves as a bearer identifier, not a credential, so any party that has ever seen the ID can write to the stream.

## Impact

**Stream poisoning and spoofing.** An unauthenticated attacker who learns a run's `friendlyId` POSTs crafted chunks into `/realtime/v1/streams/:runId/:streamId`. Subscribers, including dashboard viewers and `@trigger.dev/react-hooks` clients, receive the injected content as legitimate task output. For AI workloads that stream model tokens to end users, this lets an attacker rewrite what the user sees mid run, forge completion data, or splice misleading or malicious content into the response.

**Cross environment reach.** Because the lookup drops environment scoping, the injection is not confined to the attacker's own tenant. Any run whose ID is known can be targeted.

## Fix

Remove the unauthenticated action and require the same authentication the GET loader already uses. Route the write path through an authenticated API builder, scope the `taskRun` lookup on the caller's `runtimeEnvironmentId`, and verify the caller owns the run before `ingestData` is reached. If older clients genuinely cannot send auth headers, gate that compatibility behind an explicit opt in rather than leaving an open write endpoint for every run in the system.
