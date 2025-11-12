#!/bin/bash

#############################################
# Restore Script for Career Lexicon Builder
#############################################
#
# This script performs:
# 1. Database restoration from backup
# 2. Application data restoration
# 3. Verification and health checks
#
# Usage: ./restore.sh <timestamp>
# Example: ./restore.sh 20240101-120000
#

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="$APP_DIR/backups"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if timestamp is provided
if [ $# -eq 0 ]; then
    echo -e "${RED}Error: No timestamp provided${NC}"
    echo -e "Usage: $0 <timestamp>"
    echo -e "Example: $0 20240101-120000"
    echo -e "\nAvailable backups:"
    ls -1 "$BACKUP_DIR"/database-*.sql.gz 2>/dev/null | sed 's/.*database-\(.*\)\.sql\.gz/  \1/' || echo "  No backups found"
    exit 1
fi

TIMESTAMP="$1"
DB_BACKUP_FILE="$BACKUP_DIR/database-$TIMESTAMP.sql.gz"
APP_BACKUP_FILE="$BACKUP_DIR/applications-$TIMESTAMP.tar.gz"

echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}Career Lexicon Builder - Restore${NC}"
echo -e "${GREEN}Started at: $(date)${NC}"
echo -e "${GREEN}======================================${NC}"

# Verify backup files exist
echo -e "\n${GREEN}Verifying backup files...${NC}"

if [ ! -f "$DB_BACKUP_FILE" ]; then
    echo -e "${RED}Error: Database backup not found: $DB_BACKUP_FILE${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Database backup found: $DB_BACKUP_FILE${NC}"

if [ -f "$APP_BACKUP_FILE" ]; then
    echo -e "${GREEN}✓ Application data backup found: $APP_BACKUP_FILE${NC}"
    HAS_APP_BACKUP=true
else
    echo -e "${YELLOW}⊘ Application data backup not found (this may be normal)${NC}"
    HAS_APP_BACKUP=false
fi

# Confirmation prompt
echo -e "\n${YELLOW}WARNING: This will replace the current database and application data!${NC}"
echo -e "${YELLOW}Timestamp to restore: $TIMESTAMP${NC}"
read -p "Are you sure you want to continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo -e "${RED}Restore cancelled${NC}"
    exit 0
fi

# Change to application directory
cd "$APP_DIR"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: docker-compose not found${NC}"
    exit 1
fi

# 1. Create pre-restore backup (safety measure)
echo -e "\n${GREEN}[1/5] Creating pre-restore backup...${NC}"
PRERESTORE_TIMESTAMP=$(date +%Y%m%d-%H%M%S)
PRERESTORE_BACKUP="$BACKUP_DIR/pre-restore-$PRERESTORE_TIMESTAMP.sql.gz"

if docker-compose exec -T postgres pg_dump -U wrapper_user wrapper_prod 2>/dev/null | gzip > "$PRERESTORE_BACKUP"; then
    echo -e "${GREEN}✓ Pre-restore backup created: $PRERESTORE_BACKUP${NC}"
else
    echo -e "${YELLOW}⊘ Could not create pre-restore backup (database may be empty)${NC}"
fi

# 2. Stop backend service
echo -e "\n${GREEN}[2/5] Stopping backend service...${NC}"
docker-compose stop backend
echo -e "${GREEN}✓ Backend stopped${NC}"

# 3. Restore database
echo -e "\n${GREEN}[3/5] Restoring database...${NC}"

# Drop existing connections
docker-compose exec -T postgres psql -U wrapper_user postgres -c \
    "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='wrapper_prod' AND pid <> pg_backend_pid();" \
    2>/dev/null || true

# Drop and recreate database
echo -e "${GREEN}    Recreating database...${NC}"
docker-compose exec -T postgres psql -U wrapper_user postgres -c "DROP DATABASE IF EXISTS wrapper_prod;" 2>/dev/null || true
docker-compose exec -T postgres psql -U wrapper_user postgres -c "CREATE DATABASE wrapper_prod OWNER wrapper_user;" 2>/dev/null

# Restore from backup
echo -e "${GREEN}    Restoring data...${NC}"
gunzip -c "$DB_BACKUP_FILE" | docker-compose exec -T postgres psql -U wrapper_user wrapper_prod

echo -e "${GREEN}✓ Database restored successfully${NC}"

# 4. Restore application data
if [ "$HAS_APP_BACKUP" = true ]; then
    echo -e "\n${GREEN}[4/5] Restoring application data...${NC}"

    # Backup current applications directory
    if [ -d "$APP_DIR/applications" ] && [ "$(ls -A "$APP_DIR/applications")" ]; then
        echo -e "${GREEN}    Backing up current applications directory...${NC}"
        mv "$APP_DIR/applications" "$APP_DIR/applications.old-$PRERESTORE_TIMESTAMP"
    fi

    # Extract application data
    echo -e "${GREEN}    Extracting application data...${NC}"
    tar -xzf "$APP_BACKUP_FILE" -C "$APP_DIR"

    echo -e "${GREEN}✓ Application data restored${NC}"
else
    echo -e "\n${GREEN}[4/5] Skipping application data restore (no backup found)${NC}"
fi

# 5. Restart services and verify
echo -e "\n${GREEN}[5/5] Restarting services...${NC}"
docker-compose start backend

# Wait for backend to be healthy
echo -e "${GREEN}    Waiting for backend to be healthy...${NC}"
sleep 5

MAX_ATTEMPTS=30
ATTEMPT=0
until curl -f http://localhost:8000/health 2>/dev/null || [ $ATTEMPT -eq $MAX_ATTEMPTS ]; do
    echo -e "${YELLOW}    Health check attempt $((ATTEMPT+1))/$MAX_ATTEMPTS...${NC}"
    sleep 2
    ATTEMPT=$((ATTEMPT+1))
done

if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
    echo -e "${RED}✗ Health check failed after restore${NC}"
    echo -e "${YELLOW}Check logs: docker-compose logs backend${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Backend is healthy${NC}"

# Run migrations to ensure schema is up to date
echo -e "\n${GREEN}Running database migrations...${NC}"
docker-compose exec -T backend alembic upgrade head
echo -e "${GREEN}✓ Migrations complete${NC}"

# Summary
echo -e "\n${GREEN}======================================${NC}"
echo -e "${GREEN}Restore completed successfully!${NC}"
echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}Restored from: $TIMESTAMP${NC}"
echo -e "${GREEN}Pre-restore backup: $PRERESTORE_BACKUP${NC}"

# Show service status
echo -e "\n${GREEN}Service Status:${NC}"
docker-compose ps

# Verification
echo -e "\n${GREEN}Verification:${NC}"
echo -e "${GREEN}✓ Database connection: OK${NC}"
echo -e "${GREEN}✓ Backend health check: OK${NC}"

if [ "$HAS_APP_BACKUP" = true ]; then
    echo -e "${GREEN}✓ Application data: Restored${NC}"

    if [ -d "$APP_DIR/applications.old-$PRERESTORE_TIMESTAMP" ]; then
        echo -e "\n${YELLOW}Note: Old applications directory saved as:${NC}"
        echo -e "${YELLOW}      $APP_DIR/applications.old-$PRERESTORE_TIMESTAMP${NC}"
        echo -e "${YELLOW}      You can safely delete it after verifying the restore.${NC}"
    fi
fi

echo -e "\n${GREEN}======================================${NC}"
echo -e "${GREEN}Restore process complete!${NC}"
echo -e "${GREEN}Please verify your application is working correctly.${NC}"
echo -e "${GREEN}======================================${NC}"

exit 0
