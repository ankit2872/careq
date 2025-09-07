#!/bin/bash

# CareQ Healthcare Queue Management System
# Complete Setup and Run Script

echo "🏥 CareQ Healthcare Queue Management System"
echo "=========================================="

# Set environment variables
export GEMINI_API_KEY="AIzaSyBp-QUoSYwdpbfuA6_JMfhjymIEXC-TjLg"
export API_URL="http://127.0.0.1:8000"
export LANG_DEFAULT="en"

# Create .env file
echo "GEMINI_API_KEY=AIzaSyBp-QUoSYwdpbfuA6_JMfhjymIEXC-TjLg" > .env
echo "API_URL=http://127.0.0.1:8000" >> .env
echo "LANG_DEFAULT=en" >> .env

echo "✅ Environment variables set"
echo "✅ .env file created"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

echo "✅ Dependencies installed"

# Kill any existing server
echo "🔄 Stopping existing server..."
pkill -f uvicorn 2>/dev/null || true

# Start the server
echo "🚀 Starting CareQ server..."
echo ""
echo "🌐 Server will be available at: http://127.0.0.1:8000"
echo "📱 Patient Registration: http://127.0.0.1:8000/patient-form"
echo "🏥 Admin Dashboard: http://127.0.0.1:8000/admin-dashboard"
echo "⚙️ Simple Admin: http://127.0.0.1:8000/admin"
echo ""
echo "🤖 AI Features Enabled:"
echo "   - Gemini AI Integration"
echo "   - Real-time Symptom Analysis"
echo "   - Treatment Recommendations"
echo "   - Health Insights"
echo "   - Queue Analytics"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the server
python3 run_server.py
