#!/bin/bash

#############################################
# Backup Script for Career Lexicon Builder
#############################################
#
# This script performs:
# 1. Database backup
# 2. Application data backup
# 3. Compression and timestamping
# 4. Optional cleanup of old backups
#
# Usage: ./backup.sh [--keep-days 30]
#

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="$APP_DIR/backups"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
KEEP_DAYS=30

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --keep-days)
            KEEP_DAYS="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--keep-days 30]"
            exit 1
            ;;
    esac
done

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}Career Lexicon Builder - Backup${NC}"
echo -e "${GREEN}Started at: $(date)${NC}"
echo -e "${GREEN}======================================${NC}"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Change to application directory
cd "$APP_DIR"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: docker-compose not found${NC}"
    exit 1
fi

# Check if services are running
if ! docker-compose ps | grep -q "Up"; then
    echo -e "${YELLOW}Warning: Services may not be running${NC}"
fi

# 1. Backup Database
echo -e "\n${GREEN}[1/4] Backing up PostgreSQL database...${NC}"
DB_BACKUP_FILE="$BACKUP_DIR/database-$TIMESTAMP.sql"

if docker-compose exec -T postgres pg_dump -U wrapper_user wrapper_prod > "$DB_BACKUP_FILE" 2>/dev/null; then
    echo -e "${GREEN}✓ Database backup created: $DB_BACKUP_FILE${NC}"

    # Compress database backup
    echo -e "${GREEN}    Compressing database backup...${NC}"
    gzip "$DB_BACKUP_FILE"
    echo -e "${GREEN}✓ Compressed: ${DB_BACKUP_FILE}.gz${NC}"

    # Show backup size
    DB_SIZE=$(du -h "${DB_BACKUP_FILE}.gz" | cut -f1)
    echo -e "${GREEN}    Size: $DB_SIZE${NC}"
else
    echo -e "${RED}✗ Database backup failed${NC}"
    echo -e "${YELLOW}    This is normal if the database is not running or empty${NC}"
fi

# 2. Backup Application Data
echo -e "\n${GREEN}[2/4] Backing up application data...${NC}"
APP_BACKUP_FILE="$BACKUP_DIR/applications-$TIMESTAMP.tar.gz"

if [ -d "$APP_DIR/applications" ] && [ "$(ls -A "$APP_DIR/applications")" ]; then
    tar -czf "$APP_BACKUP_FILE" -C "$APP_DIR" applications/ 2>/dev/null
    echo -e "${GREEN}✓ Application data backup created: $APP_BACKUP_FILE${NC}"

    # Show backup size
    APP_SIZE=$(du -h "$APP_BACKUP_FILE" | cut -f1)
    echo -e "${GREEN}    Size: $APP_SIZE${NC}"
else
    echo -e "${YELLOW}⊘ No application data to backup${NC}"
fi

# 3. Backup Docker Volumes (optional, for extra safety)
echo -e "\n${GREEN}[3/4] Backing up Docker volumes...${NC}"
VOLUMES_BACKUP_FILE="$BACKUP_DIR/volumes-$TIMESTAMP.tar.gz"

if docker volume ls | grep -q wrapper-app; then
    # List all volumes related to the app
    VOLUMES=$(docker volume ls --filter name=wrapper-app -q)

    if [ -n "$VOLUMES" ]; then
        # Create temporary container to backup volumes
        for volume in $VOLUMES; do
            echo -e "${GREEN}    Backing up volume: $volume${NC}"
            docker run --rm \
                -v "$volume:/volume" \
                -v "$BACKUP_DIR:/backup" \
                alpine \
                tar -czf "/backup/volume-$volume-$TIMESTAMP.tar.gz" -C /volume .
        done
        echo -e "${GREEN}✓ Volume backups created${NC}"
    else
        echo -e "${YELLOW}⊘ No Docker volumes found${NC}"
    fi
else
    echo -e "${YELLOW}⊘ No Docker volumes to backup${NC}"
fi

# 4. Create backup manifest
echo -e "\n${GREEN}[4/4] Creating backup manifest...${NC}"
MANIFEST_FILE="$BACKUP_DIR/backup-manifest-$TIMESTAMP.txt"

cat > "$MANIFEST_FILE" << EOF
Backup Manifest
===============
Timestamp: $TIMESTAMP
Date: $(date)
Hostname: $(hostname)

Files:
------
$(ls -lh "$BACKUP_DIR"/*-$TIMESTAMP.* 2>/dev/null | awk '{print $9, "(" $5 ")"}' || echo "No backup files created")

Docker Services:
----------------
$(docker-compose ps 2>/dev/null || echo "Services not running")

Docker Volumes:
---------------
$(docker volume ls --filter name=wrapper-app 2>/dev/null || echo "No volumes found")

Environment Variables:
---------------------
$(grep -v "PASSWORD\|SECRET\|KEY" .env 2>/dev/null || echo ".env not found")
EOF

echo -e "${GREEN}✓ Manifest created: $MANIFEST_FILE${NC}"

# 5. Cleanup old backups
echo -e "\n${GREEN}[5/5] Cleaning up old backups (keeping last $KEEP_DAYS days)...${NC}"
DELETED_COUNT=0

# Delete old backup files
if [ -n "$(find "$BACKUP_DIR" -name "*.sql.gz" -mtime +$KEEP_DAYS 2>/dev/null)" ]; then
    find "$BACKUP_DIR" -name "*.sql.gz" -mtime +$KEEP_DAYS -delete
    DELETED_COUNT=$((DELETED_COUNT + 1))
fi

if [ -n "$(find "$BACKUP_DIR" -name "applications-*.tar.gz" -mtime +$KEEP_DAYS 2>/dev/null)" ]; then
    find "$BACKUP_DIR" -name "applications-*.tar.gz" -mtime +$KEEP_DAYS -delete
    DELETED_COUNT=$((DELETED_COUNT + 1))
fi

if [ -n "$(find "$BACKUP_DIR" -name "volume-*.tar.gz" -mtime +$KEEP_DAYS 2>/dev/null)" ]; then
    find "$BACKUP_DIR" -name "volume-*.tar.gz" -mtime +$KEEP_DAYS -delete
    DELETED_COUNT=$((DELETED_COUNT + 1))
fi

if [ -n "$(find "$BACKUP_DIR" -name "backup-manifest-*.txt" -mtime +$KEEP_DAYS 2>/dev/null)" ]; then
    find "$BACKUP_DIR" -name "backup-manifest-*.txt" -mtime +$KEEP_DAYS -delete
    DELETED_COUNT=$((DELETED_COUNT + 1))
fi

if [ $DELETED_COUNT -gt 0 ]; then
    echo -e "${GREEN}✓ Cleaned up old backups${NC}"
else
    echo -e "${YELLOW}⊘ No old backups to clean up${NC}"
fi

# Summary
echo -e "\n${GREEN}======================================${NC}"
echo -e "${GREEN}Backup completed successfully!${NC}"
echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}Backup directory: $BACKUP_DIR${NC}"
echo -e "${GREEN}Total backups: $(ls -1 "$BACKUP_DIR"/*-$TIMESTAMP.* 2>/dev/null | wc -l)${NC}"
echo -e "${GREEN}Timestamp: $TIMESTAMP${NC}"
echo -e "${GREEN}======================================${NC}"

# Calculate total backup size
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
echo -e "${GREEN}Total backup directory size: $TOTAL_SIZE${NC}"

exit 0
