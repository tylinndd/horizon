# Installing Docker on macOS

## Option 1: Docker Desktop (Recommended)

1. **Download Docker Desktop:**
   - Visit: https://www.docker.com/products/docker-desktop/
   - Download Docker Desktop for Mac (Apple Silicon or Intel)

2. **Install:**
   - Open the downloaded `.dmg` file
   - Drag Docker to Applications
   - Launch Docker Desktop from Applications
   - Follow the setup wizard

3. **Verify Installation:**
   ```bash
   docker --version
   docker compose version
   ```

4. **Start Docker Desktop:**
   - Make sure Docker Desktop is running (check the menu bar for the Docker icon)

## Option 2: Using Homebrew

```bash
brew install --cask docker
```

Then launch Docker Desktop from Applications.

## After Installation

Once Docker is installed, you can use:
- `docker compose` (newer syntax, recommended)
- OR `docker-compose` (older syntax, still works)

Both commands work the same way. The newer Docker versions use `docker compose` as a plugin.

## Troubleshooting

If Docker Desktop is running but commands don't work:
1. Check Docker Desktop is running (menu bar icon)
2. Restart your terminal
3. Try: `docker ps` to verify Docker is working

