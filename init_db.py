"""
Database initialization script
Populates initial data including directory entries and default property manager
"""
import os
from app import app, db
from models import User, PropertyManager, DirectoryEntry, Room
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize database with tables and seed data"""
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        
        # Check if data already exists
        if DirectoryEntry.query.first():
            print("Database already initialized. Skipping seed data.")
            return
        
        print("Seeding initial data...")
        
        # Create default property manager
        manager_user = User(
            email='info@cyberguysdmv.com',
            password_hash=generate_password_hash('manager123'),
            role='property_manager'
        )
        db.session.add(manager_user)
        db.session.flush()
        
        property_manager = PropertyManager(
            user_id=manager_user.id,
            name='Property Manager',
            email='info@cyberguysdmv.com'
        )
        db.session.add(property_manager)
        
        # Create Ballroom/Conference Room
        ballroom = Room(
            name='Ballroom/Conference Room',
            hourly_rate=100.00
        )
        db.session.add(ballroom)
        
        # Populate Directory Entries based on the PDF
        directory_data = [
            # First Floor (Ground)
            {'suite_number': '100', 'business_name': 'Vacant', 'map_coordinates': {'floor': 1, 'x': 410, 'y': 806}},
            {'suite_number': '101-1', 'business_name': 'Vacant', 'map_coordinates': {'floor': 1, 'x': 644, 'y': 643}},
            {'suite_number': '101-2', 'business_name': 'Vacant', 'map_coordinates': {'floor': 1, 'x': 644, 'y': 578}},
            {'suite_number': '101-3', 'business_name': 'Vacant', 'map_coordinates': {'floor': 1, 'x': 644, 'y': 508}},
            {'suite_number': '101-4', 'business_name': 'Vacant', 'map_coordinates': {'floor': 1, 'x': 644, 'y': 443}},
            {'suite_number': '101-5', 'business_name': 'Vacant', 'map_coordinates': {'floor': 1, 'x': 644, 'y': 378}},
            {'suite_number': '101-6', 'business_name': 'Vacant', 'map_coordinates': {'floor': 1, 'x': 800, 'y': 363}},
            {'suite_number': '101-7', 'business_name': 'Vacant', 'map_coordinates': {'floor': 1, 'x': 800, 'y': 426}},
            {'suite_number': '101-8', 'business_name': 'Vacant', 'map_coordinates': {'floor': 1, 'x': 800, 'y': 492}},
            {'suite_number': '103-1', 'business_name': 'GLORY HAIR DESIGNS / MARGARET BATES', 'map_coordinates': {'floor': 1, 'x': 365, 'y': 178}},
            {'suite_number': '103-2', 'business_name': 'SIX HAIR', 'map_coordinates': {'floor': 1, 'x': 500, 'y': 178}},
            {'suite_number': '103-3', 'business_name': 'A WOMAN\'S CLOSET', 'map_coordinates': {'floor': 1, 'x': 622, 'y': 178}},
            {'suite_number': '103-4', 'business_name': 'iLASHESbyPEYLI', 'map_coordinates': {'floor': 1, 'x': 712, 'y': 67}},
            {'suite_number': '103-5', 'business_name': 'KUTZ by MR. DON', 'map_coordinates': {'floor': 1, 'x': 421, 'y': 67}},
            
            # Second Floor (Buford Road Side)
            {'suite_number': '101', 'business_name': 'Vacant', 'map_coordinates': {'floor': 2, 'x': 577, 'y': 260}},
            {'suite_number': '102', 'business_name': 'Vacant', 'map_coordinates': {'floor': 2, 'x': 506, 'y': 260}},
            {'suite_number': '103', 'business_name': 'Vacant', 'map_coordinates': {'floor': 2, 'x': 418, 'y': 260}},
            {'suite_number': '104', 'business_name': 'DATA/TELECOM', 'map_coordinates': {'floor': 2, 'x': 238, 'y': 260}},
            {'suite_number': '105', 'business_name': 'Vacant', 'map_coordinates': {'floor': 2, 'x': 159, 'y': 260}},
            {'suite_number': '106', 'business_name': 'Vacant', 'map_coordinates': {'floor': 2, 'x': 76, 'y': 346}},
            {'suite_number': '107', 'business_name': 'Vacant', 'map_coordinates': {'floor': 2, 'x': 76, 'y': 390}},
            {'suite_number': '108', 'business_name': 'BEAUTY BY MOTOSH', 'map_coordinates': {'floor': 2, 'x': 181, 'y': 413}},
            {'suite_number': '109', 'business_name': 'Vacant', 'map_coordinates': {'floor': 2, 'x': 181, 'y': 474}},
            {'suite_number': '110', 'business_name': 'Vacant', 'map_coordinates': {'floor': 2, 'x': 159, 'y': 580}},
            {'suite_number': '111', 'business_name': 'AMC NATURALS', 'map_coordinates': {'floor': 2, 'x': 261, 'y': 580}},
            {'suite_number': '112', 'business_name': 'Vacant', 'map_coordinates': {'floor': 2, 'x': 332, 'y': 667}},
            {'suite_number': '113', 'business_name': 'Vacant', 'map_coordinates': {'floor': 2, 'x': 448, 'y': 667}},
            {'suite_number': 'B117', 'business_name': 'Adajislnk (j.thetatgirl)', 'map_coordinates': {'floor': 2, 'x': 390, 'y': 603}},
            {'suite_number': '115', 'business_name': 'Vacant', 'map_coordinates': {'floor': 2, 'x': 586, 'y': 603}},
            {'suite_number': '116', 'business_name': 'Vacant', 'map_coordinates': {'floor': 2, 'x': 505, 'y': 603}},
            {'suite_number': '117', 'business_name': 'LEANDREA\'S', 'map_coordinates': {'floor': 2, 'x': 390, 'y': 603}},
            {'suite_number': '118', 'business_name': 'STYLED by SHEREE', 'map_coordinates': {'floor': 2, 'x': 291, 'y': 512}},
            {'suite_number': '119', 'business_name': 'Vacant', 'map_coordinates': {'floor': 2, 'x': 181, 'y': 325}},
            {'suite_number': '120', 'business_name': 'HAIR SHE GOES', 'map_coordinates': {'floor': 2, 'x': 254, 'y': 325}},
            {'suite_number': '122', 'business_name': 'NATURAL HAIRCARE SPECIALIST', 'map_coordinates': {'floor': 2, 'x': 542, 'y': 325}},
            {'suite_number': '123', 'business_name': 'Vacant', 'map_coordinates': {'floor': 2, 'x': 682, 'y': 738}},
            {'suite_number': 'SHAMPOO', 'business_name': 'SHAMPOO ROOM', 'map_coordinates': {'floor': 2, 'x': 356, 'y': 325}},
            {'suite_number': 'BANQUET', 'business_name': 'BANQUET ROOM', 'map_coordinates': {'floor': 2, 'x': 697, 'y': 458}},
            
            # Second Floor (Midlothian Side)
            {'suite_number': '201-1', 'business_name': 'Vacant', 'map_coordinates': {'floor': 3, 'x': 502, 'y': 678}},
            {'suite_number': '201-2', 'business_name': 'Vacant', 'map_coordinates': {'floor': 3, 'x': 314, 'y': 678}},
            {'suite_number': '201-3', 'business_name': 'Vacant', 'map_coordinates': {'floor': 3, 'x': 328, 'y': 645}},
            {'suite_number': '201-4', 'business_name': 'Vacant', 'map_coordinates': {'floor': 3, 'x': 401, 'y': 605}},
            {'suite_number': '201-5', 'business_name': 'Vacant', 'map_coordinates': {'floor': 3, 'x': 502, 'y': 605}},
            {'suite_number': '202-A', 'business_name': 'FNB FADEZ', 'map_coordinates': {'floor': 3, 'x': 462, 'y': 551}},
            {'suite_number': '202-B', 'business_name': 'QUALITY LOC\'D', 'map_coordinates': {'floor': 3, 'x': 307, 'y': 507}},
            {'suite_number': '202-C', 'business_name': 'TRENA MICHELLE', 'map_coordinates': {'floor': 3, 'x': 307, 'y': 450}},
            {'suite_number': '202-D', 'business_name': 'NAILS by ALAMARISSA', 'map_coordinates': {'floor': 3, 'x': 487, 'y': 450}},
            {'suite_number': '203', 'business_name': 'ADAPTIVE ACCOMODATIONS OUTREACH GROUP', 'map_coordinates': {'floor': 3, 'x': 192, 'y': 332}},
            {'suite_number': '203-1', 'business_name': 'NYSLAYEDTHAT', 'map_coordinates': {'floor': 3, 'x': 514, 'y': 254}},
            {'suite_number': '203-2', 'business_name': 'GRACEFUL STYLES HAIR SALON', 'map_coordinates': {'floor': 3, 'x': 192, 'y': 360}},
            {'suite_number': '203-3', 'business_name': 'NAILZby_MIA / JAIDAANAILEDIT', 'map_coordinates': {'floor': 3, 'x': 392, 'y': 254}},
            {'suite_number': '203-6', 'business_name': 'LUXE GLOW 24', 'map_coordinates': {'floor': 3, 'x': 342, 'y': 254}},
            {'suite_number': '203-7', 'business_name': 'Vacant', 'map_coordinates': {'floor': 3, 'x': 277, 'y': 254}},
            {'suite_number': '203-8', 'business_name': 'Vacant', 'map_coordinates': {'floor': 3, 'x': 105, 'y': 288}},
            {'suite_number': '203-9', 'business_name': 'Vacant', 'map_coordinates': {'floor': 3, 'x': 105, 'y': 353}},
            {'suite_number': '203-10', 'business_name': 'THE PENTHOUSE', 'map_coordinates': {'floor': 3, 'x': 205, 'y': 740}},
            {'suite_number': '205', 'business_name': 'MID - ATLANTIC MOVING & STORAGE', 'map_coordinates': {'floor': 3, 'x': 763, 'y': 803}},
            {'suite_number': '209', 'business_name': 'Vacant', 'map_coordinates': {'floor': 3, 'x': 252, 'y': 740}},
            {'suite_number': '210', 'business_name': 'STYLED by NEJA / SLEEK HAIR by SHEEK', 'map_coordinates': {'floor': 3, 'x': 151, 'y': 740}},
            {'suite_number': '211', 'business_name': 'THE LOC LOUNGE', 'map_coordinates': {'floor': 3, 'x': 129, 'y': 791}},
            {'suite_number': '211-1', 'business_name': 'KINAH NAILED IT', 'map_coordinates': {'floor': 3, 'x': 307, 'y': 791}},
            {'suite_number': '212', 'business_name': 'Vacant', 'map_coordinates': {'floor': 3, 'x': 307, 'y': 791}},
            {'suite_number': '213', 'business_name': 'CYBERGUYS IT SOLUTIONS', 'map_coordinates': {'floor': 3, 'x': 391, 'y': 740}},
            
            # Third Floor
            {'suite_number': '200', 'business_name': 'Vacant', 'map_coordinates': {'floor': 4, 'x': 406, 'y': 683}},
            {'suite_number': '201', 'business_name': 'Vacant', 'map_coordinates': {'floor': 4, 'x': 293, 'y': 800}},
            {'suite_number': '202', 'business_name': 'Vacant', 'map_coordinates': {'floor': 4, 'x': 189, 'y': 800}},
            {'suite_number': '203', 'business_name': 'Vacant', 'map_coordinates': {'floor': 4, 'x': 310, 'y': 607}},
            {'suite_number': '204', 'business_name': 'Vacant', 'map_coordinates': {'floor': 4, 'x': 189, 'y': 87}},
            {'suite_number': '311', 'business_name': 'Vacant', 'map_coordinates': {'floor': 5, 'x': 387, 'y': 508}},
            {'suite_number': '312C', 'business_name': 'Vacant', 'map_coordinates': {'floor': 5, 'x': 387, 'y': 716}},
            {'suite_number': '313', 'business_name': 'Vacant', 'map_coordinates': {'floor': 5, 'x': 141, 'y': 713}},
            {'suite_number': '314', 'business_name': 'Vacant', 'map_coordinates': {'floor': 5, 'x': 141, 'y': 641}},
            {'suite_number': '315', 'business_name': 'Vacant', 'map_coordinates': {'floor': 5, 'x': 141, 'y': 544}},
            {'suite_number': '316', 'business_name': 'Vacant', 'map_coordinates': {'floor': 5, 'x': 141, 'y': 444}},
            {'suite_number': '317', 'business_name': 'Vacant', 'map_coordinates': {'floor': 5, 'x': 141, 'y': 342}},
            {'suite_number': '318', 'business_name': 'Vacant', 'map_coordinates': {'floor': 5, 'x': 437, 'y': 331}},
            {'suite_number': '319', 'business_name': 'CHOSEN CHRISTIAN MINISTRIES', 'map_coordinates': {'floor': 5, 'x': 362, 'y': 184}},
        ]
        
        for entry in directory_data:
            directory_entry = DirectoryEntry(
                suite_number=entry['suite_number'],
                business_name=entry['business_name'],
                map_coordinates=entry['map_coordinates']
            )
            db.session.add(directory_entry)
        
        # Commit all changes
        db.session.commit()
        print("Database initialized successfully!")
        print(f"Created {len(directory_data)} directory entries")
        print("Default property manager created: info@cyberguysdmv.com / manager123")

if __name__ == '__main__':
    init_database()
