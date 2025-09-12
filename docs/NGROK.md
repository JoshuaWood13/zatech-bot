**Expose Locally with ngrok**

Option 1: Local binary (fastest)
- Install ngrok from https://ngrok.com/download and run `ngrok config add-authtoken <your-token>`.
- Start a tunnel to your local HTTP server (port 43117 by default):
  - Start ZEBRAS HTTP locally: `zebras http --port 43117`
  - In another terminal: `ngrok http 43117`
- Copy the HTTPS forwarding URL (e.g., `https://abcd-1234.ngrok-free.app`).
- In Slack app settings set:
  - Event Subscriptions → `https://<ngrok-host>/slack/events`
  - Slash Commands → `https://<ngrok-host>/slack/commands`

Option 2: Docker Compose service
- Add your authtoken in an `.env` file at repo root:
  - `NGROK_AUTHTOKEN=xxxxxxxxxxxxxxxx`
- Bring up the HTTP app and ngrok:
  - `docker compose up --build zebras-http ngrok`
- Watch the `ngrok` service logs; it prints the HTTPS forwarding URL.
- Point Slack to that URL as above.

Tips
- Keep the ngrok process running while Slack verifies the URL.
- If you restart ngrok, the URL changes unless you have a reserved domain (paid plan).
- For Socket Mode, you don’t need ngrok, as Slack connects outbound to you.
