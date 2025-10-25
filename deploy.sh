#!/bin/bash
set -e

echo "========================================="
echo "Post-Deployment Script Started"
echo "========================================="

# Navigate to app directory
cd /home/site/wwwroot

# Check if virtual environment exists
if [ -d "antenv" ]; then
    echo "✓ Activating virtual environment..."
    source antenv/bin/activate
else
    echo "⚠ No virtual environment found, using system Python"
fi

# Install/upgrade dependencies
echo ""
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✓ Dependencies installed"

# Run database migrations
echo ""
echo "🗄️ Running database migrations..."
python << 'EOF'
try:
    from app import app, db
    with app.app_context():
        db.create_all()
        print("✓ Database tables created/updated successfully!")
        
        # Verify tables
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"✓ Database has {len(tables)} table(s): {', '.join(tables)}")
except Exception as e:
    print(f"✗ Error during migration: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
EOF

echo ""
echo "========================================="
echo "Post-Deployment Script Completed"
echo "========================================="
