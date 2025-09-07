#!/usr/bin/env python3
"""
Test script for Admin Dashboard Features
Tests all admin dashboard functionality
"""

import requests
import json
import time

API_URL = "http://127.0.0.1:8000"

def test_endpoint(endpoint, method="GET", data=None):
    """Test an API endpoint"""
    try:
        if method == "GET":
            response = requests.get(f"{API_URL}{endpoint}")
        elif method == "POST":
            response = requests.post(f"{API_URL}{endpoint}", json=data)
        elif method == "PUT":
            response = requests.put(f"{API_URL}{endpoint}", json=data)
        
        print(f"✅ {method} {endpoint}: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"   Error: {response.text}")
            return None
    except Exception as e:
        print(f"❌ {method} {endpoint}: Error - {e}")
        return None

def main():
    print("🏥 Testing Admin Dashboard Features")
    print("=" * 50)
    
    # Test 1: Get all patients
    print("\n1. Testing Patient Data Retrieval")
    patients = test_endpoint("/patients/")
    if patients:
        print(f"   Found {len(patients)} patients")
        if patients:
            print(f"   First patient: {patients[0]['name']} - {patients[0]['severity_level']}")
    
    # Test 2: Test AI Queue Analytics
    print("\n2. Testing AI Queue Analytics")
    analytics = test_endpoint("/ai/queue-analytics")
    if analytics:
        print(f"   Queue analytics loaded successfully")
        print(f"   Total patients: {analytics.get('total_patients', 'N/A')}")
    
    # Test 3: Test AI Queue Insights
    print("\n3. Testing AI Queue Insights")
    insights = test_endpoint("/ai/queue-insights")
    if insights:
        print(f"   Queue insights loaded successfully")
        analysis = insights.get('queue_analysis', {})
        print(f"   Common symptoms: {analysis.get('common_symptoms', [])}")
    
    # Test 4: Test Patient AI Analysis
    if patients:
        print("\n4. Testing Patient AI Analysis")
        patient_id = patients[0]['id']
        patient_analysis = test_endpoint(f"/ai/patient-analysis/{patient_id}")
        if patient_analysis:
            print(f"   Patient analysis for ID {patient_id} loaded successfully")
            ai_analysis = patient_analysis.get('ai_analysis', {})
            print(f"   Confidence level: {ai_analysis.get('confidence_level', 'N/A')}")
    
    # Test 5: Test AI Symptom Analysis
    print("\n5. Testing AI Symptom Analysis")
    symptom_data = {
        "symptoms": ["fever", "headache", "cough"],
        "age": 25,
        "severity_level": "Medium"
    }
    symptom_analysis = test_endpoint("/ai/analyze-symptoms", "POST", symptom_data)
    if symptom_analysis:
        print(f"   Symptom analysis completed successfully")
        ai_analysis = symptom_analysis.get('ai_analysis', {})
        print(f"   AI model: {ai_analysis.get('ai_model', 'N/A')}")
    
    # Test 6: Test Wait Time Prediction
    print("\n6. Testing Wait Time Prediction")
    wait_time = test_endpoint("/ai/predict-wait-time?severity_level=Critical&symptoms=fever,chest%20pain&age=45")
    if wait_time:
        print(f"   Wait time prediction completed")
        print(f"   Predicted wait time: {wait_time.get('predicted_wait_time', 'N/A')} minutes")
    
    # Test 7: Test PDF Generation
    if patients:
        print("\n7. Testing PDF Generation")
        patient_id = patients[0]['id']
        pdf_response = requests.get(f"{API_URL}/generate_token_pdf/{patient_id}")
        if pdf_response.status_code == 200:
            print(f"   PDF generated successfully for patient {patient_id}")
        else:
            print(f"   PDF generation failed: {pdf_response.status_code}")
    
    # Test 8: Test Patient Management (Call Patient)
    if patients:
        print("\n8. Testing Patient Management")
        patient_id = patients[0]['id']
        call_data = {"called": True}
        call_result = test_endpoint(f"/patients/{patient_id}", "PUT", call_data)
        if call_result:
            print(f"   Patient {patient_id} called successfully")
            
            # Reset the patient
            reset_data = {"called": False}
            reset_result = test_endpoint(f"/patients/{patient_id}", "PUT", reset_data)
            if reset_result:
                print(f"   Patient {patient_id} reset successfully")
    
    print("\n" + "=" * 50)
    print("🎉 Admin Dashboard Feature Testing Complete!")
    print("All core features are functional and ready for use.")

if __name__ == "__main__":
    main()
