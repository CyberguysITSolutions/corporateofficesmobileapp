# Azure Deployment Guide for Corporate Office 101 Tenant Portal

This guide provides step-by-step instructions for deploying the Corporate Office 101 Tenant Portal application to Microsoft Azure.

## Prerequisites

Before you begin, ensure you have:

1. **Azure Account**: An active Microsoft Azure subscription
2. **Azure CLI**: Installed on your local machine ([Download here](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli))
3. **Git**: Installed for version control
4. **Node.js and npm**: For building the frontend
5. **Python 3.11**: For running the backend locally

## Architecture Overview

The application consists of two main components:

1. **Backend API**: Flask application deployed to Azure App Service (Linux)
2. **Frontend Web App**: React application deployed to Azure Static Web Apps
3. **Database**: Azure Database for PostgreSQL
4. **Storage**: Azure Blob Storage for file uploads (PDF maps, event documents, etc.)

## Step 1: Set Up Azure Resources

### 1.1 Login to Azure

```bash
az login
```

### 1.2 Create a Resource Group

```bash
az group create --name corporate-office-rg --location eastus
```

### 1.3 Create PostgreSQL Database

```bash
# Create PostgreSQL server
az postgres flexible-server create \
  --resource-group corporate-office-rg \
  --name corporate-office-db \
  --location eastus \
  --admin-user dbadmin \
  --admin-password <YOUR_SECURE_PASSWORD> \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --version 14 \
  --storage-size 32

# Create database
az postgres flexible-server db create \
  --resource-group corporate-office-rg \
  --server-name corporate-office-db \
  --database-name tenantportal

# Configure firewall to allow Azure services
az postgres flexible-server firewall-rule create \
  --resource-group corporate-office-rg \
  --name corporate-office-db \
  --rule-name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

### 1.4 Create Azure Storage Account

```bash
# Create storage account
az storage account create \
  --name corporateofficesa \
  --resource-group corporate-office-rg \
  --location eastus \
  --sku Standard_LRS

# Create blob container for uploads
az storage container create \
  --name uploads \
  --account-name corporateofficesa \
  --public-access blob
```

## Step 2: Deploy Backend API

### 2.1 Create App Service Plan

```bash
az appservice plan create \
  --name corporate-office-plan \
  --resource-group corporate-office-rg \
  --is-linux \
  --sku B1
```

### 2.2 Create Web App

```bash
az webapp create \
  --resource-group corporate-office-rg \
  --plan corporate-office-plan \
  --name corporate-office-api \
  --runtime "PYTHON:3.11"
```

### 2.3 Configure Environment Variables

```bash
# Database URL
az webapp config appsettings set \
  --resource-group corporate-office-rg \
  --name corporate-office-api \
  --settings DATABASE_URL="postgresql://dbadmin:<PASSWORD>@corporate-office-db.postgres.database.azure.com/tenantportal"

# JWT Secret Key (generate a secure random string)
az webapp config appsettings set \
  --resource-group corporate-office-rg \
  --name corporate-office-api \
  --settings JWT_SECRET_KEY="<YOUR_SECURE_JWT_SECRET>"

# Stripe Keys
az webapp config appsettings set \
  --resource-group corporate-office-rg \
  --name corporate-office-api \
  --settings STRIPE_SECRET_KEY="<YOUR_STRIPE_SECRET_KEY>"

az webapp config appsettings set \
  --resource-group corporate-office-rg \
  --name corporate-office-api \
  --settings STRIPE_WEBHOOK_SECRET="<YOUR_STRIPE_WEBHOOK_SECRET>"

# CORS Origins (your frontend URL)
az webapp config appsettings set \
  --resource-group corporate-office-rg \
  --name corporate-office-api \
  --settings CORS_ORIGINS="https://corporate-office-portal.azurestaticapps.net"

# Flask Environment
az webapp config appsettings set \
  --resource-group corporate-office-rg \
  --name corporate-office-api \
  --settings FLASK_ENV="production"
```

### 2.4 Deploy Backend Code

```bash
cd backend

# Create a .deployment file
echo "[config]
command = bash deploy.sh" > .deployment

# Create deploy.sh script
cat > deploy.sh << 'EOF'
#!/bin/bash
set -e

echo "Installing Python dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Running database migrations..."
flask db upgrade

echo "Deployment complete!"
EOF

chmod +x deploy.sh

# Deploy using Git
git init
git add .
git commit -m "Initial backend deployment"

# Get deployment credentials
az webapp deployment source config-local-git \
  --name corporate-office-api \
  --resource-group corporate-office-rg

# Add Azure remote and push
git remote add azure <GIT_URL_FROM_PREVIOUS_COMMAND>
git push azure main
```

## Step 3: Deploy Frontend

### 3.1 Build Frontend

```bash
cd ../frontend

# Update .env with production API URL
echo "VITE_API_URL=https://corporate-office-api.azurewebsites.net/api
VITE_STRIPE_PUBLISHABLE_KEY=<YOUR_STRIPE_PUBLISHABLE_KEY>" > .env

# Build the application
pnpm install
pnpm run build
```

### 3.2 Deploy to Azure Static Web Apps

```bash
# Install Azure Static Web Apps CLI
npm install -g @azure/static-web-apps-cli

# Create Static Web App
az staticwebapp create \
  --name corporate-office-portal \
  --resource-group corporate-office-rg \
  --location eastus2

# Deploy the built application
cd dist
az staticwebapp deploy \
  --app-name corporate-office-portal \
  --resource-group corporate-office-rg \
  --no-use-keychain
