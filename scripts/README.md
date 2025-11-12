# Deployment Scripts

Utility scripts for managing the Career Lexicon Builder wrapper application in production.

## Available Scripts

### backup.sh

Comprehensive backup script that creates timestamped backups of:
- PostgreSQL database (compressed SQL dump)
- Application data files
- Docker volumes
- Backup manifest with metadata

**Usage:**

```bash
# Run manual backup
./scripts/backup.sh

# Run backup with custom retention
./scripts/backup.sh --keep-days 60
```

**Automated Backups:**

Add to crontab for automated daily backups:

```bash
# Edit crontab
crontab -e

# Add this line for daily backups at 2 AM
0 2 * * * /opt/wrapper-app/scripts/backup.sh --keep-days 30
```

**Features:**
- Creates timestamped backups in `backups/` directory
- Compresses database dumps with gzip
- Creates backup manifest with metadata
- Automatically cleans up old backups (default: 30 days)
- Safe execution with error handling
- Color-coded output for easy monitoring

**Output:**
```
backup-20240101-120000.sql.gz    # Database backup
applications-20240101-120000.tar.gz  # Application data
backup-manifest-20240101-120000.txt  # Backup metadata
```

### restore.sh

Restoration script that safely restores database and application data from backups.

**Usage:**

```bash
# List available backups
./scripts/restore.sh

# Restore from specific backup
./scripts/restore.sh 20240101-120000
```

**Safety Features:**
- Creates pre-restore backup automatically
- Requires confirmation before proceeding
- Stops services gracefully during restore
- Verifies health after restoration
- Runs database migrations automatically
- Preserves old data as `.old-TIMESTAMP` backup

**Process:**
1. Verifies backup files exist
2. Creates pre-restore safety backup
3. Stops backend service
4. Restores database
5. Restores application data
6. Restarts services
7. Runs migrations
8. Verifies health checks

## Backup Strategy

### Daily Backups

Recommended cron configuration:

```bash
# Database backup at 2 AM
0 2 * * * /opt/wrapper-app/scripts/backup.sh

# Weekly full system backup at 3 AM on Sundays
0 3 * * 0 /opt/wrapper-app/scripts/backup.sh && tar -czf /opt/wrapper-app/backups/full-system-$(date +\%Y\%m\%d).tar.gz /opt/wrapper-app/

# Cleanup old backups at 4 AM
0 4 * * * find /opt/wrapper-app/backups -name "*.sql.gz" -mtime +30 -delete
```

### Off-Site Backups

For production systems, implement off-site backup replication:

```bash
# Sync backups to remote server
rsync -avz --delete /opt/wrapper-app/backups/ user@backup-server:/backups/wrapper-app/

# Or upload to cloud storage (AWS S3 example)
aws s3 sync /opt/wrapper-app/backups/ s3://your-bucket/wrapper-backups/
```

### Retention Policy

Recommended retention policy:
- **Daily backups:** Keep for 30 days
- **Weekly backups:** Keep for 90 days
- **Monthly backups:** Keep for 1 year
- **Off-site backups:** Keep indefinitely (with rotation)

## Monitoring

### Check Backup Status

```bash
# View recent backups
ls -lh /opt/wrapper-app/backups/

# View backup manifest
cat /opt/wrapper-app/backups/backup-manifest-TIMESTAMP.txt

# Check backup size
du -sh /opt/wrapper-app/backups/
```

### Test Restore Procedure

Regularly test your restore procedure:

```bash
# 1. Create a test backup
./scripts/backup.sh

# 2. Note the timestamp
ls -lt backups/ | head -n 5

# 3. Test restore in non-production environment
./scripts/restore.sh TIMESTAMP
```

## Troubleshooting

### Backup Fails

```bash
# Check Docker services are running
docker-compose ps

# Check available disk space
df -h

# Check script permissions
ls -l scripts/*.sh
chmod +x scripts/*.sh
```

### Restore Fails

```bash
# Verify backup files exist
ls -l backups/database-TIMESTAMP.sql.gz

# Check database is accessible
docker-compose exec postgres psql -U wrapper_user -d wrapper_prod -c "SELECT version();"

# View restore logs
docker-compose logs postgres
```

### Disk Space Issues

```bash
# Clean up old backups manually
find backups/ -name "*.sql.gz" -mtime +30 -delete

# Compress old backups
gzip backups/*.sql

# Move old backups to archive storage
mv backups/*.sql.gz /mnt/archive/
```

## Best Practices

1. **Test Restores Regularly:** Test restore procedure monthly
2. **Monitor Backup Size:** Watch for unexpected growth
3. **Verify Backups:** Check backup manifest for completeness
4. **Off-Site Copies:** Always maintain off-site backup copies
5. **Document Procedures:** Keep restore documentation updated
6. **Secure Backups:** Encrypt backups if they contain sensitive data
7. **Automate Monitoring:** Set up alerts for backup failures

## Security Considerations

### Backup Encryption

For sensitive data, encrypt backups:

```bash
# Encrypt backup
gpg --encrypt --recipient your-email@example.com backups/database-TIMESTAMP.sql.gz

# Decrypt backup
gpg --decrypt backups/database-TIMESTAMP.sql.gz.gpg > database-TIMESTAMP.sql.gz
```

### Access Control

```bash
# Restrict backup directory access
chmod 700 /opt/wrapper-app/backups/
chown -R $USER:$USER /opt/wrapper-app/backups/

# Restrict script access
chmod 700 /opt/wrapper-app/scripts/
chmod 700 /opt/wrapper-app/scripts/*.sh
```

### Environment Variables

Never backup `.env` files to version control. Store them securely:

```bash
# Backup environment configuration (encrypted)
gpg --encrypt .env > backups/env-backup.gpg

# Restore
gpg --decrypt backups/env-backup.gpg > .env
```

## Additional Resources

- [DEPLOYMENT.md](../DEPLOYMENT.md) - Full deployment guide
- [DOCKER_README.md](../DOCKER_README.md) - Docker configuration
- [PostgreSQL Backup Documentation](https://www.postgresql.org/docs/current/backup.html)
