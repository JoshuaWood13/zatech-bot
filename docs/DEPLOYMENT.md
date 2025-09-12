**Deployment (Docker)**

Local Compose
- Prereqs: Docker and Docker Compose.
- Create a `.env` (repo root) with your Slack tokens if you want to run HTTP or Socket services:
  - `SLACK_BOT_TOKEN=...`
  - `SLACK_SIGNING_SECRET=...` (for HTTP) or `SLACK_APP_TOKEN=...` (for Socket)
- Bring up Postgres + Redis + HTTP app:
  - `docker compose up --build zebras-http`
  - Exposed locally at `http://localhost:5000` (host 5000 → container 43117).
  - Health check endpoint: `http://localhost:5000/healthz`.
- For Socket Mode instead:
  - `docker compose up --build zebras-socket`
- Optional worker:
  - `docker compose up --build zebras-worker`

Notes
- DB DSN in compose points to the `postgres` service; migrations run automatically in the container entrypoint.
- For HTTP mode with Slack, expose your machine publicly (or use a tunnel) and set Slack request URLs accordingly.
- Logs are printed to container stdout.
  

Custom Deployment
- Build image: `docker build -t zebras:latest .`
- Run HTTP:
  - `docker run --rm -p 3000:3000 -e MODE=http -e DATABASE_URL=... -e SLACK_BOT_TOKEN=... -e SLACK_SIGNING_SECRET=... zebras:latest`
- Run Socket Mode:
  - `docker run --rm -e MODE=socket -e DATABASE_URL=... -e SLACK_BOT_TOKEN=... -e SLACK_APP_TOKEN=... zebras:latest`
- Run Worker:
  - `docker run --rm -e MODE=worker -e DATABASE_URL=... -e REDIS_URL=... zebras:latest`

Health & Readiness
- HTTP: `/healthz` returns `{ "status": "ok" }`.
- Consider adding readiness checks for DB/Redis in future iterations.

Exposing with ngrok
- Quick guide: `docs/NGROK.md` shows local binary and Docker-based tunnels.
