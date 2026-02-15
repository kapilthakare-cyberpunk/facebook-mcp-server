# Progress Snapshot

- Added LinkedIn and Telegram MCP servers alongside the existing Facebook server. Scripts registered in `pyproject.toml`; Dockerfiles present for each target.
- Environment samples: `src/facebook_mcp_server/.env.example`, `src/linkedin_mcp_server/.env.example`, `src/telegram_mcp_server/.env.example` detail required vars.
- Docker builds succeed: `docker build -t facebook-mcp-server:latest -f Dockerfile .`, `docker build -t linkedin-mcp-server:latest -f Dockerfile.linkedin .`, `docker build -t telegram-mcp-server:latest -f Dockerfile.telegram .`.
- Run containers with env files (keeps secrets out of images):  
  - `docker run --rm -it --env-file .env facebook-mcp-server:latest`  
  - `docker run --rm -it --env-file .env.linkedin linkedin-mcp-server:latest`  
  - `docker run --rm -it --env-file .env.telegram telegram-mcp-server:latest`
- Smoke tests pending: via your MCP client, call Facebook `get_page_posts`/`create_post`, LinkedIn `list_recent_posts`/`create_post`, Telegram `send_message`/`get_updates`.
