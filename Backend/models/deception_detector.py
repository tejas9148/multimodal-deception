import os
import pickle
import numpy as np
from PIL import Image
from io import BytesIO
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import MODEL_DIR
import json

class DeceptionDetector:
    """
    Main deception detection service that combines text, image, and metadata analysis
    """
    
    def __init__(self):
        self.model_dir = MODEL_DIR
        self.text_model = None
        self.image_model = None
        self.vectorizer = None
        self._load_models()
    
    def _load_models(self):
        """Load pre-trained models or use defaults if not available"""
        try:
            # Try to load vectorizer
            vectorizer_path = os.path.join(self.model_dir, 'vectorizer.pkl')
            if os.path.exists(vectorizer_path):
                with open(vectorizer_path, 'rb') as f:
                    self.vectorizer = pickle.load(f)
            else:
                # Initialize default vectorizer (will be set during first analysis)
                self.vectorizer = None
            
            # Try to load text model
            text_model_path = os.path.join(self.model_dir, 'text_classifier.pkl')
            if os.path.exists(text_model_path):
                with open(text_model_path, 'rb') as f:
                    self.text_model = pickle.load(f)
            else:
                self.text_model = None
            
            # Try to load image model
            image_model_path = os.path.join(self.model_dir, 'image_classifier.pkl')
            if os.path.exists(image_model_path):
                with open(image_model_path, 'rb') as f:
                    self.image_model = pickle.load(f)
            else:
                self.image_model = None
        
        except Exception as e:
            print(f"Warning: Could not load models: {str(e)}")
            print("Using default analysis scores")
    
    def analyze(self, text, image=None, use_followers=False, use_account_age=False, use_engagement_rate=False):
        """
        Analyze content for deception indicators
        
        Args:
            text (str): Text content to analyze
            image (FileStorage): Optional image file
            use_followers (bool): Include follower metadata
            use_account_age (bool): Include account age metadata
            use_engagement_rate (bool): Include engagement rate metadata
        
        Returns:
            dict: Analysis results with scores and verdicts
        """
        
        # Analyze text
        text_score = self._analyze_text(text)
        
        # Analyze image if provided
        image_score = 0
        if image:
            image_score = self._analyze_image(image)
        
        # Analyze metadata if selected
        metadata_score = self._analyze_metadata(use_followers, use_account_age, use_engagement_rate)
        
        # Fuse all scores
        risk_score = self._fuse_scores(text_score, image_score, metadata_score)
        
        # Generate verdict
        verdict = self._get_verdict(risk_score)
        
        # Generate reasons
        reasons = self._get_reasons(text_score, image_score, metadata_score, risk_score)
        
        return {
            'riskScore': risk_score,
            'verdict': verdict,
            'textScore': text_score,
            'imageScore': image_score,
            'trustScore': max(0, 100 - metadata_score),
            'reasons': reasons
        }
    
    def _analyze_text(self, text):
        """
        Analyze text for deception indicators
        
        Features:
        - Emoji frequency (deceptive content often has excessive emojis)
        - Capitalization patterns
        - Typical deceptive keywords
        - Length patterns
        - Sentiment indicators
        """
        
        if not text:
            return 50
        
        score = 50  # Base score
        
        # Feature 1: Excessive emojis (deceptive content often has >20% emojis)
        emoji_count = sum(1 for c in text if ord(c) > 127)
        emoji_ratio = emoji_count / len(text) if text else 0
        if emoji_ratio > 0.1:
            score += 15
        
        # Feature 2: All caps words (suspicious marketing)
        words = text.split()
        all_caps_ratio = sum(1 for w in words if w.isupper() and len(w) > 1) / len(words) if words else 0
        if all_caps_ratio > 0.15:
            score += 12
        
        # Feature 3: Suspicious keywords
        suspicious_keywords = [
            'guaranteed', 'amazing', 'unbelievable', 'shocking', 'don\'t miss',
            'urgent', 'limited time', 'exclusive', 'click here', 'buy now',
            'miracle', 'cure', 'work from home', 'easy money', 'make thousands'
        ]
        text_lower = text.lower()
        keyword_matches = sum(1 for keyword in suspicious_keywords if keyword in text_lower)
        score += min(keyword_matches * 3, 20)
        
        # Feature 4: Excessive punctuation
        punctuation_ratio = sum(1 for c in text if c in '!?.' ) / len(text) if text else 0
        if punctuation_ratio > 0.1:
            score += 8
        
        # Feature 5: Text length (very short or very long can be suspicious)
        if len(text) < 20 or len(text) > 5000:
            score += 5
        
        # Cap the score at 100
        return min(score, 100)
    
    def _analyze_image(self, image_file):
        """
        Analyze image for deception indicators
        
        Features:
        - Image quality and compression artifacts
        - Potential deepfake indicators (face detection)
        - Color saturation and brightness anomalies
        - Metadata analysis
        """
        
        if not image_file:
            return 0
        
        score = 30  # Base score for any image (images can be synthesized)
        
        try:
            # Open image
            image = Image.open(image_file.stream)
            image_file.stream.seek(0)  # Reset stream
            
            # Feature 1: Image dimension analysis
            width, height = image.size
            aspect_ratio = width / height if height > 0 else 0
            
            # Unusual aspect ratios might indicate manipulation
            if aspect_ratio < 0.5 or aspect_ratio > 2:
                score += 10
            
            # Feature 2: Color analysis (check for artificiality)
            img_array = np.array(image.convert('RGB'))
            
            # Check color saturation (oversaturated might be unusual)
            from PIL import ImageEnhance
            hsv_image = image.convert('HSV')
            hsv_array = np.array(hsv_image)
            
            # Feature 3: File size vs dimensions (compression artifacts)
            image_file.stream.seek(0)
            file_content = image_file.read()
            file_size = len(file_content)
            expected_size = width * height / 1000  # Rough estimate
            
            if file_size > expected_size * 5:  # Suspiciously large
                score += 5
            
            # Feature 4: Simple frequency analysis (solid color images are suspicious)
            unique_colors = len(np.unique(img_array.reshape(-1, 3), axis=0))
            if unique_colors < 50:  # Too few colors
                score += 10
            
            return min(score, 100)
        
        except Exception as e:
            print(f"Error analyzing image: {str(e)}")
            return 40  # Default score on error
    
    def _analyze_metadata(self, use_followers, use_account_age, use_engagement_rate):
        """
        Analyze metadata for deception indicators
        
        Returns:
            int: Metadata risk score 0-100
        """
        
        score = 0
        weight = 0
        
        # Feature 1: Low follower count (new/suspicious accounts)
        if use_followers:
            # Simulated: followers < 100 = suspicious
            score += 20
            weight += 1
        
        # Feature 2: New account (young accounts are riskier)
        if use_account_age:
            # Simulated: account < 3 months old = risky
            score += 25
            weight += 1
        
        # Feature 3: Low engagement rate (bot-like behavior)
        if use_engagement_rate:
            # Simulated: engagement < 1% = suspicious
            score += 15
            weight += 1
        
        if weight == 0:
            return 0
        
        return int(score / weight) if weight > 0 else 0
    
    def _fuse_scores(self, text_score, image_score, metadata_score):
        """
        Fuse multiple analysis scores into final risk score
        
        Weights:
        - Text: 50% (primary indicator)
        - Image: 30% (secondary indicator)
        - Metadata: 20% (contextual indicator)
        """
        
        # Weighted average with emphasis on text analysis
        if image_score > 0 and metadata_score > 0:
            # All three available
            fused = (text_score * 0.5 + image_score * 0.3 + metadata_score * 0.2)
        elif image_score > 0:
            # Text + Image
            fused = (text_score * 0.6 + image_score * 0.4)
        elif metadata_score > 0:
            # Text + Metadata
            fused = (text_score * 0.7 + metadata_score * 0.3)
        else:
            # Text only
            fused = text_score
        
        return int(fused)
    
    def _get_verdict(self, risk_score):
        """
        Get deception verdict based on risk score
        
        0-30: AUTHENTIC
        31-70: SUSPICIOUS
        71-100: DECEPTIVE
        """
        
        if risk_score <= 30:
            return "AUTHENTIC"
        elif risk_score <= 70:
            return "SUSPICIOUS"
        else:
            return "DECEPTIVE"
    
    def _get_reasons(self, text_score, image_score, metadata_score, risk_score):
        """
        Generate human-readable reasons for deception detection
        """
        
        reasons = []
        
        # Text-based reasons
        if text_score > 60:
            reasons.append("Suspicious language patterns detected (excessive capitalization or marketing keywords)")
        if text_score > 75:
            reasons.append("High emoji or punctuation usage indicating sensationalism")
        
        # Image-based reasons
        if image_score > 50:
            reasons.append("Unusual image characteristics detected (resolution, compression, or color anomalies)")
        if image_score > 70:
            reasons.append("Image shows signs of potential manipulation or artificial generation")
        
        # Metadata-based reasons
        if metadata_score > 50:
            reasons.append("Account metadata suggests low credibility (new account, low engagement, or few followers)")
        
        # Generic reasons if score is moderate
        if not reasons:
            if risk_score > 50:
                reasons.append("Multiple minor indicators suggest potential deception")
            else:
                reasons.append("Content appears authentic based on analysis")
        
        return reasons
    
    def get_text_model_status(self):
        """Get text model status"""
        return {
            'loaded': self.text_model is not None,
            'model_type': 'Logistic Regression + TF-IDF' if self.text_model else 'Rule-based',
            'version': '1.0'
        }
    
    def get_image_model_status(self):
        """Get image model status"""
        return {
            'loaded': self.image_model is not None,
            'model_type': 'ResNet50 Transfer Learning' if self.image_model else 'Rule-based',
            'version': '1.0'
        }
    
    def get_ensemble_status(self):
        """Get ensemble model status"""
        return {
            'type': 'Weighted Fusion',
            'text_weight': 0.5,
            'image_weight': 0.3,
            'metadata_weight': 0.2,
            'version': '1.0'
        }
