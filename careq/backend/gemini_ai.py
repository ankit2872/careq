"""
Google Gemini AI Integration for Patient Analysis and Recommendations
Provides intelligent insights, treatment recommendations, and health analysis
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiAIService:
    def __init__(self):
        """Initialize Gemini AI service"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found. AI features will be limited.")
            self.enabled = False
        else:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.enabled = True
            
        # Safety settings for medical content
        self.safety_settings = [
            {
                "category": HarmCategory.HARM_CATEGORY_HARASSMENT,
                "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            },
            {
                "category": HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            },
            {
                "category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            },
            {
                "category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            },
        ]

    async def analyze_patient_symptoms(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze patient symptoms and provide AI insights
        """
        if not self.enabled:
            return self._fallback_analysis(patient_data)
            
        try:
            symptoms = patient_data.get('symptoms', [])
            age = patient_data.get('age', 0)
            severity = patient_data.get('severity_level', 'Medium')
            
            prompt = f"""
            As a medical AI assistant, analyze the following patient information and provide insights:
            
            Patient Age: {age}
            Symptoms: {', '.join(symptoms) if isinstance(symptoms, list) else symptoms}
            Severity Level: {severity}
            
            Please provide:
            1. Potential conditions or causes (be cautious and suggest seeing a doctor)
            2. Immediate care recommendations
            3. Red flags to watch for
            4. General health advice
            5. When to seek immediate medical attention
            
            Format your response as JSON with the following structure:
            {{
                "potential_conditions": ["condition1", "condition2"],
                "immediate_care": ["care1", "care2"],
                "red_flags": ["flag1", "flag2"],
                "health_advice": ["advice1", "advice2"],
                "urgent_attention": "when to seek immediate help",
                "confidence_level": 0.8,
                "ai_insights": "overall analysis"
            }}
            
            Remember: This is for informational purposes only and should not replace professional medical advice.
            """
            
            response = self.model.generate_content(
                prompt,
                safety_settings=self.safety_settings
            )
            
            # Parse the response
            try:
                # Extract JSON from response
                response_text = response.text
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    json_text = response_text[json_start:json_end].strip()
                else:
                    json_text = response_text
                
                analysis = json.loads(json_text)
                analysis['timestamp'] = datetime.now().isoformat()
                analysis['ai_model'] = 'gemini-pro'
                
                return analysis
                
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return {
                    "potential_conditions": ["Please consult a healthcare professional"],
                    "immediate_care": ["Rest and monitor symptoms"],
                    "red_flags": ["Seek immediate medical attention if symptoms worsen"],
                    "health_advice": ["Maintain good hydration and rest"],
                    "urgent_attention": "If symptoms are severe or worsening",
                    "confidence_level": 0.5,
                    "ai_insights": response.text[:500] + "...",
                    "timestamp": datetime.now().isoformat(),
                    "ai_model": "gemini-pro"
                }
                
        except Exception as e:
            logger.error(f"Error in Gemini AI analysis: {e}")
            return self._fallback_analysis(patient_data)

    async def generate_treatment_recommendations(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate AI-powered treatment recommendations
        """
        if not self.enabled:
            return self._fallback_recommendations(patient_data)
            
        try:
            symptoms = patient_data.get('symptoms', [])
            age = patient_data.get('age', 0)
            severity = patient_data.get('severity_level', 'Medium')
            
            prompt = f"""
            As a medical AI assistant, provide treatment recommendations for:
            
            Patient Age: {age}
            Symptoms: {', '.join(symptoms) if isinstance(symptoms, list) else symptoms}
            Severity Level: {severity}
            
            Provide recommendations in JSON format:
            {{
                "immediate_actions": ["action1", "action2"],
                "medication_suggestions": ["med1", "med2"],
                "lifestyle_changes": ["change1", "change2"],
                "follow_up_care": ["care1", "care2"],
                "monitoring_guidelines": ["guideline1", "guideline2"],
                "emergency_indicators": ["indicator1", "indicator2"],
                "recovery_timeline": "estimated recovery time",
                "prevention_tips": ["tip1", "tip2"]
            }}
            
            Important: These are general recommendations. Always consult with healthcare professionals.
            """
            
            response = self.model.generate_content(
                prompt,
                safety_settings=self.safety_settings
            )
            
            try:
                response_text = response.text
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    json_text = response_text[json_start:json_end].strip()
                else:
                    json_text = response_text
                
                recommendations = json.loads(json_text)
                recommendations['timestamp'] = datetime.now().isoformat()
                recommendations['ai_model'] = 'gemini-pro'
                
                return recommendations
                
            except json.JSONDecodeError:
                return self._fallback_recommendations(patient_data)
                
        except Exception as e:
            logger.error(f"Error generating treatment recommendations: {e}")
            return self._fallback_recommendations(patient_data)

    async def analyze_queue_patterns(self, patients: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze queue patterns and provide insights
        """
        if not self.enabled:
            return self._fallback_queue_analysis(patients)
            
        try:
            # Prepare patient data for analysis
            patient_summary = []
            for patient in patients:
                patient_summary.append({
                    'age': patient.get('age', 0),
                    'symptoms': patient.get('symptoms', []),
                    'severity': patient.get('severity_level', 'Medium'),
                    'wait_time': patient.get('eta', 0)
                })
            
            prompt = f"""
            Analyze the following healthcare queue data and provide insights:
            
            Patient Data: {json.dumps(patient_summary, indent=2)}
            
            Provide analysis in JSON format:
            {{
                "common_symptoms": ["symptom1", "symptom2"],
                "age_distribution": {{"young": 0, "middle": 0, "elderly": 0}},
                "severity_trends": {{"critical": 0, "urgent": 0, "medium": 0, "low": 0}},
                "peak_conditions": ["condition1", "condition2"],
                "resource_recommendations": ["rec1", "rec2"],
                "staffing_insights": "staffing recommendations",
                "equipment_needs": ["equipment1", "equipment2"],
                "quality_improvements": ["improvement1", "improvement2"]
            }}
            """
            
            response = self.model.generate_content(
                prompt,
                safety_settings=self.safety_settings
            )
            
            try:
                response_text = response.text
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    json_text = response_text[json_start:json_end].strip()
                else:
                    json_text = response_text
                
                analysis = json.loads(json_text)
                analysis['timestamp'] = datetime.now().isoformat()
                analysis['ai_model'] = 'gemini-pro'
                
                return analysis
                
            except json.JSONDecodeError:
                return self._fallback_queue_analysis(patients)
                
        except Exception as e:
            logger.error(f"Error analyzing queue patterns: {e}")
            return self._fallback_queue_analysis(patients)

    async def generate_health_insights(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized health insights for patients
        """
        if not self.enabled:
            return self._fallback_insights(patient_data)
            
        try:
            symptoms = patient_data.get('symptoms', [])
            age = patient_data.get('age', 0)
            
            prompt = f"""
            Generate personalized health insights for a patient:
            
            Age: {age}
            Current Symptoms: {', '.join(symptoms) if isinstance(symptoms, list) else symptoms}
            
            Provide insights in JSON format:
            {{
                "health_score": 0.8,
                "risk_factors": ["factor1", "factor2"],
                "preventive_measures": ["measure1", "measure2"],
                "dietary_recommendations": ["food1", "food2"],
                "exercise_suggestions": ["exercise1", "exercise2"],
                "stress_management": ["tip1", "tip2"],
                "sleep_hygiene": ["tip1", "tip2"],
                "long_term_health": "long-term health advice",
                "follow_up_schedule": "recommended follow-up timing"
            }}
            """
            
            response = self.model.generate_content(
                prompt,
                safety_settings=self.safety_settings
            )
            
            try:
                response_text = response.text
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    json_text = response_text[json_start:json_end].strip()
                else:
                    json_text = response_text
                
                insights = json.loads(json_text)
                insights['timestamp'] = datetime.now().isoformat()
                insights['ai_model'] = 'gemini-pro'
                
                return insights
                
            except json.JSONDecodeError:
                return self._fallback_insights(patient_data)
                
        except Exception as e:
            logger.error(f"Error generating health insights: {e}")
            return self._fallback_insights(patient_data)

    def _fallback_analysis(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback analysis when Gemini API is not available"""
        symptoms = patient_data.get('symptoms', [])
        severity = patient_data.get('severity_level', 'Medium')
        
        return {
            "potential_conditions": ["Please consult a healthcare professional for proper diagnosis"],
            "immediate_care": ["Rest, stay hydrated, and monitor symptoms"],
            "red_flags": ["Seek immediate medical attention if symptoms worsen or persist"],
            "health_advice": ["Maintain good hygiene and follow medical advice"],
            "urgent_attention": "If experiencing severe pain, difficulty breathing, or other serious symptoms",
            "confidence_level": 0.3,
            "ai_insights": "AI analysis temporarily unavailable. Please consult healthcare professionals.",
            "timestamp": datetime.now().isoformat(),
            "ai_model": "fallback"
        }

    def _fallback_recommendations(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback recommendations when Gemini API is not available"""
        return {
            "immediate_actions": ["Rest and monitor symptoms", "Stay hydrated"],
            "medication_suggestions": ["Consult doctor for medication advice"],
            "lifestyle_changes": ["Maintain healthy diet", "Get adequate sleep"],
            "follow_up_care": ["Schedule follow-up appointment"],
            "monitoring_guidelines": ["Watch for symptom changes"],
            "emergency_indicators": ["Severe pain", "Difficulty breathing"],
            "recovery_timeline": "Varies based on condition",
            "prevention_tips": ["Maintain good health practices"],
            "timestamp": datetime.now().isoformat(),
            "ai_model": "fallback"
        }

    def _fallback_queue_analysis(self, patients: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback queue analysis when Gemini API is not available"""
        return {
            "common_symptoms": ["fever", "headache", "cough"],
            "age_distribution": {"young": 0, "middle": 0, "elderly": 0},
            "severity_trends": {"critical": 0, "urgent": 0, "medium": 0, "low": 0},
            "peak_conditions": ["respiratory", "gastrointestinal"],
            "resource_recommendations": ["Ensure adequate staffing"],
            "staffing_insights": "Monitor patient load and adjust staffing accordingly",
            "equipment_needs": ["Basic medical equipment"],
            "quality_improvements": ["Regular staff training", "Patient feedback collection"],
            "timestamp": datetime.now().isoformat(),
            "ai_model": "fallback"
        }

    def _fallback_insights(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback insights when Gemini API is not available"""
        return {
            "health_score": 0.7,
            "risk_factors": ["Age-related factors", "Lifestyle factors"],
            "preventive_measures": ["Regular check-ups", "Healthy lifestyle"],
            "dietary_recommendations": ["Balanced diet", "Adequate hydration"],
            "exercise_suggestions": ["Regular physical activity"],
            "stress_management": ["Adequate rest", "Relaxation techniques"],
            "sleep_hygiene": ["Consistent sleep schedule", "Good sleep environment"],
            "long_term_health": "Maintain regular healthcare check-ups",
            "follow_up_schedule": "As recommended by healthcare provider",
            "timestamp": datetime.now().isoformat(),
            "ai_model": "fallback"
        }

# Global instance
gemini_ai = GeminiAIService()
