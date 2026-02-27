import os
import json
import numpy as np
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from config import config, MODEL_DIR
from models.deception_detector import DeceptionDetector

# Initialize Flask app
app = Flask(__name__)

# Get configuration based on environment
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Enable CORS
CORS(app, origins=app.config['CORS_ORIGINS'].split(','))

# Initialize deception detector
detector = DeceptionDetector()

# Analysis history storage (in-memory for demo, replace with database)
analysis_history = []

# ==================== HEALTH CHECK ====================
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200

# ==================== ANALYSIS ENDPOINTS ====================
@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Main analysis endpoint
    
    Request:
        - text: (string) Social media content to analyze
        - image: (file) Optional image file
        - followers: (boolean) Include follower count
        - accountAge: (boolean) Include account age
        - engagementRate: (boolean) Include engagement rate
    
    Response:
        - riskScore: (int) 0-100 deception risk
        - verdict: (string) DECEPTIVE/SUSPICIOUS/AUTHENTIC
        - textScore: (int) Text analysis risk 0-100
        - imageScore: (int) Image analysis risk 0-100
        - trustScore: (int) Account trust 0-100
        - reasons: (array) Explanation of findings
    """
    try:
        # Get text content
        text_content = request.form.get('text', '').strip()
        if not text_content:
            return jsonify({'error': 'Text content is required'}), 400

        # Get image if provided
        image_file = None
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename == '':
                image_file = None

        # Get metadata selections
        use_followers = request.form.get('followers') == 'true'
        use_account_age = request.form.get('accountAge') == 'true'
        use_engagement_rate = request.form.get('engagementRate') == 'true'

        # Run analysis
        result = detector.analyze(
            text=text_content,
            image=image_file,
            use_followers=use_followers,
            use_account_age=use_account_age,
            use_engagement_rate=use_engagement_rate
        )

        # Store in history
        history_entry = {
            'timestamp': datetime.now().isoformat(),
            'content_preview': text_content[:50] + '...' if len(text_content) > 50 else text_content,
            'risk_score': result['riskScore'],
            'status': result['verdict']
        }
        analysis_history.append(history_entry)

        return jsonify(result), 200

    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

# ==================== HISTORY ENDPOINTS ====================
@app.route('/api/analysis-history', methods=['GET'])
def get_history():
    """Get analysis history"""
    try:
        limit = request.args.get('limit', default=10, type=int)
        return jsonify({
            'history': list(reversed(analysis_history[-limit:]))
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis-history/clear', methods=['POST'])
def clear_history():
    """Clear analysis history"""
    try:
        global analysis_history
        analysis_history = []
        return jsonify({'message': 'History cleared'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== MODEL STATUS ====================
@app.route('/api/model-status', methods=['GET'])
def model_status():
    """Get model status and performance metrics"""
    try:
        return jsonify({
            'text_model': detector.get_text_model_status(),
            'image_model': detector.get_image_model_status(),
            'ensemble': detector.get_ensemble_status(),
            'last_trained': '2026-02-27',
            'accuracy': {
                'text': 0.88,
                'image': 0.82,
                'ensemble': 0.85
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ==================== MAIN ====================
if __name__ == '__main__':
    # Create models directory if it doesn't exist
    os.makedirs(app.config['MODEL_DIR'], exist_ok=True)
    
    # Run Flask app
    debug = app.config['DEBUG']
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=debug,
        use_reloader=debug
    )
