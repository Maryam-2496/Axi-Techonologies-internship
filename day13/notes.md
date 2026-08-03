# Day 13: Real-Time Communication with WebSockets

## What I did
- Installed Flask-SocketIO and wired it into the existing Flask app alongside auth, caching, and queue features
- Implemented connection lifecycle handlers: connect, disconnect, and a default error handler
- Built custom event handlers for joining rooms (join_room) and sending/broadcasting messages (send_message / receive_message)
- Tested real-time multi-client messaging using a simple browser-based Socket.IO test client, confirming messages sent from one browser tab appear instantly in another tab in the same room
- Documented Redis Pub/Sub as the mechanism for scaling WebSocket events across multiple server instances (not load-tested locally, since this only applies when running more than one server process)
- Added JWT authentication to the WebSocket connection handshake: connections must supply a valid token as a query parameter, or they are rejected and disconnected
- Verified rejection behavior for both an invalid token and a missing token

## What I learned
- WebSockets keep one persistent connection open for two-way communication, unlike HTTP's repeated request-response cycle
- Socket.IO falls back to HTTP long-polling automatically when a true WebSocket upgrade isn't available or fails - this fallback still delivers real-time-feeling updates
- Flask's built-in development server has real limitations with WebSocket upgrades in certain async modes; "threading" mode combined with polling-only transport was the practical, stable configuration for this local Windows dev environment
- Authenticating a WebSocket connection happens once, at the initial handshake (via a token in the query string), rather than per-message like typical HTTP requests
- Redis Pub/Sub lets multiple independent server processes share real-time events, which matters once an app scales beyond a single server instance

## Testing performed
- Confirmed a client can connect, receive a welcome message, and that the connect/disconnect/error handlers all fire correctly
- Opened two separate browser tabs, joined the same room in both, and confirmed messages sent in either tab appeared in both instantly
- Registered and logged in a test user via Thunder Client, retrieved a JWT, and confirmed a WebSocket connection succeeds only when a valid token is supplied
- Tested connection rejection with an invalid token (rejected with "invalid token") and with no token at all (rejected with "no token provided")