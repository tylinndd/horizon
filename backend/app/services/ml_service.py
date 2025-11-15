"""
ML Service for outbreak detection and risk scoring
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


class MLService:
    """Machine learning service for outbreak detection"""
    
    def __init__(self):
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.is_fitted = False
    
    def compute_risk_score(
        self,
        features: Dict[str, float],
        region_id: str
    ) -> Dict:
        """
        Compute outbreak risk score from features
        
        Args:
            features: Dictionary of feature values (e.g., {'pharmacy_spike': 1.5, 'search_trend': 2.0})
            region_id: Region identifier
        
        Returns:
            Dictionary with risk_probability, risk_level, and contributing_factors
        """
        # Simple risk scoring logic (can be replaced with trained model)
        risk_factors = []
        risk_score = 0.0
        
        # Pharmacy spike factor
        if 'pharmacy_spike' in features:
            spike = features['pharmacy_spike']
            if spike > 1.5:
                risk_score += 0.3
                risk_factors.append(f"Pharmacy purchases increased by {spike:.1f}x")
        
        # Search trend factor
        if 'search_trend' in features:
            trend = features['search_trend']
            if trend > 1.5:
                risk_score += 0.25
                risk_factors.append(f"Search interest increased by {trend:.1f}x")
        
        # Hospital utilization factor
        if 'hospital_utilization' in features:
            util = features['hospital_utilization']
            if util > 0.8:
                risk_score += 0.25
                risk_factors.append(f"Hospital utilization at {util:.1%}")
        
        # Anomaly score factor
        if 'anomaly_score' in features:
            anomaly = features['anomaly_score']
            if anomaly > 0.7:
                risk_score += 0.2
                risk_factors.append(f"Anomaly detected (score: {anomaly:.2f})")
        
        # Normalize to 0-1 range
        risk_probability = min(risk_score, 1.0)
        
        # Determine risk level
        if risk_probability >= 0.75:
            risk_level = "critical"
        elif risk_probability >= 0.5:
            risk_level = "high"
        elif risk_probability >= 0.25:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            "risk_probability": risk_probability,
            "risk_level": risk_level,
            "contributing_factors": "; ".join(risk_factors) if risk_factors else "No significant risk factors detected"
        }
    
    def detect_anomaly(
        self,
        values: List[float],
        threshold: float = 0.7
    ) -> Dict:
        """
        Detect anomalies in a time series
        
        Args:
            values: List of metric values over time
            threshold: Anomaly score threshold
        
        Returns:
            Dictionary with anomaly_score and is_anomaly
        """
        if len(values) < 2:
            return {"anomaly_score": 0.0, "is_anomaly": False}
        
        # Simple anomaly detection using z-score
        values_array = np.array(values)
        mean = np.mean(values_array)
        std = np.std(values_array)
        
        if std == 0:
            return {"anomaly_score": 0.0, "is_anomaly": False}
        
        # Check the most recent value
        latest_value = values[-1]
        z_score = abs((latest_value - mean) / std)
        
        # Normalize z-score to 0-1 range (assuming max z-score of 3)
        anomaly_score = min(z_score / 3.0, 1.0)
        is_anomaly = anomaly_score > threshold
        
        return {
            "anomaly_score": anomaly_score,
            "is_anomaly": is_anomaly
        }

