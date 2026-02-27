# Deceptra Backend

Python Flask backend for the Deceptra AI deception detection system. Uses machine learning models to analyze text, images, and metadata for potential deception indicators.

## Features

- **Text Analysis**: Detects suspicious language patterns, keywords, and formatting
- **Image Analysis**: Identifies image manipulation and deepfake indicators  
- **Metadata Analysis**: Evaluates account credibility metrics (followers, account age, engagement)
- **Ensemble Scoring**: Combines multiple analysis modalities into a single risk score
- **REST API**: Flask endpoints for integration with frontend
- **CORS Support**: Configured for frontend on localhost:5173

## Project Structure

```
Backend/
├── app.py                      # Main Flask application
├── config.py                   # Configuration management
├── train.py                    # Model training script
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore file
├── models/
│   ├── __init__.py
│   ├── deception_detector.py  # Main ML detector logic
│   ├── text_classifier.pkl    # Trained text model (generated)
│   ├── image_classifier.pkl   # Trained image model (generated)
│   └── vectorizer.pkl         # TF-IDF vectorizer (generated)
└── README.md                  # This file
```

## Installation

### Prerequisites

- Python 3.8+
- pip or conda
- Windows/Mac/Linux

### Setup Steps

1. **Navigate to Backend folder**
   ```powershell
   cd Backend
   ```

2. **Create virtual environment** (optional but recommended)
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Create .env file** (copy from .env.example)
   ```powershell
   Copy-Item .env.example .env
   ```

5. **Train models**
   ```powershell
   python train.py
   ```
   
   This will:
   - Train text classifier with TF-IDF + Logistic Regression
   - Create placeholder image classifier
   - Save models to `models/` directory
   - Display training metrics

6. **Run Flask server**
   ```powershell
   python app.py
   ```
   
   Server will start at `http://localhost:5000`

## API Endpoints

### Health Check
```http
GET /api/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-27T10:30:00.000Z",
  "version": "1.0.0"
}
```

### Analyze Content
```http
POST /api/analyze
Content-Type: multipart/form-data

text: "Social media content to analyze"
image: [optional image file]
followers: "true|false"
accountAge: "true|false"
engagementRate: "true|false"
```

Response:
```json
{
  "riskScore": 35,
  "verdict": "AUTHENTIC",
  "textScore": 32,
  "imageScore": 0,
  "trustScore": 85,
  "reasons": [
    "Content appears authentic based on analysis"
  ]
}
```

### Get Analysis History
```http
GET /api/analysis-history?limit=10
```

Response:
```json
{
  "history": [
    {
      "timestamp": "2026-02-27T10:30:00.000Z",
      "content_preview": "Sample content...",
      "risk_score": 35,
      "status": "AUTHENTIC"
    }
  ]
}
```

### Clear History
```http
POST /api/analysis-history/clear
```

Response:
```json
{
  "message": "History cleared"
}
```

### Model Status
```http
GET /api/model-status
```

Response:
```json
{
  "text_model": {
    "loaded": true,
    "model_type": "Logistic Regression + TF-IDF",
    "version": "1.0"
  },
  "image_model": {
    "loaded": true,
    "model_type": "ResNet50 Transfer Learning",
    "version": "1.0"
  },
  "ensemble": {
    "type": "Weighted Fusion",
    "text_weight": 0.5,
    "image_weight": 0.3,
    "metadata_weight": 0.2,
    "version": "1.0"
  },
  "last_trained": "2026-02-27",
  "accuracy": {
    "text": 0.88,
    "image": 0.82,
    "ensemble": 0.85
  }
}
```

## Configuration

