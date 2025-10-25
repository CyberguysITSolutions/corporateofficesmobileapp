# Deployment Checklist for Corporate Office 101 Tenant Portal

Use this checklist to ensure all steps are completed before and after deployment.

## Pre-Deployment

### Azure Account Setup
- [ ] Azure subscription is active and has sufficient credits
- [ ] Azure CLI is installed and configured
- [ ] Logged in to Azure CLI (`az login`)
- [ ] Selected correct subscription (`az account set`)

### Third-Party Services
- [ ] Stripe account created
- [ ] Stripe API keys obtained (test and live)
- [ ] Stripe webhook endpoint configured
- [ ] Email service configured (if using Azure Communication Services)

### Code Preparation
- [ ] All environment variables documented
- [ ] Database schema finalized
- [ ] API endpoints tested locally
- [ ] Frontend builds successfully
- [ ] All dependencies listed in requirements.txt and package.json
- [ ] Security vulnerabilities checked (`npm audit`, `pip check`)

### Configuration Files
- [ ] `.env.example` files created for both frontend and backend
- [ ] `requirements.txt` includes all Python dependencies
- [ ] `package.json` includes all Node.js dependencies
- [ ] `gunicorn_config.py` configured for production
- [ ] CORS settings configured correctly

## Azure Resource Creation

### Resource Group
- [ ] Resource group created
- [ ] Appropriate region selected (e.g., East US)

### Database
- [ ] PostgreSQL flexible server created
- [ ] Database created within the server
- [ ] Firewall rules configured
- [ ] Admin credentials stored securely
- [ ] Connection string tested

### Storage
- [ ] Storage account created
- [ ] Blob container created for uploads
- [ ] Public access level set appropriately
- [ ] Connection string obtained

### App Service (Backend)
- [ ] App Service plan created
- [ ] Web app created with Python 3.11 runtime
- [ ] Deployment source configured (Git, GitHub Actions, etc.)
- [ ] All environment variables set
- [ ] HTTPS-only enabled
- [ ] Managed identity enabled (optional but recommended)

### Static Web App (Frontend)
- [ ] Static Web App created
- [ ] Deployment source configured
- [ ] Custom domain configured (if applicable)
- [ ] SSL certificate configured

## Deployment

### Backend Deployment
- [ ] Code pushed to Azure
- [ ] Deployment completed successfully
- [ ] Application starts without errors
- [ ] Health endpoint responds (`/api/health`)
- [ ] Database migrations run successfully
- [ ] Initial data seeded (directory, rooms, property manager)

### Frontend Deployment
- [ ] Environment variables updated with production API URL
- [ ] Build completed successfully
- [ ] Static files deployed to Azure
- [ ] Application loads in browser
- [ ] API calls work correctly

## Post-Deployment Testing

### Authentication
- [ ] User registration works
- [ ] User login works
- [ ] JWT tokens are issued correctly
- [ ] Protected routes require authentication
- [ ] Logout works correctly

### Payments
- [ ] Payment form loads
- [ ] Stripe Elements render correctly
- [ ] Test payment succeeds (use Stripe test card: 4242 4242 4242 4242)
- [ ] Payment history displays
- [ ] Recurring payment setup works
- [ ] Webhook receives payment events

### Events
- [ ] Event creation works
- [ ] Events display in calendar
- [ ] Event details can be viewed
- [ ] Event documents can be uploaded
- [ ] RSVP functionality works (if enabled)

### Room Booking
- [ ] Booking form loads
- [ ] Available times display correctly
- [ ] Booking submission works
- [ ] Approval workflow functions
- [ ] Booking confirmation sent
- [ ] Property manager receives notification

### Service Requests
- [ ] Request form loads
- [ ] Request submission works
- [ ] Photo upload works
- [ ] Request status tracking works
- [ ] Property manager receives notification
- [ ] Status updates reflect correctly

### Messages
- [ ] Message board loads
- [ ] Messages can be posted
- [ ] Urgent messages require admin approval
- [ ] Message importance marking works
- [ ] Notifications sent for urgent messages

### Directory
- [ ] Building map PDF displays correctly
- [ ] Tenant directory loads
- [ ] All 30 tenants listed
- [ ] Suite numbers correct
- [ ] PDF download works
- [ ] Open in new tab works

## Security Checks

- [ ] HTTPS enforced on all endpoints
- [ ] CORS configured correctly (no wildcard in production)
- [ ] SQL injection protection verified
- [ ] XSS protection enabled
- [ ] CSRF protection enabled
- [ ] Rate limiting configured (if applicable)
- [ ] Sensitive data encrypted in database
- [ ] API keys not exposed in frontend code
- [ ] Error messages don't leak sensitive information

## Monitoring and Logging

- [ ] Application Insights configured
- [ ] Log streaming enabled
- [ ] Error tracking configured
- [ ] Performance monitoring enabled
- [ ] Alerts configured for critical errors
- [ ] Uptime monitoring configured

## Documentation

- [ ] README.md updated with deployment info
- [ ] API documentation complete
- [ ] User guide created (if needed)
- [ ] Admin guide created
- [ ] Environment variables documented
- [ ] Troubleshooting guide created

## Backup and Recovery

- [ ] Database backup schedule configured
- [ ] Backup restoration tested
- [ ] Disaster recovery plan documented
- [ ] Code repository backed up
- [ ] Configuration backed up

## Performance Optimization

- [ ] Frontend assets minified
- [ ] Images optimized
- [ ] CDN configured (if applicable)
- [ ] Caching headers set
- [ ] Database queries optimized
- [ ] API response times acceptable

## Compliance and Legal

- [ ] Privacy policy created
- [ ] Terms of service created
- [ ] GDPR compliance reviewed (if applicable)
- [ ] Data retention policy defined
- [ ] User consent mechanisms implemented

## User Acceptance Testing

- [ ] Property manager account created
- [ ] Test tenant accounts created
- [ ] All features tested by end users
- [ ] Feedback collected and addressed
- [ ] User training completed

## Go-Live

- [ ] DNS records updated (if using custom domain)
- [ ] SSL certificates verified
- [ ] All stakeholders notified
- [ ] Support contact information published
- [ ] Monitoring dashboard accessible
- [ ] On-call support arranged

## Post-Launch

- [ ] Monitor error rates for first 24 hours
- [ ] Check performance metrics
- [ ] Review user feedback
- [ ] Address any critical issues immediately
- [ ] Schedule follow-up review meeting

## Maintenance Schedule

- [ ] Weekly: Review logs and error reports
- [ ] Monthly: Check for security updates
- [ ] Monthly: Review and optimize database
- [ ] Quarterly: Review and update dependencies
- [ ] Quarterly: Conduct security audit
- [ ] Annually: Review and renew SSL certificates
- [ ] Annually: Review Azure resource costs and optimize

## Emergency Contacts

- **Property Manager**: info@cyberguysdmv.com
- **Azure Support**: [Azure Portal](https://portal.azure.com)
- **Stripe Support**: https://support.stripe.com
- **Development Team**: [Your Contact Info]

## Notes

Use this section to track any deployment-specific notes or issues encountered:

---

**Deployment Date**: _______________

**Deployed By**: _______________

**Version**: _______________

**Notes**:
