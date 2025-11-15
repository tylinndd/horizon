# Deployment Guide

## Quick Answer: Do You Need Docker?

**No, you don't need Docker for Render deployment!** 

Render supports native deployments:
- **Backend**: Deploy as Python Web Service
- **Frontend**: Deploy as Static Site
- **Database**: Use Render's managed PostgreSQL

Docker is only useful for:
- Local development consistency
- Complex multi-service orchestration
- But **NOT required** for Render

## Deployment Options

### Option 1: Render (Recommended - No Docker Needed)

See `RENDER_DEPLOYMENT.md` for complete instructions.

**Quick steps:**
1. Create PostgreSQL database in Render
2. Deploy backend as Web Service (Python)
3. Deploy frontend as Static Site
4. Run migrations via Shell or build script

### Option 2: Docker (If You Want It)

If you prefer Docker for local development or other platforms:

```bash
# Local development
docker compose up -d

# Production (if deploying to platforms that require Docker)
docker build -t horizon-backend ./backend
docker build -t horizon-frontend ./frontend
```

### Option 3: Other Platforms

- **Heroku**: Similar to Render, no Docker needed
- **Railway**: Supports both Docker and native
- **Fly.io**: Supports both Docker and native
- **AWS/GCP/Azure**: Can use Docker or native deployments

## Recommendation

For Render deployment: **Skip Docker** and use native deployments. It's simpler, faster, and cheaper.

Keep Docker files for:
- Local development (optional)
- Future platform migrations
- Team consistency

But you don't need them for Render!

