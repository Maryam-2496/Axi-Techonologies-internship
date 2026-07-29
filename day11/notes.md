# Day 11: Caching & Performance Optimization with Redis

## What I did
- Installed Memurai (Windows-native, Redis-protocol-compatible server) since Docker/WSL weren't available
- Connected Flask to Redis using the redis-py client, verified with a successful ping
- Practiced core Redis commands directly in memurai-cli: SET, GET, DEL, and TTL expiration (EX)
- Implemented the Cache-Aside pattern on GET /auth/me: check Redis first, fall back to the database on a cache miss, then store the result in Redis with a 5-minute TTL
- Added cache invalidation: PUT /auth/me and DELETE /auth/me now delete the corresponding Redis key immediately after the database is updated, so stale data is never served
- Verified caching and invalidation directly via Redis (KEYS user:*, GET user:<id>) rather than relying only on response-time comparisons

## What I learned
- Memurai is a Windows-native, Redis-protocol-compatible alternative to running real Redis via Docker/WSL, and works identically with redis-py and all Redis commands
- The Cache-Aside pattern means the application checks the cache first and only queries the database on a miss, then populates the cache for next time
- TTL (Time-To-Live) lets Redis automatically expire and delete stale keys without manual cleanup
- Millisecond timing differences aren't a reliable way to prove caching on a fast local SQLite database — checking Redis directly (via KEYS/GET) is a more honest and reliable way to confirm cache behavior
- Cache invalidation must happen immediately after any write (POST/PUT/DELETE) that changes cached data, or users can see outdated information

## Testing performed
- Confirmed Redis connection from Flask (redis_client.ping() returned True)
- Practiced SET/GET/DEL and TTL expiration directly in memurai-cli
- Called GET /auth/me twice, confirmed a cache entry (user:<id>) appeared in Redis via KEYS/GET
- Updated a user's name via PUT /auth/me, then confirmed the immediately following GET /auth/me returned the updated name (not stale cached data)
- Confirmed the Redis cache entry itself reflected the updated name after the PUT