# Corporate Office 101 - Backend API

This is the backend API for the Corporate Office 101 mobile application, built with Flask and designed to be deployed on Azure App Service.

## Features

- **User Authentication**: JWT-based authentication for tenants and property managers
- **Payment Processing**: Stripe integration for rent payments and room bookings
- **Event Management**: Create, update, and RSVP to events
- **Room Booking**: Request and approve room bookings with payment integration
- **Service Requests**: Submit and track maintenance, cleaning, and meeting requests
- **Message Board**: Post and view messages with urgent notification support
- **Building Directory**: View and manage tenant directory with interactive map

## Technology Stack

- **Framework**: Flask 3.0
- **Database**: PostgreSQL (via SQLAlchemy ORM)
- **Authentication**: Flask-JWT-Extended
- **Payment Gateway**: Stripe
- **Cloud Services**: Azure (App Service, Blob Storage, Communication Services)

## Prerequisites

- Python 3.11+
- PostgreSQL database
- Stripe account
- Azure account (for production deployment)

## Local Development Setup

### 1. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and update with your credentials:

```bash
cp .env.example .env
```

Edit `.env` and fill in the following:

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Flask secret key
- `JWT_SECRET_KEY`: JWT secret key
- `STRIPE_SECRET_KEY`: Stripe secret key
- `STRIPE_PUBLISHABLE_KEY`: Stripe publishable key
- `STRIPE_WEBHOOK_SECRET`: Stripe webhook secret
- `AZURE_STORAGE_CONNECTION_STRING`: Azure Blob Storage connection string
- `AZURE_COMMUNICATION_CONNECTION_STRING`: Azure Communication Services connection string

### 3. Initialize Database

```bash
python3 init_db.py
```

This will create all database tables and populate initial data including:
- Directory entries (30 businesses)
- Ballroom/Conference Room
- Default property manager account (info@cyberguysdmv.com / manager123)

### 4. Run Development Server

```bash
python3 app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new tenant
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/profile` - Get current user profile
- `PUT /api/auth/profile` - Update user profile

### Payments
- `GET /api/payments` - Get payment history
- `POST /api/payments/initiate` - Initiate a new payment
- `POST /api/payments/webhook` - Stripe webhook endpoint
- `GET /api/payments/status` - Get payment status summary

### Events
- `GET /api/events` - Get all events
- `POST /api/events` - Create a new event
- `PUT /api/events/<id>` - Update an event
- `DELETE /api/events/<id>` - Delete an event
- `POST /api/events/<id>/rsvp` - RSVP to an event
- `GET /api/events/<id>/rsvps` - Get event RSVPs

### Room Booking
- `GET /api/bookings/rooms` - Get all bookable rooms
- `GET /api/bookings/rooms/<id>/availability` - Check room availability
- `POST /api/bookings` - Create a booking request
- `GET /api/bookings` - Get user's bookings
- `PUT /api/bookings/<id>/approve` - Approve booking (manager only)
- `PUT /api/bookings/<id>/reject` - Reject booking (manager only)

### Service Requests
- `POST /api/servicerequests` - Submit a service request
- `GET /api/servicerequests` - Get service requests
- `GET /api/servicerequests/<id>` - Get specific request
- `PUT /api/servicerequests/<id>/status` - Update request status (manager only)
- `PUT /api/servicerequests/<id>/assign` - Assign request (manager only)

### Messages
- `GET /api/messages` - Get all messages
- `POST /api/messages` - Post a new message
- `POST /api/messages/urgent` - Post urgent message (manager only)
- `PUT /api/messages/<id>/important` - Mark message as important

### Directory
- `GET /api/directory` - Get building directory
- `GET /api/directory/locations` - Get directory with map coordinates
- `GET /api/directory/map/pdf` - Get map PDF URL

## Azure Deployment

### 1. Create Azure Resources

- Azure App Service (Python 3.11)
- Azure SQL Database (or PostgreSQL)
- Azure Blob Storage
- Azure Communication Services (for email)

### 2. Configure App Service

Set environment variables in Azure App Service Configuration:

```bash
az webapp config appsettings set --resource-group <resource-group> --name <app-name> --settings \
  DATABASE_URL="<database-url>" \
  SECRET_KEY="<secret-key>" \
  JWT_SECRET_KEY="<jwt-secret>" \
  STRIPE_SECRET_KEY="<stripe-secret>" \
  STRIPE_PUBLISHABLE_KEY="<stripe-publishable>" \
  STRIPE_WEBHOOK_SECRET="<stripe-webhook-secret>" \
  AZURE_STORAGE_CONNECTION_STRING="<storage-connection>" \
  AZURE_COMMUNICATION_CONNECTION_STRING="<communication-connection>"
```

### 3. Deploy to Azure

```bash
az webapp up --resource-group <resource-group> --name <app-name> --runtime "PYTHON:3.11"
```

### 4. Initialize Production Database

SSH into the App Service and run:

```bash
python3 init_db.py
```

## Testing

Use tools like Postman or curl to test the API endpoints. Example:

```bash
# Register a new tenant
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "tenant@example.com",
    "password": "password123",
    "business_name": "Test Business",
    "suite_number": "101"
  }'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "tenant@example.com",
    "password": "password123"
  }'
```

## Security Considerations

- All passwords are hashed using Werkzeug's security functions
- JWT tokens are used for API authentication
- CORS is enabled for cross-origin requests
- Input validation is performed on all endpoints
- Stripe webhook signatures are verified
- Role-based access control is enforced

## License

Proprietary - Corporate Office 101
