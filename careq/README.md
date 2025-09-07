# 🏥 CareQ - AI-Powered Healthcare Queue Management System

## 🎯 **Complete Healthcare Solution with Gemini AI Integration**

### ✅ **FULLY FUNCTIONAL SYSTEM WITH GEMINI API KEY**

---

## 🚀 **Quick Start**

### **Option 1: Automated Setup (Recommended)**
```bash
# Run the complete setup script
./setup_and_run.sh
```

### **Option 2: Manual Setup**
```bash
# 1. Set environment variables
export GEMINI_API_KEY="AIzaSyBp-QUoSYwdpbfuA6_JMfhjymIEXC-TjLg"
export API_URL="http://127.0.0.1:8000"
export LANG_DEFAULT="en"

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Start the server
python3 run_server.py
```

---

## 🌐 **Access Your Application**

### **Main Application URLs:**
- **🏠 Home Page**: `http://127.0.0.1:8000/`
- **📝 Patient Registration**: `http://127.0.0.1:8000/patient-form`
- **🏥 Advanced Admin Dashboard**: `http://127.0.0.1:8000/admin-dashboard`
- **⚙️ Simple Admin**: `http://127.0.0.1:8000/admin`

### **API Endpoints:**
- **Patients API**: `http://127.0.0.1:8000/patients/`
- **AI Symptom Analysis**: `http://127.0.0.1:8000/ai/analyze-symptoms`
- **AI Patient Analysis**: `http://127.0.0.1:8000/ai/patient-analysis/{id}`
- **AI Queue Insights**: `http://127.0.0.1:8000/ai/queue-insights`
- **PDF Generation**: `http://127.0.0.1:8000/generate_token_pdf/{id}`

---

## 🤖 **AI Features (Gemini API Enabled)**

### **For Patients:**
- **🧠 AI Symptom Analysis**: Real-time analysis using Google Gemini AI
- **💊 Treatment Recommendations**: AI-generated treatment suggestions
- **🏥 Health Insights**: Personalized health recommendations
- **📊 Health Score**: AI confidence and health assessment
- **⚠️ Red Flags**: AI-identified warning signs

### **For Healthcare Staff:**
- **📈 Queue Analytics**: AI-powered queue pattern analysis
- **👥 Patient Analysis**: Individual patient AI insights
- **🎯 Resource Optimization**: AI management recommendations
- **📋 Treatment Support**: AI treatment recommendations
- **📊 Performance Metrics**: AI confidence tracking

### **For Administrators:**
- **📊 AI Dashboard**: Comprehensive AI analytics
- **🔍 Pattern Recognition**: AI queue pattern analysis
- **💡 Smart Recommendations**: AI resource optimization
- **📈 Trend Analysis**: Historical AI insights
- **⚡ Real-time Updates**: Live AI recommendations

---

## 🛠 **Technical Stack**

### **Backend:**
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM
- **Uvicorn**: ASGI server
- **Google Gemini AI**: Advanced language model integration
- **ReportLab**: PDF generation
- **APScheduler**: Task scheduling
- **WebSocket**: Real-time communication

### **Frontend:**
- **HTML5/CSS3**: Modern web standards
- **JavaScript (ES6+)**: Interactive functionality
- **Glass-morphism Design**: Premium UI effects
- **Responsive Design**: Mobile-first approach
- **Multi-language Support**: English and Hindi

### **AI Integration:**
- **Google Gemini Pro**: Advanced language model
- **Real-time Analysis**: Live symptom analysis
- **Safety Settings**: Medical content compliance
- **Fallback Mode**: Reliable operation
- **Confidence Scoring**: AI reliability metrics

---

## 📁 **Project Structure**

```
careq/
├── backend/
│   ├── app.py                 # Main FastAPI application
│   ├── db.py                  # Database models
│   ├── triage.py              # Triage scoring system
│   ├── ai_predictor.py        # AI wait time prediction
│   ├── gemini_ai.py           # Gemini AI integration
│   ├── notifications.py       # Notification system
│   ├── i18n/                  # Internationalization
│   │   ├── en.json
│   │   └── hi.json
│   └── __init__.py
├── frontend/
│   ├── index.html             # Main landing page
│   ├── patient_form.html      # Patient registration
│   ├── admin.html             # Simple admin dashboard
│   └── admin_dashboard.html   # Advanced admin dashboard
├── requirements.txt           # Python dependencies
├── run_server.py             # Server startup script
├── setup_and_run.sh          # Complete setup script
├── .env                      # Environment variables
└── README.md                 # This file
```

---

## 🔧 **Configuration**

### **Environment Variables:**
```bash
GEMINI_API_KEY=AIzaSyBp-QUoSYwdpbfuA6_JMfhjymIEXC-TjLg
API_URL=http://127.0.0.1:8000
LANG_DEFAULT=en
```

### **Database:**
- **SQLite**: File-based database (no setup required)
- **Auto-creation**: Database and tables created automatically
- **Data persistence**: Patient data saved between sessions

---

## 🎨 **UI Features**

### **Main Landing Page:**
- **Glass-morphism Design**: Modern, premium UI effects
- **AI Features Showcase**: Interactive AI cards
- **Real-time Statistics**: Live queue data
- **Multi-language Support**: English and Hindi
- **Responsive Design**: Mobile and desktop optimized

### **Patient Registration:**
- **Multi-step Form**: Guided registration process
- **AI Analysis**: Real-time symptom analysis
- **Treatment Recommendations**: AI-generated suggestions
- **PDF Token Generation**: Professional token creation
- **Confirmation System**: Step-by-step validation

