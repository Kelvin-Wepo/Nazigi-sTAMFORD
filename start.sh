#!/bin/bash
set -e

echo "=========================================="
echo "🚌 Nazigi Stamford Bus SMS Service"
echo "=========================================="

# Wait for database to be ready
echo "⏳ Waiting for database..."
sleep 5

# Run database migrations
echo "📊 Running database migrations..."
export FLASK_APP=app.py
flask db upgrade 2>&1 || {
    echo "⚠️  Migration failed, trying direct table creation..."
    python -c "from app import create_app; from models import db; app = create_app(); app.app_context().push(); db.create_all(); print('✅ Tables created')" 2>&1 || echo "❌ Table creation failed - will retry on first request"
}

echo "✅ Database ready!"
echo "=========================================="
echo "🚀 Starting Gunicorn server on port ${PORT:-5000}"
echo "=========================================="

# Start Gunicorn
exec gunicorn \
    --bind 0.0.0.0:${PORT:-5000} \
    --workers ${GUNICORN_WORKERS:-4} \
    --threads ${GUNICORN_THREADS:-2} \
    --timeout ${GUNICORN_TIMEOUT:-120} \
    --worker-class sync \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --capture-output \
    --enable-stdio-inheritance \
    wsgi:app
