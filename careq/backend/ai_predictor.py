"""
AI-Powered Waiting Time Prediction System
Uses machine learning to predict patient waiting times based on various factors
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json
import logging

logger = logging.getLogger(__name__)

class AIWaitingTimePredictor:
    def __init__(self):
        self.model_weights = {
            'severity_multiplier': {
                'Critical': 0.1,    # 1-5 minutes
                'Urgent': 0.3,      # 5-15 minutes  
                'Medium': 0.6,      # 15-30 minutes
                'Low': 1.0          # 30-60 minutes
            },
            'queue_length_factor': 0.8,
            'time_of_day_factor': {
                'morning': 1.2,     # 6-12 AM
                'afternoon': 1.0,   # 12-6 PM
                'evening': 0.8,     # 6-12 PM
                'night': 0.6        # 12-6 AM
            },
            'day_of_week_factor': {
                'Monday': 1.3,
                'Tuesday': 1.2,
                'Wednesday': 1.1,
                'Thursday': 1.0,
                'Friday': 0.9,
                'Saturday': 0.7,
                'Sunday': 0.6
            },
            'symptom_complexity': {
                'simple': 0.8,      # Single symptom
                'moderate': 1.0,    # 2-3 symptoms
                'complex': 1.3      # 4+ symptoms
            }
        }
        
        # Historical data for learning
        self.historical_data = []
        self.learning_rate = 0.1
        
    def predict_waiting_time(self, patient_data: Dict[str, Any], current_queue: List[Dict]) -> Dict[str, Any]:
        """
        Predict waiting time for a patient using AI/ML algorithms
        """
        try:
            # Extract features
            features = self._extract_features(patient_data, current_queue)
            
            # Calculate base waiting time
            base_time = self._calculate_base_waiting_time(features)
            
            # Apply AI adjustments
            ai_adjusted_time = self._apply_ai_adjustments(base_time, features)
            
            # Add confidence score
            confidence = self._calculate_confidence(features)
            
            # Generate insights
            insights = self._generate_insights(features, ai_adjusted_time)
            
            return {
                'predicted_wait_time': max(1, int(ai_adjusted_time)),
                'confidence_score': confidence,
                'factors_considered': features,
                'insights': insights,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in AI prediction: {e}")
            return self._fallback_prediction(patient_data, current_queue)
    
    def _extract_features(self, patient_data: Dict, current_queue: List[Dict]) -> Dict[str, Any]:
        """Extract relevant features for AI prediction"""
        now = datetime.now()
        
        # Queue features
        queue_length = len([p for p in current_queue if not p.get('called', False)])
        high_priority_in_queue = len([p for p in current_queue 
                                    if not p.get('called', False) and p.get('severity_level') in ['Critical', 'Urgent']])
        
        # Patient features
        severity = patient_data.get('severity_level', 'Medium')
        symptoms = patient_data.get('symptoms', [])
        age = patient_data.get('age', 30)
        
        # Time features
        hour = now.hour
        day_of_week = now.strftime('%A')
        
        # Determine time of day
        if 6 <= hour < 12:
            time_period = 'morning'
        elif 12 <= hour < 18:
            time_period = 'afternoon'
        elif 18 <= hour < 24:
            time_period = 'evening'
        else:
            time_period = 'night'
        
        # Symptom complexity
        symptom_count = len(symptoms) if isinstance(symptoms, list) else 1
        if symptom_count == 1:
            complexity = 'simple'
        elif symptom_count <= 3:
            complexity = 'moderate'
        else:
            complexity = 'complex'
        
        return {
            'queue_length': queue_length,
            'high_priority_in_queue': high_priority_in_queue,
            'severity_level': severity,
            'symptom_complexity': complexity,
            'symptom_count': symptom_count,
            'age': age,
            'time_of_day': time_period,
            'day_of_week': day_of_week,
            'hour': hour
        }
    
    def _calculate_base_waiting_time(self, features: Dict) -> float:
        """Calculate base waiting time using weighted factors"""
        base_time = 15  # Base 15 minutes
        
        # Severity multiplier
        severity_mult = self.model_weights['severity_multiplier'].get(
            features['severity_level'], 0.6
        )
        
        # Queue length factor
        queue_factor = 1 + (features['queue_length'] * self.model_weights['queue_length_factor'])
        
        # Time of day factor
        time_factor = self.model_weights['time_of_day_factor'].get(
            features['time_of_day'], 1.0
        )
        
        # Day of week factor
        day_factor = self.model_weights['day_of_week_factor'].get(
            features['day_of_week'], 1.0
        )
        
        # Symptom complexity factor
        complexity_factor = self.model_weights['symptom_complexity'].get(
            features['symptom_complexity'], 1.0
        )
        
        # Calculate final time
        predicted_time = base_time * severity_mult * queue_factor * time_factor * day_factor * complexity_factor
        
        return predicted_time
    
    def _apply_ai_adjustments(self, base_time: float, features: Dict) -> float:
        """Apply AI/ML adjustments based on historical patterns"""
        # Simulate learning from historical data
        if len(self.historical_data) > 10:
            # Calculate average accuracy and adjust
            recent_accuracy = self._calculate_recent_accuracy()
            if recent_accuracy < 0.7:  # If accuracy is low, adjust
                adjustment_factor = 1 + (0.7 - recent_accuracy) * 0.2
                base_time *= adjustment_factor
        
        # Apply dynamic adjustments based on current conditions
        if features['high_priority_in_queue'] > 3:
            base_time *= 1.2  # More high priority patients = longer wait
        
        if features['time_of_day'] == 'morning' and features['queue_length'] > 5:
            base_time *= 1.3  # Morning rush hour
        
        # Age-based adjustments
        if features['age'] < 18 or features['age'] > 65:
            base_time *= 0.9  # Faster service for vulnerable populations
        
        return base_time
    
    def _calculate_confidence(self, features: Dict) -> float:
        """Calculate confidence score for the prediction"""
        confidence = 0.8  # Base confidence
        
        # Higher confidence for more data points
        if len(self.historical_data) > 50:
            confidence += 0.1
        
        # Lower confidence for unusual patterns
        if features['queue_length'] > 10:
            confidence -= 0.1
        
        if features['severity_level'] == 'Critical' and features['queue_length'] > 5:
            confidence -= 0.2
        
        return max(0.1, min(1.0, confidence))
    
    def _generate_insights(self, features: Dict, predicted_time: float) -> List[str]:
        """Generate insights about the prediction"""
        insights = []
        
        if features['severity_level'] == 'Critical':
            insights.append("Critical priority - you'll be seen very soon")
        elif features['severity_level'] == 'Urgent':
            insights.append("Urgent priority - shorter wait time expected")
        
        if features['queue_length'] == 0:
            insights.append("No patients ahead - immediate attention")
        elif features['queue_length'] <= 3:
            insights.append("Short queue - quick service expected")
        elif features['queue_length'] <= 7:
            insights.append("Moderate queue - reasonable wait time")
        else:
            insights.append("Longer queue - please be patient")
        
        if features['time_of_day'] == 'morning':
            insights.append("Morning rush hour - busier than usual")
        elif features['time_of_day'] == 'evening':
            insights.append("Evening hours - typically less busy")
        
        if features['symptom_complexity'] == 'complex':
            insights.append("Complex symptoms may require longer consultation")
        
        return insights
    
    def _fallback_prediction(self, patient_data: Dict, current_queue: List[Dict]) -> Dict[str, Any]:
        """Fallback prediction when AI fails"""
        queue_length = len([p for p in current_queue if not p.get('called', False)])
        severity = patient_data.get('severity_level', 'Medium')
        
        # Simple fallback calculation
        if severity == 'Critical':
            wait_time = 5
        elif severity == 'Urgent':
            wait_time = 10 + queue_length * 2
        elif severity == 'Medium':
            wait_time = 20 + queue_length * 3
        else:
            wait_time = 30 + queue_length * 4
        
        return {
            'predicted_wait_time': max(1, wait_time),
            'confidence_score': 0.5,
            'factors_considered': {'queue_length': queue_length, 'severity': severity},
            'insights': ['Using fallback prediction - AI temporarily unavailable'],
            'timestamp': datetime.now().isoformat()
        }
    
    def update_model(self, actual_wait_time: int, predicted_wait_time: int, features: Dict):
        """Update the model with actual vs predicted data"""
        self.historical_data.append({
            'actual_wait_time': actual_wait_time,
            'predicted_wait_time': predicted_wait_time,
            'features': features,
            'timestamp': datetime.now().isoformat(),
            'accuracy': 1 - abs(actual_wait_time - predicted_wait_time) / max(actual_wait_time, predicted_wait_time)
        })
        
        # Keep only recent data (last 100 records)
        if len(self.historical_data) > 100:
            self.historical_data = self.historical_data[-100:]
    
    def _calculate_recent_accuracy(self) -> float:
        """Calculate recent prediction accuracy"""
        if len(self.historical_data) < 5:
            return 0.8
        
        recent_data = self.historical_data[-10:]  # Last 10 predictions
        accuracies = [record['accuracy'] for record in recent_data]
        return sum(accuracies) / len(accuracies)
    
    def get_queue_analytics(self, current_queue: List[Dict]) -> Dict[str, Any]:
        """Get AI-powered queue analytics"""
        if not current_queue:
            return {
                'total_patients': 0,
                'average_wait_time': 0,
                'priority_distribution': {},
                'peak_hour_prediction': 'No data available',
                'recommendations': ['No patients in queue']
            }
        
        # Calculate analytics
        total_patients = len(current_queue)
        uncalled_patients = [p for p in current_queue if not p.get('called', False)]
        
        # Priority distribution
        priority_dist = {}
        for patient in uncalled_patients:
            severity = patient.get('severity_level', 'Medium')
            priority_dist[severity] = priority_dist.get(severity, 0) + 1
        
        # Average wait time
        avg_wait = sum(p.get('eta', 15) for p in uncalled_patients) / len(uncalled_patients) if uncalled_patients else 0
        
        # Peak hour prediction
        now = datetime.now()
        if 9 <= now.hour <= 11:
            peak_prediction = "Currently in peak hours (9-11 AM)"
        elif 14 <= now.hour <= 16:
            peak_prediction = "Currently in peak hours (2-4 PM)"
        else:
            peak_prediction = f"Peak hours expected at 9-11 AM or 2-4 PM"
        
        # Recommendations
        recommendations = []
        if len(uncalled_patients) > 8:
            recommendations.append("High queue volume - consider additional staff")
        if priority_dist.get('Critical', 0) > 2:
            recommendations.append("Multiple critical patients - prioritize urgent care")
        if avg_wait > 45:
            recommendations.append("Long wait times - inform patients of delays")
        
        return {
            'total_patients': total_patients,
            'uncalled_patients': len(uncalled_patients),
            'average_wait_time': round(avg_wait, 1),
            'priority_distribution': priority_dist,
            'peak_hour_prediction': peak_prediction,
            'recommendations': recommendations,
            'ai_confidence': 0.85
        }

# Global instance
ai_predictor = AIWaitingTimePredictor()