### **Admin Dashboard:**
- **Real-time Queue Management**: Live patient monitoring
- **AI Insights Section**: Comprehensive AI analytics
- **Patient Analytics**: Individual patient analysis
- **Resource Optimization**: AI management recommendations
- **Export Functionality**: Data export capabilities

---

## 🧠 **AI Analysis Examples**

### **Symptom Analysis:**
```json
{
  "symptoms": ["fever", "headache", "cough"],
  "age": 25,
  "ai_analysis": {
    "potential_conditions": ["Viral infection", "Common cold"],
    "immediate_care": ["Rest", "Stay hydrated", "Monitor temperature"],
    "red_flags": ["High fever", "Severe headache", "Difficulty breathing"],
    "confidence_level": 0.85
  },
  "treatment_recommendations": {
    "immediate_actions": ["Rest", "Hydration", "Temperature monitoring"],
    "medication_suggestions": ["Over-the-counter pain relief"],
    "lifestyle_changes": ["Adequate sleep", "Stress management"]
  }
}
```

### **Queue Analytics:**
```json
{
  "queue_analysis": {
    "common_symptoms": ["fever", "cough", "headache"],
    "peak_conditions": ["respiratory", "gastrointestinal"],
    "staffing_insights": "Consider additional staff during peak hours",
    "resource_recommendations": ["Increase monitoring equipment", "Staff training"]
  }
}
```

---

## 🚀 **Features Overview**

### **Core Features:**
- ✅ **Patient Registration**: Multi-step form with AI analysis
- ✅ **Queue Management**: Real-time patient queue monitoring
- ✅ **AI Triage**: Smart priority assessment
- ✅ **PDF Tokens**: Professional token generation
- ✅ **Real-time Updates**: WebSocket live updates
- ✅ **Multi-language**: English and Hindi support
- ✅ **Responsive Design**: Mobile and desktop optimized

### **AI Features:**
- ✅ **Gemini AI Integration**: Google's advanced language model
- ✅ **Symptom Analysis**: Real-time AI analysis
- ✅ **Treatment Recommendations**: AI-generated suggestions
- ✅ **Health Insights**: Personalized health advice
- ✅ **Queue Analytics**: AI-powered queue insights
- ✅ **Resource Optimization**: AI management recommendations
- ✅ **Confidence Scoring**: AI reliability metrics
- ✅ **Safety Compliance**: Medical content standards

### **Admin Features:**
- ✅ **Real-time Dashboard**: Live patient monitoring
- ✅ **AI Analytics**: Comprehensive AI insights
- ✅ **Patient Management**: Individual patient analysis
- ✅ **Queue Control**: Call, reset, manage patients
- ✅ **Export Data**: Data export capabilities
- ✅ **Performance Metrics**: AI confidence tracking

---

## 🔒 **Security & Privacy**

### **Data Protection:**
- **Secure API**: Encrypted communication
- **No Data Storage**: AI analysis not permanently stored
- **Patient Privacy**: Protected health information
- **Compliance**: Healthcare data protection standards

### **AI Safety:**
- **Safety Settings**: Configured for medical content
- **Disclaimer**: Clear AI analysis limitations
- **Professional Advice**: Emphasis on consulting healthcare professionals
- **Fallback Mode**: Graceful degradation when AI unavailable

---

## 📱 **Mobile Support**

### **Responsive Design:**
- **Mobile-First**: Optimized for mobile devices
- **Touch-Friendly**: Easy navigation on touch screens
- **Fast Loading**: Optimized for mobile networks
- **Offline Capable**: Basic functionality without internet

---

## 🌍 **Multi-language Support**

### **Languages:**
- **English**: Full feature support
- **Hindi**: Complete translation
- **Easy Switching**: Toggle between languages
- **Cultural Adaptation**: Localized content

---

## 🎯 **Use Cases**

### **Healthcare Facilities:**
- **Hospitals**: Emergency room queue management
- **Clinics**: Outpatient appointment management
- **Urgent Care**: Walk-in patient management
- **Specialty Centers**: Specialized care queues

### **Patient Benefits:**
- **Reduced Wait Times**: Efficient queue management
- **Better Information**: Real-time updates
- **AI Insights**: Health analysis and recommendations
- **Professional Care**: Enhanced healthcare experience

---

## 🚀 **Getting Started**

### **1. Run the Setup Script:**
```bash
./setup_and_run.sh
```

### **2. Access the Application:**
- Open browser and go to: `http://127.0.0.1:8000`
- Register as a patient or access admin dashboard
- Experience AI-powered healthcare management

### **3. Test AI Features:**
- Register a patient with symptoms
- Click "Get AI Analysis" for real-time insights
- Access admin dashboard for AI analytics
- Explore queue management features

---

## 🎉 **Ready to Use!**

Your CareQ system is now **fully operational** with **Gemini AI integration**!

**🌐 Access your application at: `http://127.0.0.1:8000`**

**Key Features:**
- ✅ **Complete Healthcare Queue Management**
- ✅ **Google Gemini AI Integration**
- ✅ **Real-time Symptom Analysis**
- ✅ **AI Treatment Recommendations**
- ✅ **Health Insights and Analytics**
- ✅ **Professional PDF Token Generation**
- ✅ **Multi-language Support**
- ✅ **Responsive Design**
- ✅ **Real-time Updates**
- ✅ **Admin Dashboard with AI Analytics**

**Your healthcare facility now has the most advanced AI-powered queue management system!** 🏥🤖✨

---

## 📞 **Support**

For any issues or questions:
1. Check the terminal output for error messages
2. Ensure all dependencies are installed
3. Verify the server is running on port 8000
4. Check the browser console for JavaScript errors

**Happy Healthcare Management!** 🏥✨
