# Production Deployment Guide

Complete guide for deploying the Career Lexicon Builder wrapper application to production.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Initial Setup](#initial-setup)
- [Environment Configuration](#environment-configuration)
- [SSL Certificate Setup](#ssl-certificate-setup)
- [Initial Deployment](#initial-deployment)
- [Updating the Application](#updating-the-application)
- [Backup and Restore](#backup-and-restore)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
- [Troubleshooting](#troubleshooting)
- [Security Considerations](#security-considerations)

## Prerequisites

Before deploying to production, ensure you have:

- **Server Requirements:**
  - Ubuntu 22.04 LTS (or similar Linux distribution)
  - Minimum 2 CPU cores, 4GB RAM, 20GB storage
  - Root or sudo access
  - Public IP address and domain name

- **Software Requirements:**
  - Docker Engine 20.10+
  - Docker Compose 2.0+
  - curl and basic utilities

- **External Services:**
  - Domain name with DNS configured (A record pointing to server IP)
  - Anthropic API key (for Claude integration)
  - GitHub account (for container registry)

## Initial Setup

### 1. Server Preparation

Connect to your server via SSH and run the following commands:

```bash
# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add current user to docker group (avoid using sudo for docker commands)
sudo usermod -aG docker $USER

# Install Docker Compose plugin
sudo apt-get install -y docker-compose-plugin

# Verify installations
docker --version
docker compose version

# Log out and back in for group changes to take effect
exit
```

### 2. Create Application Directory

```bash
# Create application directory
sudo mkdir -p /opt/wrapper-app
sudo chown $USER:$USER /opt/wrapper-app
cd /opt/wrapper-app

# Create necessary subdirectories
mkdir -p backups nginx/ssl applications
```

### 3. Clone Configuration Files

You need to copy the following files to your production server:

- `docker-compose.prod.yml`
- `wrapper-frontend/nginx.prod.conf` (to `nginx/nginx.prod.conf`)
- `.env.production` (create from template below)

```bash
# Option 1: Clone from repository
git clone https://github.com/YOUR_USERNAME/career-lexicon-builder.git temp
cp temp/docker-compose.prod.yml .
cp temp/wrapper-frontend/nginx.prod.conf nginx/
rm -rf temp

# Option 2: Manual copy via SCP
# From your local machine:
scp docker-compose.prod.yml user@server:/opt/wrapper-app/
scp wrapper-frontend/nginx.prod.conf user@server:/opt/wrapper-app/nginx/
```

## Environment Configuration

### 1. Create Production Environment File

Create `/opt/wrapper-app/.env` with the following content:

```env
# Database Configuration
POSTGRES_DB=wrapper_prod
POSTGRES_USER=wrapper_user
POSTGRES_PASSWORD=CHANGE_ME_GENERATE_STRONG_PASSWORD

# API Keys
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE

# Security
JWT_SECRET_KEY=CHANGE_ME_GENERATE_RANDOM_STRING_64_CHARS

# GitHub Container Registry
GITHUB_USERNAME=your-github-username
IMAGE_TAG=latest

# Application Settings
ENVIRONMENT=production
CLAUDE_CODE_PATH=claude
CORS_ORIGINS=https://yourdomain.com

# Optional: Custom deploy port
DEPLOY_PORT=22
```

### 2. Generate Secure Secrets

Generate strong passwords and secrets:

```bash
# Generate strong database password
openssl rand -base64 32

# Generate JWT secret key
openssl rand -hex 32

# Save these in your .env file
```

### 3. Secure the Environment File

```bash
# Set restrictive permissions
chmod 600 .env

# Verify only you can read it
ls -l .env
```

## SSL Certificate Setup

### Option 1: Let's Encrypt (Recommended)

```bash
# Install Certbot
sudo apt-get install -y certbot

# Stop any services using ports 80/443
docker-compose -f docker-compose.prod.yml down

# Obtain certificate (replace with your domain)
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Create symbolic links to certificates
sudo ln -s /etc/letsencrypt/live/yourdomain.com/fullchain.pem /opt/wrapper-app/nginx/ssl/fullchain.pem
sudo ln -s /etc/letsencrypt/live/yourdomain.com/privkey.pem /opt/wrapper-app/nginx/ssl/privkey.pem

# Set up automatic renewal
sudo crontab -e
# Add this line:
0 3 * * * certbot renew --quiet && docker-compose -f /opt/wrapper-app/docker-compose.prod.yml restart frontend
```

### Option 2: Custom SSL Certificate

If you have your own SSL certificates:

```bash
# Copy certificates to nginx/ssl directory
sudo cp /path/to/your/fullchain.pem /opt/wrapper-app/nginx/ssl/
sudo cp /path/to/your/privkey.pem /opt/wrapper-app/nginx/ssl/

# Set proper permissions
sudo chmod 644 /opt/wrapper-app/nginx/ssl/fullchain.pem
sudo chmod 600 /opt/wrapper-app/nginx/ssl/privkey.pem
```

## Initial Deployment

### 1. Pull Docker Images

```bash
cd /opt/wrapper-app

# Log in to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u YOUR_USERNAME --password-stdin

# Pull images
docker-compose -f docker-compose.prod.yml pull
```

### 2. Start Services

```bash
# Start all services
docker-compose -f docker-compose.prod.yml up -d

# Watch logs during startup
docker-compose -f docker-compose.prod.yml logs -f
```

### 3. Initialize Database

The database migrations run automatically on backend startup, but you can verify:

```bash
# Check migration status
docker-compose exec backend alembic current

# Manually run migrations if needed
docker-compose exec backend alembic upgrade head
```

### 4. Verify Deployment

```bash
# Check service status
docker-compose ps

# Test backend health
curl http://localhost:8000/health

# Test frontend (if SSL is configured)
curl https://yourdomain.com/

# Check logs for any errors
docker-compose logs backend
docker-compose logs frontend
```

## Updating the Application

### Manual Update

```bash
cd /opt/wrapper-app

# Pull latest images
docker-compose -f docker-compose.prod.yml pull

# Create pre-deployment backup
./scripts/backup.sh

# Restart services
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose exec backend alembic upgrade head

# Verify health
curl -f http://localhost:8000/health
```

### Automated Update via GitHub Actions

Updates are automated when you push a new tag:

```bash
# On your development machine
git tag -a v1.0.1 -m "Release version 1.0.1"
git push origin v1.0.1

# GitHub Actions will:
# 1. Build and push Docker images
# 2. SSH to production server
# 3. Pull latest images
# 4. Backup database
# 5. Restart services
# 6. Run migrations
# 7. Verify health check
```

## Backup and Restore

### Automated Daily Backups

Create a cron job for automated backups:

```bash
# Edit crontab
crontab -e

# Add these lines:
# Daily database backup at 2 AM
0 2 * * * /opt/wrapper-app/scripts/backup.sh

# Weekly application data backup at 3 AM on Sundays
0 3 * * 0 tar -czf /opt/wrapper-app/backups/applications-$(date +\%Y\%m\%d).tar.gz -C /opt/wrapper-app applications/
```

### Manual Database Backup

```bash
# Backup database
docker-compose exec -T postgres pg_dump -U wrapper_user wrapper_prod > backups/backup-$(date +%Y%m%d-%H%M%S).sql

# Compress backup
gzip backups/backup-$(date +%Y%m%d-%H%M%S).sql
```

### Restore Database

```bash
# Stop backend service
docker-compose stop backend

# Restore from backup
gunzip -c backups/backup-20240101-120000.sql.gz | docker-compose exec -T postgres psql -U wrapper_user wrapper_prod

# Restart services
docker-compose start backend
```

### Backup Retention

```bash
# Keep only last 30 days of backups (add to cron)
0 4 * * * find /opt/wrapper-app/backups -name "*.sql.gz" -mtime +30 -delete
```

## Monitoring and Maintenance

### Health Checks

```bash
# Backend health with dependency status
curl http://localhost:8000/health | jq

# Expected output:
# {
#   "status": "healthy",
#   "database": "healthy",
#   "anthropic_api": "healthy"
# }

# Frontend health
curl http://localhost/

# Database connection
docker-compose exec postgres pg_isready -U wrapper_user -d wrapper_prod
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres

# Last 100 lines
docker-compose logs --tail=100 backend

# Follow logs since specific time
docker-compose logs --since 30m backend
```

### Service Management

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart backend

# Stop all services
docker-compose stop

# Start all services
docker-compose start

# View resource usage
docker stats
```

### Database Maintenance

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U wrapper_user wrapper_prod

# Vacuum database (inside psql)
VACUUM ANALYZE;

# Check database size
SELECT pg_size_pretty(pg_database_size('wrapper_prod'));

# List tables
\dt

# Exit psql
\q
```

### Disk Space Management

```bash
# Check disk usage
df -h

# Check Docker disk usage
docker system df

# Clean up unused Docker resources
docker system prune -a --volumes

# Clean up old logs (be careful!)
truncate -s 0 /var/lib/docker/containers/*/*-json.log
```

## Troubleshooting

### Backend Won't Start

```bash
# Check logs
docker-compose logs backend

# Common issues:
# 1. Database connection failed
#    - Verify DATABASE_URL in .env
#    - Check postgres service is running: docker-compose ps postgres

# 2. Missing ANTHROPIC_API_KEY
#    - Verify ANTHROPIC_API_KEY in .env
#    - Restart backend: docker-compose restart backend

# 3. Migration errors
#    - Check migration status: docker-compose exec backend alembic current
#    - Try manual migration: docker-compose exec backend alembic upgrade head
```

### Frontend Returns 502 Bad Gateway

```bash
# Check backend is running
docker-compose ps backend

# Check backend health
curl http://localhost:8000/health

# Check nginx configuration
docker-compose exec frontend nginx -t

# Restart nginx
docker-compose restart frontend
```

### SSL Certificate Issues

```bash
# Check certificate validity
openssl x509 -in nginx/ssl/fullchain.pem -text -noout

# Renew Let's Encrypt certificate
sudo certbot renew

# Restart frontend to reload certificates
docker-compose restart frontend
```

### Database Connection Issues

```bash
# Check postgres is running
docker-compose ps postgres

# Check postgres logs
docker-compose logs postgres

# Test connection manually
docker-compose exec postgres psql -U wrapper_user -d wrapper_prod -c "SELECT version();"

# Restart postgres
docker-compose restart postgres
```

### Out of Disk Space

```bash
# Check disk usage
df -h

# Clean up Docker
docker system prune -a --volumes

# Clean up old backups
find backups/ -name "*.sql.gz" -mtime +30 -delete

# Clean up old application data if safe
# (Be careful with this!)
```

### High Memory Usage

```bash
# Check container resource usage
docker stats

# Restart high-memory services
docker-compose restart backend

# Increase memory limits in docker-compose.prod.yml:
# services:
#   backend:
#     deploy:
#       resources:
#         limits:
#           memory: 2G
```

## Security Considerations

### Firewall Configuration

```bash
# Install UFW
sudo apt-get install -y ufw

# Allow SSH (IMPORTANT: Do this first!)
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

### Regular Updates

```bash
# Update system packages monthly
sudo apt-get update
sudo apt-get upgrade -y

# Update Docker images weekly
cd /opt/wrapper-app
docker-compose pull
docker-compose up -d
```

### Security Scanning

```bash
# Scan Docker images for vulnerabilities
docker scout cve backend:latest
docker scout cve frontend:latest

# Update base images regularly by rebuilding
```

### Access Control

```bash
# Restrict file permissions
chmod 600 /opt/wrapper-app/.env
chmod 700 /opt/wrapper-app/scripts/
chmod 600 /opt/wrapper-app/nginx/ssl/*.pem

# Use SSH keys only (disable password authentication)
sudo vi /etc/ssh/sshd_config
# Set: PasswordAuthentication no
sudo systemctl restart sshd
```

### Monitor Failed Login Attempts

```bash
# Install fail2ban
sudo apt-get install -y fail2ban

# Configure for SSH
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

## Production Checklist

Before going live, verify:

- [ ] SSL certificates are properly configured and valid
- [ ] All environment variables are set in .env
- [ ] Strong passwords are used for database and JWT
- [ ] Firewall is configured and enabled
- [ ] Automated backups are scheduled
- [ ] Health checks are passing
- [ ] Logs are being written correctly
- [ ] Domain DNS is properly configured
- [ ] CORS origins are correctly set
- [ ] GitHub Container Registry authentication is working
- [ ] Monitoring is in place
- [ ] Backup restore procedure has been tested
- [ ] Documentation is up to date

## Support and Resources

- **Documentation:** See README.md and WRAPPER_HANDOFF.md
- **Issues:** https://github.com/YOUR_USERNAME/career-lexicon-builder/issues
- **Docker:** https://docs.docker.com/
- **Let's Encrypt:** https://letsencrypt.org/
- **Nginx:** https://nginx.org/en/docs/
