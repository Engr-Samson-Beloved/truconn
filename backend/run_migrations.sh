#!/bin/bash
echo "========================================"
echo "Running Compliance Migrations"
echo "========================================"
echo ""

# Check if venv exists and activate it
if [ -f "venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
elif [ -f "backend/venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source backend/venv/bin/activate
else
    echo "WARNING: Virtual environment not found!"
    echo "Please activate it manually first."
    echo ""
fi

echo ""
echo "Running migrations for compliance app..."
python manage.py migrate compliance

echo ""
echo "Running all migrations to ensure everything is up to date..."
python manage.py migrate

echo ""
echo "========================================"
echo "Migration Complete!"
echo "========================================"

