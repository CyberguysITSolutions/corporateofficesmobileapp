# Corporate Office 101 - Tenant Portal

A comprehensive web and mobile application for managing office building operations, including rent payments, event management, room bookings, service requests, and building directory.

## 🏢 Project Overview

This application serves the Corporate Office 101 building at Buford Rd/8014 Midlothian Tnpk, providing tenants with a modern platform to:

- **Make Rent Payments**: Secure payment processing via Stripe
- **Manage Events**: Create, RSVP, and track building events
- **Book Conference Rooms**: Request and manage room bookings
- **Submit Service Requests**: Maintenance, cleaning, and meeting requests
- **View Building Directory**: Interactive map with 30+ tenant listings
- **Receive Notifications**: Urgent messages and announcements

## 🏗️ Architecture

### Backend (Python/Flask)
- **Framework**: Flask 3.0
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT-based authentication
- **Payment Processing**: Stripe API integration
- **Hosting**: Azure App Service (Linux)

### Frontend (React)
- **Framework**: React with Vite
- **UI Library**: Tailwind CSS
- **Hosting**: Azure Static Web Apps
- **Mobile**: React Native (planned)

### Azure Services
- **App Service**: Backend API hosting
- **PostgreSQL**: Flexible Server database
- **Blob Storage**: File uploads (PDFs, images)
- **Static Web Apps**: Frontend hosting
- **Communication Services**: Email notifications (planned)

## 📋 Prerequisites

- **Azure Account**: Active subscription
- **Azure CLI**: For resource management
- **Python 3.11+**: Backend development
- **Node.js 18+**: Frontend development
- **PostgreSQL**: Local development database
- **Stripe Account**: Payment processing
- **Git**: Version control

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/CyberguysITSolutions/corporateofficesmobileapp.git
cd corporateofficesmobileapp
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python init_db.py

# Run development server
python app.py
```

The API will be available at `http://localhost:5000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your API URL

# Run development server
npm run dev
```

The web app will be available at `http://localhost:5173`

## 📦 Deployment

### Deploy to Azure

The project includes GitHub Actions workflows for automated deployment.

#### Step 1: Set up Azure Resources

```bash
# Login to Azure
az login

# Create resource group
az group create --name corporate-office-rg --location eastus

# Create PostgreSQL database
az postgres flexible-server create \
  --resource-group corporate-office-rg \
  --name corporate-office-db \
  --location eastus \
  --admin-user dbadmin \
  --admin-password <YOUR_PASSWORD>

# Create App Service
az webapp up \
  --resource-group corporate-office-rg \
  --name corporate-office-api \
  --runtime "PYTHON:3.11"
```

See [AZURE_DEPLOYMENT_GUIDE.md](docs/AZURE_DEPLOYMENT_GUIDE.md) for detailed instructions.

#### Step 2: Configure GitHub Secrets

Add these secrets to your GitHub repository (Settings > Secrets and variables > Actions):

- `AZURE_WEBAPP_PUBLISH_PROFILE`: Download from Azure Portal
- `AZURE_STATIC_WEB_APPS_API_TOKEN`: From Static Web App
- `VITE_API_URL`: Your backend API URL
- `VITE_STRIPE_PUBLISHABLE_KEY`: Stripe publishable key

#### Step 3: Push to Deploy

```bash
git add .
git commit -m "Initial deployment"
git push origin main
```

GitHub Actions will automatically deploy both backend and frontend.

## 📚 Documentation

- [Architecture Design](docs/app_architecture_design.md)
- [Database Schema](docs/database_schema_design.md)
- [Azure Deployment Guide](docs/AZURE_DEPLOYMENT_GUIDE.md)
- [Deployment Checklist](docs/DEPLOYMENT_CHECKLIST.md)
- [API Documentation](backend/README.md)

## 🔧 Configuration

### Backend Environment Variables

```env
DATABASE_URL=postgresql://user:pass@host:5432/db
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
CORS_ORIGINS=https://your-frontend-url.com
```

### Frontend Environment Variables

```env
VITE_API_URL=https://your-api-url.azurewebsites.net/api
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 📊 Database Schema

The application uses PostgreSQL with the following main entities:

- **Users**: Authentication and roles
- **Tenants**: Business information and preferences
- **Payments**: Rent payment transactions
- **Events**: Building events and RSVPs
- **Bookings**: Conference room reservations
- **ServiceRequests**: Maintenance and support tickets
- **Messages**: Announcement board
- **DirectoryEntries**: Building directory with 30+ businesses

## 🔐 Security

- JWT-based authentication with secure token management
- Password hashing with Werkzeug
- HTTPS-only in production
- CORS configuration for API protection
- Input validation and sanitization
- Stripe secure payment processing
- Role-based access control (RBAC)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

Proprietary - Corporate Office 101

## 📧 Contact

**Property Management**: info@cyberguysdmv.com

**Technical Support**: [Create an issue](https://github.com/CyberguysITSolutions/corporateofficesmobileapp/issues)

## 🎯 Roadmap

- [x] Backend API development
- [x] Database schema design
- [x] Authentication system
- [x] Payment processing
- [ ] Frontend web application
- [ ] React Native mobile apps
- [ ] Push notifications
- [ ] Email notifications
- [ ] Advanced reporting
- [ ] Tenant portal enhancements

## 📱 Mobile Apps

React Native mobile applications for iOS and Android are planned for future releases.

## 💰 Cost Estimate

Approximate monthly Azure costs:

- App Service (B1): $13/month
- PostgreSQL (Burstable B1ms): $12/month
- Static Web Apps (Free tier): $0/month
- Storage Account: $1/month
- **Total**: ~$26/month

## 🏆 Acknowledgments

- Built for Corporate Office 101
- Developed by CyberGuys IT Solutions
- Powered by Microsoft Azure
