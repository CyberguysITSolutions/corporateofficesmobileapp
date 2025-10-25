# Corporate Office 101 - Project Structure

## 📁 Complete File Structure

```
corporateofficesmobileapp/
├── .github/
│   └── workflows/
│       └── azure-deploy.yml          # GitHub Actions CI/CD workflow
├── backend/
│   ├── app.py                        # Main Flask application
│   ├── models.py                     # SQLAlchemy database models
│   ├── init_db.py                    # Database initialization script
│   ├── requirements.txt              # Python dependencies
│   ├── gunicorn_config.py           # Production server configuration
│   ├── startup.sh                    # Azure App Service startup script
│   └── .env.example                  # Environment variables template
├── docs/
│   ├── AZURE_DEPLOYMENT_GUIDE.md    # Detailed Azure deployment guide
│   ├── DEPLOYMENT_CHECKLIST.md      # Pre/post deployment checklist
│   ├── app_architecture_design.md   # System architecture documentation
│   ├── database_schema_design.md    # Database schema details
│   ├── README.md                     # Backend API documentation
│   └── OfficeDirectory_and_Map.pdf  # Building floor plans
├── .gitignore                        # Git ignore rules
├── README.md                         # Main project documentation
├── QUICKSTART.md                     # Quick deployment guide
└── deploy-azure.sh                   # Automated Azure deployment script
```

## 🚀 Quick Deployment Steps

### Option 1: Automated Deployment (Recommended)

```bash
# 1. Make script executable
chmod +x deploy-azure.sh

# 2. Run automated deployment
./deploy-azure.sh

# 3. Deploy code
cd backend
zip -r ../deploy.zip . -x "*.git*" -x "*venv*" -x "*__pycache__*"
cd ..
az webapp deployment source config-zip \
  --resource-group corporate-office-rg \
  --name corporate-office-api \
  --src deploy.zip

# 4. Initialize database
az webapp ssh --resource-group corporate-office-rg --name corporate-office-api
python init_db.py
```

### Option 2: GitHub Actions (Continuous Deployment)

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/CyberguysITSolutions/corporateofficesmobileapp.git
git push -u origin main

# 2. Configure GitHub Secrets (in repository settings):
# - AZURE_WEBAPP_PUBLISH_PROFILE
# - VITE_API_URL
# - VITE_STRIPE_PUBLISHABLE_KEY
# - AZURE_STATIC_WEB_APPS_API_TOKEN

