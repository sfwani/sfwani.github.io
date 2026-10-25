## Summary

The self-hosting stack for trigger.dev v4 ships a `.env.example` at `hosting/docker/.env.example` that contains real, working secret values rather than placeholders. Operators who copy it to `.env` (the documented path) inherit a publicly known `MAGIC_LINK_SECRET`, `ENCRYPTION_KEY`, `SESSION_SECRET`, and default database, Redis, ClickHouse and object store credentials. I verified a full unauthenticated chain against a live default instance: forge a magic link, land an authenticated session with no email delivery, and reach every infrastructure service with its shipped password.

## Where it lives

The secrets are committed in plaintext. These are not throwaway placeholders, they are the values the compose stack actually loads:

<!-- bug: MAGIC_LINK_SECRET=44da78b7bbb0dfe709cf38931d25dcdd :: shipped magic link secret lets anyone mint login tokens -->
<!-- bug: ENCRYPTION_KEY=f686147ab967943ebbe9ed3b496e465a :: published key decrypts every stored tenant secret -->
```bash
SESSION_SECRET=2818143646516f6fffd707b36f334bbb
MAGIC_LINK_SECRET=44da78b7bbb0dfe709cf38931d25dcdd
ENCRYPTION_KEY=f686147ab967943ebbe9ed3b496e465a
MANAGED_WORKER_SECRET=447c29678f9eaf289e9c4b70d3dd8a7f
...
POSTGRES_PASSWORD=unsafe-postgres-pw
DATABASE_URL=postgresql://postgres:unsafe-postgres-pw@postgres:5432/main?...
CLICKHOUSE_URL=http://default:password@clickhouse:8123?secure=false
OBJECT_STORE_ACCESS_KEY_ID=admin
OBJECT_STORE_SECRET_ACCESS_KEY=very-safe-password
```

The `MAGIC_LINK_SECRET` is the keystone. trigger.dev's passwordless login encrypts the magic link token with this secret, so knowing it lets anyone mint a valid login token for any email without ever receiving the email. My PoC reproduces the exact token the server expects:

```javascript
const MAGIC_LINK_SECRET = "44da78b7bbb0dfe709cf38931d25dcdd";
const payload = JSON.stringify({ e: email, c: Date.now() });
const encrypted = CryptoJS.AES.encrypt(payload, MAGIC_LINK_SECRET).toString();
// GET /magic?token=<encodeURIComponent(encrypted)>  -> session cookie, user auto-created
```

## Impact

**Unauthenticated session forging.** Visiting the forged `/magic?token=...` URL auto-creates the account and sets a session cookie. Against a live default instance the chain produced a working session (`HTTP 302 -> /orgs/new`) with no interaction from any real user.

**Full infrastructure access.** With the webapp network reachable (the default stack places runner containers on it), the shipped credentials opened every backend service directly: PostgreSQL via `postgres:unsafe-postgres-pw` with all tenant tables readable (`User`, `SecretStore`, `PersonalAccessToken`, `EnvironmentVariable`, `RuntimeEnvironment`, `OrgMember`), Redis answering `PONG` with no auth, and ClickHouse returning its version via `default:password`.

**Secret decryption.** `ENCRYPTION_KEY=f686147ab967943ebbe9ed3b496e465a` is the key used to encrypt stored secrets, so the `SecretStore` contents an attacker reads from PostgreSQL are decryptable with the same published value. The breach is not limited to metadata, it extends to the credentials trigger.dev holds on behalf of every tenant.

Taken together this is a complete, cross tenant compromise of any self hosted instance left on the defaults, reachable by an unauthenticated remote attacker.

## Fix

Stop shipping live secrets in a file operators are told to copy. The stack should generate unique secrets at deploy time through a bootstrap step, and the webapp should refuse to start when `MAGIC_LINK_SECRET`, `ENCRYPTION_KEY` or `SESSION_SECRET` match a known published default or are empty. Enable Redis authentication with an auto generated password, give the task runners an isolated network that can reach only the supervisor workload API, and require real credentials on the infrastructure services rather than the committed ones.
