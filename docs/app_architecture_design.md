# Application Architecture Design

## 1. Overview

This document outlines the proposed architecture for the cross-platform mobile application for Corporate Office 101 Buford Rd/8014 Midlothian Tnpk. The application will enable tenants to manage rent payments, events, room bookings, service requests, urgent notifications, and access an interactive building map and directory. The solution will comprise a Python-based backend API, a JavaScript-based cross-platform frontend, and will be hosted on Microsoft Azure.

## 2. High-Level Architecture

```mermaid
graph TD
    A[Mobile App (iOS/Android)] -->|API Calls| B(Frontend - React Native/Web)
    B -->|HTTPS/JSON| C(Backend API - Python/Flask)
    C -->|Database Queries| D(Azure SQL Database)
    C -->|File Storage| E(Azure Blob Storage)
    C -->|Notifications| F(Azure Notification Hubs)
    C -->|Payment Gateway| G(Stripe API)
    H[Web App] --> B
```

## 3. Component Breakdown

### 3.1. Frontend (Client-Side)

*   **Technology**: React Native (for iOS/Android) and React (for Web). This allows for a single codebase for all three platforms, reducing development time and ensuring consistency.
*   **Features**: 
    *   User Authentication (Sign-up, Login, Password Reset)
    *   Tenant Dashboard (overview of payments, events, requests)
    *   Rent Payment Interface (Stripe integration)
    *   Event Calendar (view, create, RSVP)
    *   Room Booking Interface (view availability, book, manage)
    *   Service Request Form (submit, track status, photo upload)
    *   Message Board (view urgent messages, post general messages)
    *   Interactive Map & Directory (display PDF, clickable locations, tenant details)
    *   User Profile Management
*   **Deployment**: Web app deployed as a static site on Azure Static Web Apps or Azure App Service. Mobile apps distributed via Apple App Store and Google Play Store.

### 3.2. Backend (Server-Side)

*   **Technology**: Python with Flask (lightweight and flexible) or Django (more batteries-included, suitable for complex applications). Given the features, Flask with extensions or Django REST Framework would be appropriate.
*   **Deployment**: Azure App Service (for hosting the Python API).
*   **Key Modules/Services**:
    *   **Authentication & Authorization**: User registration, login, role-based access control (tenant, property manager).
    *   **User Management**: CRUD operations for tenant and property manager profiles.
    *   **Payment Processing**: Integration with Stripe API for rent payments, webhooks for payment status updates.
    *   **Event Management**: CRUD for events, RSVP tracking.
    *   **Room Booking**: Manage room availability, booking requests, approval workflow.
    *   **Service Request Management**: Submit requests, track status, assign to personnel.
    *   **Message Board**: Post and retrieve messages, urgent message flagging.
    *   **File Management**: Handle PDF map and event document uploads/downloads.
    *   **Notification Service**: Send email notifications (e.g., payment reminders, request updates) and push notifications (urgent messages).

### 3.3. Database

*   **Technology**: Azure SQL Database (managed relational database service).
*   **Schema (Conceptual)**:
    *   `Users`: `id`, `email`, `password_hash`, `role` (tenant/manager), `created_at`, `updated_at`
    *   `Tenants`: `id`, `user_id` (FK), `business_name`, `unit_number`, `contact_info`, `email_notifications_enabled`
    *   `PropertyManagers`: `id`, `user_id` (FK), `name`, `email`
    *   `Payments`: `id`, `tenant_id` (FK), `amount`, `due_date`, `paid_date`, `status`, `stripe_charge_id`, `is_recurring`
    *   `Events`: `id`, `title`, `description`, `date`, `time`, `location`, `contact_person`, `uploaded_documents` (JSON array of file paths), `requires_rsvp`
    *   `EventRSVPs`: `id`, `event_id` (FK), `tenant_id` (FK), `status`
    *   `Rooms`: `id`, `name`, `hourly_rate`
    *   `Bookings`: `id`, `room_id` (FK), `tenant_id` (FK), `start_time`, `end_time`, `duration`, `purpose`, `attendees`, `status` (pending/approved/rejected), `manager_approval_id` (FK to PropertyManagers)
    *   `ServiceRequests`: `id`, `tenant_id` (FK), `type` (maintenance/cleaning/meeting), `description`, `urgency`, `photo_url`, `status` (new/in_progress/resolved), `assigned_to_id` (FK to PropertyManagers), `created_at`, `updated_at`
    *   `Messages`: `id`, `sender_id` (FK to Users), `recipient_type` (all/tenant), `content`, `is_urgent`, `is_important`, `created_at`, `expires_at`
    *   `DirectoryEntries`: `id`, `suite_number`, `business_name`, `map_coordinates` (for interactive map, to be determined)

