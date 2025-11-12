# Security Considerations

Security best practices and considerations for the Career Lexicon Builder wrapper application.

## Table of Contents

- [Authentication and Authorization](#authentication-and-authorization)
- [API Security](#api-security)
- [Database Security](#database-security)
- [Network Security](#network-security)
- [Container Security](#container-security)
- [Secrets Management](#secrets-management)
- [SSL/TLS Configuration](#ssltls-configuration)
- [Monitoring and Logging](#monitoring-and-logging)
- [Incident Response](#incident-response)
- [Security Checklist](#security-checklist)

## Authentication and Authorization

### JWT Token Security

- **JWT Secret:** Use a strong, randomly generated secret key (minimum 64 characters)
  ```bash
  openssl rand -hex 32
  ```

- **Token Expiration:** Implement reasonable token expiration times
  - Access tokens: 1 hour
  - Refresh tokens: 7 days

- **Token Storage:** Never store tokens in localStorage (vulnerable to XSS)
  - Use httpOnly cookies
  - Set Secure flag for HTTPS
  - Set SameSite=Strict

### Password Security

- **Requirements:**
  - Minimum 12 characters
  - Mix of uppercase, lowercase, numbers, special characters
  - Password complexity validation

- **Storage:**
  - Use bcrypt for password hashing (implemented in backend)
  - Never store plain text passwords
  - Salt rounds: minimum 12

### API Key Management

- **Anthropic API Key:**
  - Store in environment variables only
  - Never commit to version control
  - Rotate keys periodically
  - Monitor usage for anomalies

## API Security

### CORS Configuration

Production CORS settings in `main.py`:

```python
# Restrict to your domain only
CORS_ORIGINS = "https://yourdomain.com"

# No wildcards in production
allow_origins=["https://yourdomain.com"],
allow_credentials=True,
```

### Rate Limiting

Nginx configuration includes rate limiting:

```nginx
# API endpoints: 10 requests/second with burst of 20
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

# General traffic: 100 requests/second with burst of 20
limit_req_zone $binary_remote_addr zone=general_limit:10m rate=100r/s;
```

Adjust based on your traffic patterns:

```nginx
location /api/ {
    limit_req zone=api_limit burst=20 nodelay;
    # ...
}
```

### Input Validation

- All user inputs are validated using Pydantic models
- SQL injection prevention through parameterized queries
- XSS prevention through proper output encoding
- File upload restrictions (type, size)

### Security Headers

Production nginx configuration includes security headers:

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; ..." always;
```

## Database Security

### Connection Security

- Use strong database passwords:
  ```bash
  openssl rand -base64 32
  ```

- Database connections use private Docker network
- No direct external access to PostgreSQL
- Use SSL for database connections in production

### Access Control

```sql
-- Create dedicated user with minimal permissions
CREATE USER wrapper_user WITH PASSWORD 'strong_password';
GRANT CONNECT ON DATABASE wrapper_prod TO wrapper_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO wrapper_user;
```

### Backup Security

- Encrypt database backups:
  ```bash
  gpg --encrypt --recipient admin@example.com backup.sql.gz
  ```

- Store backups in secure location
- Implement access controls on backup directory:
  ```bash
  chmod 700 /opt/wrapper-app/backups/
  ```

### SQL Injection Prevention

- Use SQLAlchemy ORM (prevents SQL injection)
- Never concatenate SQL queries
- Use parameterized queries for raw SQL

## Network Security

### Firewall Configuration

```bash
# Allow only necessary ports
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP (redirect to HTTPS)
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable

# Block all other incoming traffic
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

### SSH Hardening

Edit `/etc/ssh/sshd_config`:

```bash
# Disable password authentication
PasswordAuthentication no

# Disable root login
PermitRootLogin no

# Use SSH keys only
PubkeyAuthentication yes

# Restrict SSH to specific users
AllowUsers your-username

# Change default port (optional)
Port 2222
```

### DDoS Protection

- Use Cloudflare or similar CDN
- Implement rate limiting (see above)
- Monitor for unusual traffic patterns

## Container Security

### Image Security

- Use official base images (Python, Node, PostgreSQL)
- Scan images for vulnerabilities:
  ```bash
  docker scout cve backend:latest
  docker scout cve frontend:latest
  ```

- Keep base images updated
- Use specific version tags (not `latest` in production)

### Container Isolation

- Containers run on isolated Docker network
- No unnecessary exposed ports
- Use least privilege principle

### Resource Limits

Add to `docker-compose.prod.yml`:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

## Secrets Management

### Environment Variables

- Never commit `.env` to version control
- Use `.env.production.example` as template
- Set restrictive permissions:
  ```bash
  chmod 600 .env
  ```

### GitHub Secrets

Required secrets for CI/CD:

```yaml
DEPLOY_HOST         # Production server IP/domain
DEPLOY_USER         # SSH user
DEPLOY_SSH_KEY      # SSH private key
DEPLOY_PORT         # SSH port (default: 22)
```

### Rotation Schedule

- Database passwords: Every 90 days
- JWT secret: Every 90 days
- API keys: Every 180 days
- SSH keys: Every 365 days

## SSL/TLS Configuration

### Certificate Setup

Use Let's Encrypt (free, automated):

```bash
sudo certbot certonly --standalone -d yourdomain.com
```

### Strong TLS Configuration

Already implemented in `nginx.prod.conf`:

```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers HIGH:!aNULL:!MD5;
ssl_prefer_server_ciphers on;
```

### Certificate Renewal

Automate with cron:

```bash
0 3 * * * certbot renew --quiet && docker-compose restart frontend
```

### HSTS (HTTP Strict Transport Security)

Force HTTPS for 1 year:

```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

## Monitoring and Logging

### Application Logs

- Centralized logging with Docker
- Log retention: 10MB per file, 3 files
- Monitor for suspicious activity:
  ```bash
  docker-compose logs -f | grep "ERROR\|WARN"
  ```

### Security Events to Monitor

- Failed login attempts
- Unusual API usage patterns
- Database connection errors
- SSL certificate expiration
- Disk space issues

### Log Analysis

```bash
# Check for failed login attempts
docker-compose logs backend | grep "401\|403"

# Monitor API rate limiting
docker-compose logs frontend | grep "limit_req"

# Check SSL handshake errors
docker-compose logs frontend | grep "ssl"
```

### Alerting

Set up alerts for:
- Multiple failed login attempts
- Service downtime
- High error rates
- Certificate expiration (30 days before)
- Disk space low (< 20%)

## Incident Response

### Security Incident Procedure

1. **Detect:** Monitor logs and alerts
2. **Contain:** Isolate affected systems
3. **Investigate:** Analyze logs and determine scope
4. **Remediate:** Patch vulnerabilities, rotate credentials
5. **Document:** Record incident details
6. **Review:** Update security measures

### Emergency Contacts

Document key contacts:
- System administrator
- Security team
- Hosting provider support
- Incident response team

### Backup Recovery

In case of compromise:

```bash
# Stop services
docker-compose down

# Restore from clean backup
./scripts/restore.sh <last-known-good-timestamp>

# Rotate all credentials
# Update all environment variables
# Restart services
docker-compose up -d
```

## Security Checklist

### Pre-Deployment

- [ ] Strong passwords generated for all services
- [ ] SSL certificates obtained and configured
- [ ] Firewall configured and enabled
- [ ] SSH hardened (keys only, no password)
- [ ] Security headers configured in nginx
- [ ] CORS restricted to production domain
- [ ] Rate limiting configured
- [ ] Environment variables secured (chmod 600)
- [ ] Database access restricted
- [ ] Backup encryption configured

### Post-Deployment

- [ ] Verify HTTPS is working
- [ ] Test rate limiting
- [ ] Verify security headers (use securityheaders.com)
- [ ] Check for exposed secrets
- [ ] Verify backup and restore procedures
- [ ] Set up monitoring and alerting
- [ ] Document incident response procedures
- [ ] Schedule regular security reviews

### Ongoing Maintenance

- [ ] Update system packages monthly
- [ ] Update Docker images weekly
- [ ] Rotate credentials quarterly
- [ ] Review logs weekly
- [ ] Test backups monthly
- [ ] Security scan quarterly
- [ ] Penetration test annually

## Security Tools

### Recommended Tools

- **SSL Testing:** [SSL Labs](https://www.ssllabs.com/ssltest/)
- **Security Headers:** [Security Headers](https://securityheaders.com/)
- **Vulnerability Scanning:** Docker Scout, Snyk
- **Log Analysis:** ELK Stack, Grafana Loki
- **Intrusion Detection:** Fail2ban
- **WAF:** Cloudflare, AWS WAF

### Security Scanning

```bash
# Scan Docker images
docker scout cve backend:latest

# Check for exposed secrets
git secrets --scan

# Audit npm packages
cd wrapper-frontend && npm audit

# Audit Python packages
cd wrapper-backend && pip-audit
```

## Compliance Considerations

### Data Protection

- Implement data retention policies
- Allow users to delete their data
- Encrypt sensitive data at rest
- Document data processing procedures

### Privacy

- Clear privacy policy
- Consent for data collection
- Data minimization principle
- User rights (access, deletion, portability)

## Reporting Security Issues

If you discover a security vulnerability:

1. **Do NOT** open a public issue
2. Email security@yourdomain.com
3. Include detailed description
4. Allow reasonable time for response

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Nginx Security](https://nginx.org/en/docs/http/ngx_http_ssl_module.html)
- [PostgreSQL Security](https://www.postgresql.org/docs/current/security.html)
