"""
Database models for Corporate Office 101 Tenant Portal
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB

db = SQLAlchemy()

class User(db.Model):
    """User authentication table"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'tenant' or 'property_manager'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = db.relationship('Tenant', backref='user', uselist=False, lazy=True)
    property_manager = db.relationship('PropertyManager', backref='user', uselist=False, lazy=True)
    messages = db.relationship('Message', backref='sender', lazy=True)

class Tenant(db.Model):
    """Tenant details table"""
    __tablename__ = 'tenants'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=True)
    business_name = db.Column(db.String(255), nullable=False)
    suite_number = db.Column(db.String(50), nullable=False, unique=True)
    contact_info = db.Column(JSONB, default={})
    email_notifications_enabled = db.Column(db.Boolean, default=True)
    stripe_customer_id = db.Column(db.String(255), unique=True)
    map_coordinates = db.Column(JSONB)
    
    # Relationships
    payments = db.relationship('Payment', backref='tenant', lazy=True)
    events = db.relationship('Event', backref='creator', lazy=True)
    bookings = db.relationship('Booking', backref='tenant', lazy=True)
    service_requests = db.relationship('ServiceRequest', backref='tenant', lazy=True)
    event_rsvps = db.relationship('EventRSVP', backref='tenant', lazy=True)

class PropertyManager(db.Model):
    """Property manager details table"""
    __tablename__ = 'property_managers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    
    # Relationships
    approved_bookings = db.relationship('Booking', backref='approver', lazy=True)
    assigned_requests = db.relationship('ServiceRequest', backref='assigned_to', lazy=True)

class Payment(db.Model):
    """Payment transactions table"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    due_date = db.Column(db.Date, nullable=False, index=True)
    paid_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), nullable=False, index=True)  # 'due', 'paid', 'overdue', 'failed'
    stripe_charge_id = db.Column(db.String(255), unique=True)
    is_recurring = db.Column(db.Boolean, default=False)
    payment_method_type = db.Column(db.String(50))

class Event(db.Model):
    """Events table"""
    __tablename__ = 'events'
    __table_args__ = {'quote': True} 
    
    id = db.Column(db.Integer, primary_key=True)
    creator_tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.Date, nullable=False, index=True)
    event_time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    contact_person = db.Column(db.String(255))
    requires_rsvp = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    documents = db.relationship('EventDocument', backref='event', lazy=True, cascade='all, delete-orphan')
    rsvps = db.relationship('EventRSVP', backref='event', lazy=True, cascade='all, delete-orphan')

class EventDocument(db.Model):
    """Event documents table"""
    __tablename__ = 'event_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    file_url = db.Column(db.String(512), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class EventRSVP(db.Model):
    """Event RSVPs table"""
    __tablename__ = 'event_rsvps'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # 'attending', 'not_attending', 'maybe'
    rsvped_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('event_id', 'tenant_id', name='unique_event_rsvp'),)

class Room(db.Model):
    """Bookable rooms table"""
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Relationships
    bookings = db.relationship('Booking', backref='room', lazy=True)

class Booking(db.Model):
    """Room bookings table"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, index=True)
    end_time = db.Column(db.DateTime, nullable=False)
    purpose = db.Column(db.Text, nullable=False)
    num_attendees = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, index=True)  # 'pending', 'approved', 'rejected', 'cancelled'
    manager_approval_id = db.Column(db.Integer, db.ForeignKey('property_managers.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)
    stripe_payment_intent_id = db.Column(db.String(255), unique=True)

class ServiceRequest(db.Model):
    """Service requests table"""
    __tablename__ = 'service_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'maintenance', 'cleaning', 'meeting'
    description = db.Column(db.Text, nullable=False)
    urgency = db.Column(db.String(50))  # 'low', 'medium', 'high'
    photo_url = db.Column(db.String(512))
    status = db.Column(db.String(50), nullable=False, index=True)  # 'new', 'in_progress', 'resolved', 'closed'
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('property_managers.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Message(db.Model):
    """Message board table"""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_type = db.Column(db.String(50), nullable=False)  # 'all', 'tenant', 'manager'
    content = db.Column(db.Text, nullable=False)
    is_urgent = db.Column(db.Boolean, default=False)
    is_important = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    expires_at = db.Column(db.DateTime)

class DirectoryEntry(db.Model):
    """Building directory table"""
    __tablename__ = 'directory_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    suite_number = db.Column(db.String(50), unique=True, nullable=False)
    business_name = db.Column(db.String(255), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), unique=True)
    map_coordinates = db.Column(JSONB)