```

Alternatively, you can use GitHub Actions for automated deployment:

1. Push your code to a GitHub repository
2. In Azure Portal, go to your Static Web App
3. Connect it to your GitHub repository
4. Azure will automatically set up a GitHub Actions workflow

## Step 4: Initialize Database

After deployment, initialize the database with the directory data:

```bash
# SSH into the App Service
az webapp ssh --resource-group corporate-office-rg --name corporate-office-api

# Run the initialization script
python init_db.py
```

## Step 5: Configure Stripe Webhooks

1. Go to your Stripe Dashboard
2. Navigate to Developers > Webhooks
3. Add a new endpoint: `https://corporate-office-api.azurewebsites.net/api/payments/webhook`
4. Select events to listen for: `payment_intent.succeeded`, `payment_intent.payment_failed`
5. Copy the webhook signing secret and update the Azure App Settings

## Step 6: Configure Custom Domain (Optional)

### 6.1 For Backend API

```bash
# Add custom domain
az webapp config hostname add \
  --webapp-name corporate-office-api \
  --resource-group corporate-office-rg \
  --hostname api.corporateoffice101.com

# Enable HTTPS
az webapp config ssl bind \
  --name corporate-office-api \
  --resource-group corporate-office-rg \
  --certificate-thumbprint <THUMBPRINT> \
  --ssl-type SNI
```

### 6.2 For Frontend

```bash
# Add custom domain to Static Web App
az staticwebapp hostname set \
  --name corporate-office-portal \
  --resource-group corporate-office-rg \
  --hostname www.corporateoffice101.com
```

## Step 7: Set Up Monitoring and Logging

### 7.1 Enable Application Insights

```bash
# Create Application Insights
az monitor app-insights component create \
  --app corporate-office-insights \
  --location eastus \
  --resource-group corporate-office-rg

# Link to App Service
az webapp config appsettings set \
  --resource-group corporate-office-rg \
  --name corporate-office-api \
  --settings APPINSIGHTS_INSTRUMENTATIONKEY="<INSTRUMENTATION_KEY>"
```

### 7.2 Configure Log Streaming

```bash
# Enable application logging
az webapp log config \
  --name corporate-office-api \
  --resource-group corporate-office-rg \
  --application-logging filesystem \
  --level information

# Stream logs
az webapp log tail \
  --name corporate-office-api \
  --resource-group corporate-office-rg
```

## Step 8: Security Best Practices

1. **Enable HTTPS Only**:
   ```bash
   az webapp update \
     --resource-group corporate-office-rg \
     --name corporate-office-api \
     --https-only true
   ```

2. **Configure Managed Identity** for accessing Azure resources without storing credentials

3. **Set up Azure Key Vault** for storing sensitive configuration

4. **Enable Azure DDoS Protection** for your resources

5. **Configure Web Application Firewall (WAF)** for additional security

## Step 9: Testing

After deployment, test the following:

1. **Frontend Access**: Visit your Static Web App URL
2. **API Health**: Check `https://corporate-office-api.azurewebsites.net/api/health`
3. **User Registration**: Create a test tenant account
4. **Login**: Verify authentication works
5. **Payment Flow**: Test Stripe integration (use test mode)
6. **File Uploads**: Test event document uploads
7. **PDF Viewing**: Verify the building map displays correctly

## Troubleshooting

### Common Issues

1. **Database Connection Errors**:
   - Verify firewall rules allow Azure services
   - Check DATABASE_URL format
   - Ensure SSL mode is configured correctly

2. **CORS Errors**:
   - Verify CORS_ORIGINS includes your frontend URL
   - Check that the frontend is using the correct API URL

3. **Stripe Webhook Failures**:
   - Verify webhook secret is correct
   - Check that the endpoint is publicly accessible
   - Review Stripe dashboard for webhook delivery attempts

4. **Build Failures**:
   - Check that all environment variables are set
   - Verify Python/Node versions match requirements
   - Review deployment logs in Azure Portal

## Maintenance

### Updating the Application

**Backend**:
```bash
cd backend
git add .
git commit -m "Update backend"
git push azure main
```

**Frontend**:
```bash
cd frontend
pnpm run build
az staticwebapp deploy --app-name corporate-office-portal
```

### Database Backups

Azure Database for PostgreSQL automatically creates backups. To manually create a backup:

```bash
az postgres flexible-server backup create \
  --resource-group corporate-office-rg \
  --name corporate-office-db \
  --backup-name manual-backup-$(date +%Y%m%d)
```

## Cost Estimation

Approximate monthly costs (as of 2025):

- **App Service (B1)**: ~$13/month
- **PostgreSQL (Burstable B1ms)**: ~$12/month
- **Static Web Apps (Free tier)**: $0/month
- **Storage Account**: ~$1/month (for small usage)
- **Application Insights**: ~$5/month (for basic monitoring)

**Total**: ~$31/month (may vary based on usage)

## Support

For issues or questions:
- Azure Support: https://azure.microsoft.com/support/
- Stripe Support: https://support.stripe.com/
- Application Issues: Contact info@cyberguysdmv.com

## Additional Resources

- [Azure App Service Documentation](https://docs.microsoft.com/en-us/azure/app-service/)
- [Azure Static Web Apps Documentation](https://docs.microsoft.com/en-us/azure/static-web-apps/)
- [Azure Database for PostgreSQL Documentation](https://docs.microsoft.com/en-us/azure/postgresql/)
- [Stripe API Documentation](https://stripe.com/docs/api)