# 3. Push to trigger deployment
git push origin main
```

## 📋 What's Included

### Backend API (Flask/Python)
- ✅ User authentication (JWT-based)
- ✅ Payment processing (Stripe integration)
- ✅ Event management
- ✅ Room booking system
- ✅ Service request tracking
- ✅ Message board
- ✅ Building directory (30+ businesses)
- ✅ File upload support
- ✅ Role-based access control

### Database (PostgreSQL)
- ✅ 11 fully designed tables
- ✅ Relationships and constraints
- ✅ Pre-populated directory data
- ✅ Default property manager account

### Azure Integration
- ✅ App Service deployment
- ✅ PostgreSQL Flexible Server
- ✅ Blob Storage configuration
- ✅ Environment variable management
- ✅ GitHub Actions workflow

### Documentation
- ✅ Quick start guide
- ✅ Detailed deployment guide
- ✅ Architecture documentation
- ✅ Database schema
- ✅ API documentation
- ✅ Deployment checklist

## 🔑 Key Files Explained

### `backend/app.py`
Main Flask application with all API endpoints:
- Authentication routes (`/api/auth/*`)
- Payment routes (`/api/payments/*`)
- Event routes (`/api/events/*`)
- Directory routes (`/api/directory/*`)
- Health check (`/api/health`)

### `backend/models.py`
SQLAlchemy models for:
- Users, Tenants, PropertyManagers
- Payments, Events, Bookings
- ServiceRequests, Messages
- DirectoryEntries

### `backend/init_db.py`
Database initialization script that:
- Creates all tables
- Populates 30+ directory entries from the PDF
- Creates default property manager account
- Sets up the Ballroom/Conference Room

### `.github/workflows/azure-deploy.yml`
GitHub Actions workflow for automated deployment:
- Backend Python app deployment
- Frontend build and deployment
- Environment configuration

### `deploy-azure.sh`
Automated Azure infrastructure setup:
- Resource group creation
- PostgreSQL database provisioning
- Storage account setup
- App Service deployment
- Initial configuration

## 🎯 Next Steps

1. **Deploy the Backend**
   ```bash
   ./deploy-azure.sh
   ```

2. **Add Stripe Configuration**
   ```bash
   az webapp config appsettings set \
     --resource-group corporate-office-rg \
     --name corporate-office-api \
     --settings STRIPE_SECRET_KEY="sk_test_..."
   ```

3. **Initialize Database**
   ```bash
   az webapp ssh --resource-group corporate-office-rg --name corporate-office-api
   python init_db.py
   ```

4. **Test the API**
   ```bash
   curl https://corporate-office-api.azurewebsites.net/api/health
   ```

5. **Deploy Frontend** (Coming Next)
   - React web application
   - Azure Static Web Apps
   - Stripe payment UI

## 📊 Database Overview

The system includes these main entities:

| Table | Records | Description |
|-------|---------|-------------|
| Users | Dynamic | Authentication & roles |
| Tenants | Dynamic | Business information |
| DirectoryEntries | 86 | Building directory (from PDF) |
| Rooms | 1 | Ballroom/Conference Room |
| Payments | Dynamic | Rent payments |
| Events | Dynamic | Building events |
| Bookings | Dynamic | Room reservations |
| ServiceRequests | Dynamic | Maintenance tickets |
| Messages | Dynamic | Announcement board |

## 🔐 Security Features

- ✅ JWT authentication tokens
- ✅ Password hashing (Werkzeug)
- ✅ Role-based access control (RBAC)
- ✅ CORS configuration
- ✅ Input validation
- ✅ Stripe secure payments
- ✅ HTTPS-only in production
- ✅ Environment variable protection

## 📦 Dependencies

### Python (backend/requirements.txt)
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-JWT-Extended 4.5.3
- psycopg2-binary 2.9.9
- stripe 7.4.0
- gunicorn 21.2.0

## 🌐 API Endpoints Summary

### Authentication
- `POST /api/auth/register` - Register tenant
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update profile

### Payments
- `GET /api/payments` - Payment history
- `POST /api/payments/initiate` - Initiate payment
- `POST /api/payments/webhook` - Stripe webhook

### Events
- `GET /api/events` - List events
- `POST /api/events` - Create event

### Directory
- `GET /api/directory` - Building directory
- `GET /api/directory/map/pdf` - Map PDF URL

### Health
- `GET /api/health` - Health check
- `GET /` - API info

## 💰 Cost Breakdown

| Service | Tier | Monthly Cost |
|---------|------|--------------|
| App Service | B1 Basic | $13.14 |
| PostgreSQL | B1ms Burstable | $12.41 |
| Storage | Standard LRS | $1.00 |
| Static Web Apps | Free | $0.00 |
| **TOTAL** | | **~$26.55/month** |

## 📞 Support

- **Email**: info@cyberguysdmv.com
- **Documentation**: See `/docs` folder
- **Issues**: GitHub Issues

## ✅ Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] Azure account with active subscription
- [ ] Azure CLI installed and configured
- [ ] Stripe account with API keys
- [ ] GitHub repository created
- [ ] Read QUICKSTART.md
- [ ] Reviewed security settings

## 🎉 What's Working

After deployment, you'll have:

1. ✅ Full REST API running on Azure
2. ✅ PostgreSQL database with schema
3. ✅ 86 directory entries populated
4. ✅ Payment processing via Stripe
5. ✅ JWT authentication
6. ✅ Default property manager account
7. ✅ Health monitoring
8. ✅ Automated deployment pipeline

## 📝 Default Credentials

**Property Manager:**
- Email: `info@cyberguysdmv.com`
- Password: `manager123`

⚠️ **Change immediately in production!**

## 🚧 Coming Soon

- [ ] React frontend web application
- [ ] React Native mobile apps (iOS/Android)
- [ ] Push notifications
- [ ] Email notifications
- [ ] Advanced analytics
- [ ] Tenant mobile app features

---

**Ready to deploy?** Start with `QUICKSTART.md`!
