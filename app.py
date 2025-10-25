"""
Corporate Office 101 - Backend API
Flask application for tenant portal management
"""
import os
from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, 
    get_jwt_identity, get_jwt
)
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import stripe

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://localhost/corporate_office')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize extensions (db is initialized in models.py)
from models import db, User, Tenant, PropertyManager, Payment, Event, EventDocument, EventRSVP, Room, Booking, ServiceRequest, Message, DirectoryEntry

db.init_app(app)
jwt = JWTManager(app)
CORS(app, origins=os.getenv('CORS_ORIGINS', '*').split(','))

# Stripe configuration
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')

# Role-based access control decorator
def role_required(roles):
    """Decorator to require specific roles for endpoints"""
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = User.query.get(int(current_user_id))
            if not user or user.role not in roles:
                return jsonify({'error': 'Unauthorized access'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new tenant user"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['email', 'password', 'business_name', 'suite_number']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create user
    user = User(
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        role='tenant'
    )
    db.session.add(user)
    db.session.flush()
    
    # Create tenant profile
    tenant = Tenant(
        user_id=user.id,
        business_name=data['business_name'],
        suite_number=data['suite_number'],
        contact_info=data.get('contact_info', {}),
        email_notifications_enabled=data.get('email_notifications_enabled', True)
    )
    db.session.add(tenant)
    db.session.commit()
    
    # Generate access token
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'message': 'User registered successfully',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'email': user.email,
            'role': user.role
        }
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    data = request.get_json()
    
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user.id,
            'email': user.email,
            'role': user.role
        }
    }), 200

@app.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    profile = {'id': user.id, 'email': user.email, 'role': user.role}
    
    if user.role == 'tenant':
        tenant = Tenant.query.filter_by(user_id=user.id).first()
        if tenant:
            profile['business_name'] = tenant.business_name
            profile['suite_number'] = tenant.suite_number
            profile['contact_info'] = tenant.contact_info
    elif user.role == 'property_manager':
        manager = PropertyManager.query.filter_by(user_id=user.id).first()
        if manager:
            profile['name'] = manager.name
    
    return jsonify(profile), 200

@app.route('/api/auth/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    data = request.get_json()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if user.role == 'tenant':
        tenant = Tenant.query.filter_by(user_id=user.id).first()
        if tenant:
            if 'business_name' in data:
                tenant.business_name = data['business_name']
            if 'contact_info' in data:
                tenant.contact_info = data['contact_info']
            if 'email_notifications_enabled' in data:
                tenant.email_notifications_enabled = data['email_notifications_enabled']
    
    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200

# ==================== PAYMENT ROUTES ====================

@app.route('/api/payments', methods=['GET'])
@jwt_required()
@role_required(['tenant'])
def get_payments():
    """Get payment history for current tenant"""
    current_user_id = get_jwt_identity()
    tenant = Tenant.query.filter_by(user_id=int(current_user_id)).first()
    
    if not tenant:
        return jsonify({'error': 'Tenant not found'}), 404
    
    payments = Payment.query.filter_by(tenant_id=tenant.id).order_by(Payment.due_date.desc()).all()
    
    return jsonify([{
        'id': p.id,
        'amount': float(p.amount),
        'due_date': p.due_date.isoformat(),
        'paid_date': p.paid_date.isoformat() if p.paid_date else None,
        'status': p.status,
        'is_recurring': p.is_recurring
    } for p in payments]), 200

@app.route('/api/payments/initiate', methods=['POST'])
@jwt_required()
@role_required(['tenant'])
def initiate_payment():
    """Initiate a new payment with Stripe"""
    current_user_id = get_jwt_identity()
    tenant = Tenant.query.filter_by(user_id=int(current_user_id)).first()
    data = request.get_json()
    
    if not tenant:
        return jsonify({'error': 'Tenant not found'}), 404
    
    amount = data.get('amount')
    if not amount:
        return jsonify({'error': 'Amount is required'}), 400
    
    try:
        # Create Stripe PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=int(float(amount) * 100),  # Convert to cents
            currency='usd',
            metadata={
                'tenant_id': str(tenant.id),
                'business_name': tenant.business_name
            }
        )
        
        # Create payment record
        payment = Payment(
            tenant_id=tenant.id,
            amount=amount,
            due_date=datetime.now(),
            status='due',
            stripe_charge_id=intent.id
        )
        db.session.add(payment)
        db.session.commit()
        
        return jsonify({
            'client_secret': intent.client_secret,
            'payment_id': payment.id
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/payments/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events"""
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    # Handle payment success
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        payment = Payment.query.filter_by(stripe_charge_id=payment_intent['id']).first()
        
        if payment:
            payment.status = 'paid'
            payment.paid_date = datetime.now()
            db.session.commit()
    
    # Handle payment failure
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        payment = Payment.query.filter_by(stripe_charge_id=payment_intent['id']).first()
        
        if payment:
            payment.status = 'failed'
            db.session.commit()
    
    return jsonify({'status': 'success'}), 200

# ==================== EVENTS ROUTES ====================

@app.route('/api/events', methods=['GET'])
@jwt_required()
def get_events():
    """Get all events"""
    events = Event.query.order_by(Event.event_date.desc(), Event.event_time.desc()).all()
    
    return jsonify([{
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'event_date': e.event_date.isoformat(),
        'event_time': e.event_time.isoformat(),
        'location': e.location,
        'contact_person': e.contact_person,
        'requires_rsvp': e.requires_rsvp,
        'created_at': e.created_at.isoformat()
    } for e in events]), 200

@app.route('/api/events', methods=['POST'])
@jwt_required()
@role_required(['tenant'])
def create_event():
    """Create a new event"""
    current_user_id = get_jwt_identity()
    tenant = Tenant.query.filter_by(user_id=int(current_user_id)).first()
    data = request.get_json()
    
    if not tenant:
        return jsonify({'error': 'Tenant not found'}), 404
    
    event = Event(
        creator_tenant_id=tenant.id,
        title=data['title'],
        description=data.get('description'),
        event_date=datetime.fromisoformat(data['event_date']),
        event_time=datetime.strptime(data['event_time'], '%H:%M:%S').time(),
        location=data['location'],
        contact_person=data.get('contact_person'),
        requires_rsvp=data.get('requires_rsvp', False)
    )
    
    db.session.add(event)
    db.session.commit()
    
    return jsonify({'message': 'Event created successfully', 'event_id': event.id}), 201

# ==================== DIRECTORY ROUTES ====================

@app.route('/api/directory', methods=['GET'])
@jwt_required()
def get_directory():
    """Get building directory"""
    entries = DirectoryEntry.query.order_by(DirectoryEntry.suite_number).all()
    
    return jsonify([{
        'id': e.id,
        'suite_number': e.suite_number,
        'business_name': e.business_name,
        'map_coordinates': e.map_coordinates
    } for e in entries]), 200

@app.route('/api/directory/map/pdf', methods=['GET'])
def get_map_pdf():
    """Get map PDF URL"""
    # In production, this would return the Azure Blob Storage URL
    map_url = os.getenv('MAP_PDF_URL', '/static/OfficeDirectory_and_Map.pdf')
    return jsonify({'url': map_url}), 200

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'Corporate Office 101 API',
        'version': '1.0.0',
        'status': 'running'
    }), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=os.getenv('FLASK_ENV') == 'development', host='0.0.0.0', port=5000)
