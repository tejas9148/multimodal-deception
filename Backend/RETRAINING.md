# Deception Detection Model Retraining Workflow

This guide explains how to retrain your multimodal deception detection model and update the backend for new data or improved accuracy.

## 1. Prepare Your Dataset
- Format: CSV or TXT with columns for text, label (0=authentic, 1=deceptive), and optional metadata.
- Place your dataset in the Backend/data/ directory (e.g., data/dataset.csv).

## 2. Run the Training Script
- Open a terminal in Backend/
- Run:

    python train_text_model.py

- This will train the text classifier and save new model files (text_classifier.pkl, vectorizer.pkl) in Backend/models/.

## 3. Restart the Backend
- After training, restart the Flask backend to load the new model:

    python app.py

- If using a .env file, ensure CORS_ORIGINS includes your frontend port.

## 4. Validate
- Use the dashboard to submit test statements.
- Confirm scores and reasons are dynamic and reflect the new model.

## 5. Troubleshooting
- If errors occur, check:
  - Dataset format and path
  - Model files in Backend/models/
  - Console/logs for error messages

## 6. Optional: Retrain Image/Metadata Models
- If you have new image or metadata data, update and run the relevant training scripts (if available).

---
For further customization or advanced retraining, update train_text_model.py or add new scripts for additional modalities.