### 3.4. Azure Services

*   **Azure App Service**: For hosting the Python backend API. Provides scalability, load balancing, and easy deployment.
*   **Azure SQL Database**: Managed relational database for storing all application data. Offers high availability and performance.
*   **Azure Blob Storage**: For storing static assets like the map PDF, uploaded event documents, and service request photos. Provides scalable and cost-effective object storage.
*   **Azure Notification Hubs**: For sending push notifications to mobile devices (iOS and Android) for urgent messages.
*   **Azure SendGrid/Azure Communication Services**: For sending email notifications (e.g., payment reminders, service request updates, booking approvals).
*   **Azure Active Directory B2C (Optional)**: For advanced user authentication and identity management, if more complex scenarios arise.

## 4. API Endpoints (Conceptual)

### User/Tenant Management
*   `POST /api/register` (Tenant sign-up)
*   `POST /api/login`
*   `GET /api/profile`
*   `PUT /api/profile`
*   `GET /api/directory` (Tenant directory)

### Payments
*   `GET /api/payments` (Tenant payment history)
*   `POST /api/payments/initiate` (Initiate new payment via Stripe)
*   `POST /api/payments/webhook` (Stripe webhook for status updates)
*   `GET /api/payments/status` (Check payment status)

### Events
*   `GET /api/events` (List all events)
*   `POST /api/events` (Create new event - tenants)
*   `PUT /api/events/{id}` (Update event - tenants)
*   `DELETE /api/events/{id}` (Delete event - tenants)
*   `POST /api/events/{id}/rsvp` (RSVP to an event)
*   `GET /api/events/{id}/rsvps` (View RSVPs - event creator/manager)

### Room Booking
*   `GET /api/rooms` (List bookable rooms)
*   `GET /api/rooms/{id}/availability` (Check room availability)
*   `POST /api/bookings` (Request a room booking - tenants)
*   `GET /api/bookings` (View tenant's bookings)
*   `PUT /api/bookings/{id}/approve` (Approve booking - manager)
*   `PUT /api/bookings/{id}/reject` (Reject booking - manager)

### Service Requests
*   `POST /api/servicerequests` (Submit new request - tenants)
*   `GET /api/servicerequests` (View tenant's requests)
*   `GET /api/servicerequests/{id}` (View specific request)
*   `PUT /api/servicerequests/{id}/status` (Update request status - manager)
*   `PUT /api/servicerequests/{id}/assign` (Assign request - manager)

### Message Board
*   `GET /api/messages` (Retrieve all messages)
*   `POST /api/messages` (Post new message - tenants/manager)
*   `POST /api/messages/urgent` (Post urgent message - manager only, with admin approval for tenants)
*   `PUT /api/messages/{id}/important` (Mark message as important - tenants)

### Map & Directory
*   `GET /api/map/pdf` (Retrieve map PDF URL)
*   `GET /api/directory/locations` (Retrieve interactive map locations)

## 5. Security Considerations

*   **Authentication**: JWT (JSON Web Tokens) for secure API access.
*   **Authorization**: Role-based access control (RBAC) to ensure users can only access authorized resources and perform authorized actions.
*   **Data Encryption**: Data at rest and in transit will be encrypted (HTTPS, Azure SQL TDE).
*   **Input Validation**: All user inputs will be validated to prevent common vulnerabilities like SQL injection and XSS.
*   **Stripe Security**: Leverage Stripe's built-in security features for payment processing.

## 6. Next Steps

*   Detailed database schema design (completed for DirectoryEntries).
*   Selection of specific Python framework (Flask vs. Django) and React Native components.
*   Setup of Azure resources.
*   Development of backend API.
*   Development of frontend applications.
*   Integration and testing.
