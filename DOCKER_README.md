# Docker Deployment Guide

## Development (Local PostgreSQL only)

```bash
# Start PostgreSQL only
docker-compose -f docker-compose.dev.yml up -d

# Run backend locally
cd wrapper-backend
source venv/bin/activate
export DATABASE_URL=postgresql://wrapper_user:wrapper_pass@localhost:5432/wrapper
alembic upgrade head
python main.py

# Run frontend locally
cd wrapper-frontend
npm run dev
```

## Production (Full Stack)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Environment Variables

Create `.env` file in root:
```
ANTHROPIC_API_KEY=your_key_here
```

## Accessing Services

- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432