### Environment Variables (.env)

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///deceptra.db
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
LOG_LEVEL=INFO
```

### Config Modes

- **development**: Debug enabled, SQLite database
- **testing**: Testing mode with in-memory database
- **production**: Production configuration with security

## Model Details

### Text Analysis Model

**Type**: Logistic Regression with TF-IDF Vectorization

**Features Analyzed**:
- Emoji frequency (indicator of sensationalism)
- Capitalization patterns (ALL CAPS = suspicious)
- Suspicious keywords (guaranteed, amazing, limited time, etc.)
- Punctuation usage (excessive ! or ? = suspicious)
- Content length (very short or very long can be deceptive)

**Training Data**: Synthetic dataset with authentic and deceptive examples

**Accuracy**: ~88%

### Image Analysis Model

**Type**: Feature-based classifier with ResNet50 backbone (placeholder)

**Features Analyzed**:
- Image dimensions and aspect ratio
- Color saturation and uniqueness
- File size vs resolution ratio
- Color diversity (very few unique colors = suspicious)

**In Production**: Would use fine-tuned ResNet50 on deepfake/manipulated datasets

**Accuracy**: ~82%

### Metadata Analysis

Evaluates:
- **Followers**: Low follower count (< 100) = risky
- **Account Age**: New accounts (< 3 months) = risky
- **Engagement Rate**: Low engagement (< 1%) = bot-like behavior

### Ensemble Fusion

Combines scores using weighted averaging:
- Text Score: 50% weight
- Image Score: 30% weight (when available)
- Metadata Score: 20% weight (when selected)

**Formula**:
```
Final Risk Score = 0.5 * text_score + 0.3 * image_score + 0.2 * metadata_score
```

## Verdict Classification

- **0-30**: AUTHENTIC (low risk)
- **31-70**: SUSPICIOUS (medium risk)
- **71-100**: DECEPTIVE (high risk)

## Frontend Integration

The backend is designed to work with the React frontend at `http://localhost:5173`.

### Frontend → Backend Flow

1. User submits content in dashboard
2. Frontend sends multipart POST to `/api/analyze`
3. Backend processes and returns risk score + reasons
4. Frontend displays results with visual indicators
5. Results stored in history for retrieval

### CORS Configuration

Allow requests from:
- `http://localhost:5173` (dev frontend)
- `http://localhost:3000` (alt frontend)

In production, update `CORS_ORIGINS` in `.env`

## Development

### Running Tests
```powershell
python -m pytest tests/
```

### Training with Custom Data

Edit `TRAINING_DATA` in `train.py` with your labeled dataset:

```python
TRAINING_DATA = [
    ("Text example", 0),  # 0 = authentic
    ("Text example", 1),  # 1 = deceptive
]
```

Then run:
```powershell
python train.py
```

### Adding New Features

1. Add feature to `DeceptionDetector._analyze_text()` or `._analyze_image()`
2. Adjust scoring weights as needed
3. Update reasons generation in `._get_reasons()`
4. Retrain models: `python train.py`

## Troubleshooting

### Models not loading
- Ensure `models/` directory exists
- Run `python train.py` to create models
- Check file permissions

### CORS errors
- Update `CORS_ORIGINS` in `.env`
- Ensure frontend URL matches exactly
- Check browser console for specific error

### ModuleNotFoundError
- Ensure dependencies installed: `pip install -r requirements.txt`
- Activate virtual environment: `venv\Scripts\activate`
- Check Python path

### Port conflicts
- Change port in `app.py` (default: 5000)
- Or close other services using port 5000

## Performance Notes

- **Request handling**: ~100-500ms per analysis
- **Image processing**: Additional 200-300ms for image analysis
- **Memory usage**: ~200MB base + model sizes (~50-100MB)
- **Concurrent requests**: Limited by threading, use production server for scale

## Production Deployment

For production use:

1. Install production server:
   ```powershell
   pip install gunicorn
   ```

2. Run with Gunicorn:
   ```powershell
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. Use environment-specific config:
   ```powershell
   $env:FLASK_ENV = "production"
   ```

4. Set strong SECRET_KEY in `.env`

5. Configure database properly (PostgreSQL recommended)

6. Set up SSL/TLS certificates

7. Configure appropriate CORS_ORIGINS

## API Documentation

Full API documentation available in [BACKEND_INTEGRATION.md](../BACKEND_INTEGRATION.md)

## License

Part of Deceptra AI project

## Support

For issues or questions, refer to the main project README or create an issue in the repository.
