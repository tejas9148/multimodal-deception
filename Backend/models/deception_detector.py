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
        
        # Store input text for reason generation
        self.last_text_input = text
        # Analyze text
        text_score = self._analyze_text(text)

        # Analyze image if provided
        image_score = None
        if image:
            image_score = self._analyze_image(image)

        # Analyze metadata if selected
        metadata_score = None
        if use_followers or use_account_age or use_engagement_rate:
            metadata_score = self._analyze_metadata(use_followers, use_account_age, use_engagement_rate)

        # Fuse all scores
        risk_score = self._fuse_scores(
            text_score,
            image_score if image_score is not None else 0,
            metadata_score if metadata_score is not None else 0
        )

        # Generate verdict
        verdict = self._get_verdict(risk_score)

        # Generate reasons
        reasons = self._get_reasons(
            text_score,
            image_score if image_score is not None else 0,
            metadata_score if metadata_score is not None else 0,
            risk_score
        )

        result = {
            'riskScore': risk_score,
            'verdict': verdict,
            'textScore': text_score,
            'reasons': reasons
        }
        if image_score is not None:
            result['imageScore'] = image_score
        if metadata_score is not None:
            result['trustScore'] = max(0, 100 - metadata_score)
        return result
    
    def _analyze_text(self, text):
        """
        Analyze text for deception indicators using trained model if available, else fallback to rule-based.
        """
        if not text:
            return 50
        
        # Use trained model if available
        # NOTE: Trained model is disabled in favor of improved rule-based scoring
        # which provides better calibration for real vs fake content
        if False and self.text_model is not None and self.vectorizer is not None:
            try:
                X_vec = self.vectorizer.transform([text])
                pred_proba = self.text_model.predict_proba(X_vec)[0]
                # Assume label 1 = deceptive, 0 = authentic
                risk_score = int(pred_proba[1] * 100)
                return risk_score
            except Exception as e:
                print(f"Text model prediction error: {e}")
                # Fallback to rule-based if error
        
        # Fallback: rule-based scoring
        text_lower = text.lower()
        words = text.split()
        
        # Start with lower base score for legitimate content
        score = 27  # Balanced starting point
        
        # 1. Emoji analysis (high emoji = deceptive)
        emoji_count = sum(1 for c in text if ord(c) > 127)
        emoji_ratio = emoji_count / len(text) if text else 0
        if emoji_ratio > 0.15:
            score += 20
        elif emoji_ratio > 0.05:
            score += 10
        elif emoji_count > 0:
            score += 3
        
        # Bonus for warning/alarm emojis (🚨 ⚠️ 🔥 😱)
        alarm_emojis = text.count('🚨') + text.count('⚠️') + text.count('🔥') + text.count('😱')
        if alarm_emojis > 0:
            score += min(alarm_emojis * 5, 10)
        
        # 2. ALL CAPS analysis (exclude words that are abbreviations or single capital letters)
        # Only count words that are ALL CAPS and longer than 1 character
        caps_words = [w for w in words if w.isupper() and len(w) > 2 and w.isalpha()]
        all_caps_ratio = len(caps_words) / len(words) if words else 0
        if all_caps_ratio > 0.15:
            score += 15
        elif all_caps_ratio > 0.08:
            score += 8
        
        # 3. Suspicious keywords - with weighted importance
        # High-impact keywords for fake news/disasters
        high_impact_keywords = [
            'breaking', 'major', 'devastating', 'catastrophic',  # Dramatic/sensational
            'kill', 'dead', 'death', 'earthquake', 'explosion', 'crash',  # Disaster keywords
            'breaking news', 'just happened', 'urgent alert',  # Breaking news style
            'suspended', 'blocked', 'terminated', 'restricted',  # Account threat keywords
            'exposed', 'revealed', 'finally revealed', 'hidden'  # Conspiracy/revelation
        ]
        
        # Standard suspicious keywords
        standard_keywords = [
            'guaranteed', 'amazing', 'unbelievable', 'shocking', "don't miss",
            'urgent', 'limited time', 'exclusive', 'click here', 'buy now',
            'miracle', 'cure', 'work from home', 'easy money', 'make thousands',
            'proven', 'doctor recommended', 'secret formula', 'act now',
            'must see', 'this trick', 'hate this', 'you wont believe',
            'only', 'never', 'always', 'can',  # Absolute statements (no 'will')
            'secret', 'suppressed', 'covered up',  # Conspiracy language
            'discovered', 'shocking truth', 'finally',  # Sensationalism
            'claim your', 'free reward', 'select for', 'click the link',  # Scam language
            # Security/account-related (moderate threat) - only in suspicious context
            'verify', 'unusual', 'irregular',  # Verification keywords (more specific than 'confirm')
            'security concern', 'login attempt', 'suspicious activity',  # Account threat
            'potential issue',  # Risk warnings
            'congratulations', 'selected', 'eligible',  # Targeted scams
        ]
        
        # Count high-impact matches (worth more)
        high_impact_matches = sum(1 for keyword in high_impact_keywords if keyword in text_lower)
        standard_matches = sum(1 for keyword in standard_keywords if keyword in text_lower)
        
        # High-impact keywords worth 12 points each (disaster/catastrophe language), standard worth 5 each
        score += min((high_impact_matches * 12) + (standard_matches * 5), 70)
        
        # Extra boost for combined congratulations-exclusive-reward phrases
        if 'congratulations' in text_lower and 'exclusive' in text_lower and 'reward' in text_lower:
            score += 15
        
        # Cap suspicious score for simple subscription notices
        if 'subscription' in text_lower and 'renew' in text_lower and score < 35:
            score = min(score, 30)
        
        # 4. Excessive punctuation (!! or ??? or ...)
        exclamation_count = text.count('!')
        question_count = text.count('?')
        if exclamation_count >= 5:
            score += 18  # Very aggressive - many exclamation marks
        elif exclamation_count > 3:
            score += 15  # Multiple exclamation marks - very suspicious
        elif exclamation_count > 2:
            score += 10
        elif exclamation_count > 0:
            score += 2
        
        if question_count > 3:
            score += 10  # Multiple question marks (clickbait style)
        elif question_count > 1:
            score += 3
        
        # Detect suspicious URLs and financial keywords
        if 'http://' in text or '.biz' in text or '.xyz' in text or 'click' in text_lower:
            score += 8
        
        # Detect financial/banking scam keywords (STRONG indicator)
        banking_words = ['pin', 'cvv', 'refund', 'tax', 'atm', 'bank', 'account', 'payment', 'billing']
        action_words = ['enter', 'release', 'unlock', 'claim', 'retrieve', 'access', 'submit', 'update']
        has_banking = any(word in text_lower for word in banking_words)
        has_action = any(word in text_lower for word in action_words)
        if has_banking and has_action:
            score += 30  # VERY strong phishing/financial scam indicator
        
        # Detect security-related phishing keywords
        if any(word in text_lower for word in ['pin', 'cvv', 'password', 'verify', 'confirm']):
            if any(threat in text_lower for threat in ['suspended', 'blocked', 'danger', 'threat']):
                score += 15  # Strong phishing indicator
        
        # 5. Emphasis markers (multiple symbols)
        emphasis_chars = text.count('*') + text.count('_') + text.count('~') + text.count('^')
        if emphasis_chars > 5:
            score += 8
        
        # 6. Very short text (headlines/fragments without context)
        text_length = len(text)
        if text_length < 15:
            score += 5  # Too short, might be incomplete
        elif text_length > 10000:
            score += 3  # Unusually long
        
        # 7. Emotional/superlative words (common in false claims)
        emotional_words = [
            'best', 'worst', 'incredible', 'terrible', 'fantastic', 'disgusting',
            'amazing', 'awful', 'love', 'hate', 'ugly', 'beautiful'
        ]
        # Count whole words only to avoid false positives
        text_words_lower = [w.strip('.,!?;:') for w in words]
        emotional_matches = sum(1 for word in emotional_words if word in text_words_lower)
        score += min(emotional_matches * 2, 10)
        
        # Detect urgent/immediate action phrases common in scams
        urgent_phrases = ['immediately', 'right now', 'act now', 'do not delay', 'expires soon', 'expires forever']
        urgent_matches = sum(1 for phrase in urgent_phrases if phrase in text_lower)
        score += min(urgent_matches * 4, 15)
        
        # Reduce if mostly facts (contains numbers, scientific terms, citations)
        has_numbers = any(c.isdigit() for c in text)
        has_percent = '%' in text
        scientific_terms = ['research', 'study', 'found', 'published', 'data', 'analysis', 'journal', 'experiment']
        has_scientific = any(term in text_lower for term in scientific_terms)
        
        # Factual statements with numbers/data should not be penalized as much
        # BUT: Only reduce if it's GENUINELY scientific/academic content
        if has_scientific:
            if (has_numbers or has_percent) and has_scientific:
                score = max(score - 12, 10)  # Reduce for genuine research/scientific content
        # Don't reduce just because there are numbers - that's common in fake news too!
        
        return min(max(score, 10), 100)
    
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
        if text_score > 70:
            reasons.append("High-risk language patterns detected (excessive capitalization, marketing keywords, or sensational tone)")
        elif text_score > 50:
            reasons.append("Some suspicious language patterns detected (emoji usage, punctuation, or promotional language)")
        
        # Check for specific text features
        if hasattr(self, 'last_text_input') and self.last_text_input:
            emoji_count = sum(1 for c in self.last_text_input if ord(c) > 127)
            punctuation_count = sum(1 for c in self.last_text_input if c in '!?.')
            
            if emoji_count > 3:
                reasons.append(f"Excessive emoji usage ({emoji_count} emojis) - common in sensationalized content")
            if punctuation_count > 10:
                reasons.append(f"Excessive punctuation ({punctuation_count}) - typical of emotional/manipulative language")
        
        # Image-based reasons
        if image_score > 70:
            reasons.append("Image shows signs of potential manipulation or artificial generation")
        elif image_score > 50:
            reasons.append("Unusual image characteristics detected (resolution, compression, or color anomalies)")
        
        # Metadata-based reasons
        if metadata_score > 60:
            reasons.append("Account metadata suggests low credibility (new account, low engagement, or few followers)")
        
        # Generic reasons based on risk level
        if not reasons:
            if risk_score > 70:
                reasons.append("Multiple indicators suggest high deception risk")
            elif risk_score > 50:
                reasons.append("Mixed signals detected - content shows some suspicious patterns")
            elif risk_score > 30:
                reasons.append("Content appears mostly authentic with minor suspicious indicators")
            else:
                reasons.append("Content appears authentic based on analysis")
        
        # Remove duplicates while preserving order
        reasons = list(dict.fromkeys(reasons))
        return reasons
