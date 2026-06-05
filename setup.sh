#!/bin/bash

# Script untuk menjalankan REKLE Dashboard + Model Server secara lokal

set -e

echo "🚀 REKLE Dashboard - Local Setup"
echo "=================================="

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -q -r requirements.txt
pip install -q -r model_server/requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🏃 To start the application:"
echo ""
echo "   Terminal 1 (Model Server):"
echo "   cd model_server"
echo "   python -m uvicorn app:app --reload --port 8000"
echo ""
echo "   Terminal 2 (Dashboard):"
echo "   streamlit run streamlit_app.py"
echo ""
echo "   URLs:"
echo "   - Dashboard: http://localhost:8501"
echo "   - API: http://localhost:8000"
echo "   - Health: http://localhost:8000/health"
echo ""
