## Summary

The trigger.dev supervisor runs a workload server (default port 8020, bound to `0.0.0.0`) that drives the entire run lifecycle: starting attempts, completing them, heartbeating, suspending, continuing, and dequeuing work. Every HTTP route on this server in `apps/supervisor/src/workloadServer/index.ts` executes with zero authentication, and the WebSocket namespace only checks that two headers are present, never that they carry a secret. Any party that can reach the port can manipulate any run by its `friendlyId`.

## Where it lives

The server is constructed to listen on all interfaces by default:

<!-- bug: const host = opts.host ?? "0.0.0.0"; :: listens on all interfaces by default -->
```typescript
constructor(opts: WorkloadServerOptions) {
  super();
  const host = opts.host ?? "0.0.0.0";
  const port = opts.port;
  ...
```

Each lifecycle route takes a `runFriendlyId` and a `snapshotFriendlyId` from the URL and immediately calls the worker client. There is no bearer check, no shared secret, no mutual TLS. For example, the attempt start route:

<!-- bug: const startResponse = await this.workerClient.startRunAttempt( :: calls the worker client with no credential check -->
<!-- bug: this.runnerIdFromRequest(req) :: runner id comes from an unverified request header -->
```typescript
.route(
  "/api/v1/workload-actions/runs/:runFriendlyId/snapshots/:snapshotFriendlyId/attempts/start",
  "POST",
  {
    paramsSchema: WorkloadActionParams,
    bodySchema: WorkloadRunAttemptStartRequestBody,
    handler: async ({ req, reply, params, body }) => {
      const startResponse = await this.workerClient.startRunAttempt(
        params.runFriendlyId,
        params.snapshotFriendlyId,
        body,
        this.runnerIdFromRequest(req)
      );
```

The same shape repeats for `/attempts/complete`, `/heartbeat`, `/suspend`, `/continue`, `/snapshots/since`, and `/deployments/:deploymentId/dequeue`. The only identity signal is a `runnerId` pulled from a request header, used for bookkeeping, not verified against anything.

The WebSocket side is no better. The namespace middleware only copies two headers into socket data and disconnects if they are missing:

<!-- bug: this.logger.debug("[WS] auth success", socket.data); :: header presence alone counts as auth success -->
```typescript
setSocketDataFromHeader("deploymentId", WORKLOAD_HEADERS.DEPLOYMENT_ID);
setSocketDataFromHeader("runnerId", WORKLOAD_HEADERS.RUNNER_ID);
...
this.logger.debug("[WS] auth success", socket.data);
```

Presence of a header is treated as authentication. Both values are attacker suppliable.

## Impact

**Run lifecycle hijack.** An attacker on the network forges requests for any known `runFriendlyId` and `snapshotFriendlyId` pair. They can mark attempts complete with attacker chosen results, force completion or failure, spoof heartbeats to keep dead runs alive or let live ones expire, and trigger suspend and continue transitions out of order.

**Work theft and injection.** The dequeue route hands out queued work for a deployment to anyone who asks, so an attacker can pull pending runs intended for legitimate runners. Combined with the complete route, this lets an attacker intercept a run and return forged output as the task result.

This is a direct consequence of the supervisor trusting its network. On the default self-hosted stack the runner containers share that network, so the exposure is reachable, not theoretical.

## Fix

Require a real credential on every workload route and on the WebSocket handshake. The deployment already provisions a `MANAGED_WORKER_SECRET`; verify it (or a per runner token) on each request instead of merely reading the `runnerId` header. Stop treating header presence as authentication in the socket middleware, and bind the server to a private interface rather than `0.0.0.0` unless an authenticated gateway sits in front of it.
