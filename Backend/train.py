"""
Model training script for deception detection system
Trains text and image models using synthetic data
"""

import os
import pickle
import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from config import MODEL_DIR

# Training data (synthetic dataset for demonstration)
TRAINING_DATA = [
    # Deceptive examples (label=1)
    ("Check out this AMAZING work from home opportunity! GUARANTEED to make $5000/week! Limited time offer!!! Click here now!!!", 1),
    ("You won't BELIEVE what this celebrity does to stay young. This one weird trick doctors HATE! Exclusive offer inside!", 1),
    ("LIMITED TIME! Get free Miracle Cure for all diseases! Unbelievable results! Don't miss out!!!", 1),
    ("Work from home and make THOUSANDS weekly! No experience needed! This shocking secret will change your life!", 1),
    ("EXCLUSIVE: This shocking video was BANNED from YouTube! MUST WATCH!!! 😱😱😱", 1),
    ("🚀🚀🚀 URGENT: Buy now or regret FOREVER! Only 3 spots left! CLICK HERE IMMEDIATELY!!!!", 1),
    ("You'll never believe what happened next... SHOCKING content inside! Don't miss this EXCLUSIVE offer!!", 1),
    ("GUARANTEED weight loss! Lose 30 pounds in 30 days with this MIRACLE pill! 100% natural!!!!", 1),
    
    # Authentic examples (label=0)
    ("I really enjoyed the meeting today. We discussed the quarterly results and outlined our strategy for next quarter.", 0),
    ("The weather is nice today. I went for a walk in the park and saw some birds.", 0),
    ("Project deadline is next Friday. Please make sure to submit your work on time.", 0),
    ("I'm learning Python programming. It's an interesting language with many applications.", 0),
    ("The coffee at the new cafe is excellent. I recommend trying their espresso.", 0),
    ("My team completed the sprint successfully. We delivered all planned features.", 0),
    ("The book was informative and well-written. I learned a lot about the topic.", 0),
    ("I watched a documentary about climate change. It provided useful information.", 0),
]

def train_text_model():
    """Train text deception detection model"""
    print("Training text model...")
    
    # Prepare data
    texts = [item[0] for item in TRAINING_DATA]
    labels = np.array([item[1] for item in TRAINING_DATA])
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    # Create pipeline with TF-IDF and Logistic Regression
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=100, ngram_range=(1, 2))),
        ('classifier', LogisticRegression(max_iter=1000, random_state=42))
    ])
    
    # Train model
    pipeline.fit(X_train, y_train)
    
    # Evaluate
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    print(f"  Accuracy:  {accuracy:.2%}")
    print(f"  Precision: {precision:.2%}")
    print(f"  Recall:    {recall:.2%}")
    print(f"  F1-Score:  {f1:.2%}")
    
    # Save model
    model_dir = MODEL_DIR
    os.makedirs(model_dir, exist_ok=True)
    
    # Save vectorizer
    vectorizer = pipeline.named_steps['tfidf']
    vectorizer_path = os.path.join(model_dir, 'vectorizer.pkl')
    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    print(f"  Saved vectorizer to {vectorizer_path}")
    
    # Save classifier
    classifier = pipeline.named_steps['classifier']
    classifier_path = os.path.join(model_dir, 'text_classifier.pkl')
    with open(classifier_path, 'wb') as f:
        pickle.dump(classifier, f)
    print(f"  Saved model to {classifier_path}")
    
    return pipeline

def train_image_model():
    """
    Train image deception detection model
    
    Note: This is a placeholder. In production, you would:
    1. Use a pre-trained ResNet50 from torchvision
    2. Fine-tune on labeled deepfake/manipulated image dataset
    3. Save the model weights
    
    For now, we'll create a simple classifier
    """
    print("Image model training (note: using synthetic rules)...")
    
    # In a real implementation, this would be a CNN or transfer learning model
    # For now, we'll save a simple object indicating model is available
    
    model_info = {
        'type': 'ResNet50-Transfer',
        'pretrained': True,
        'num_classes': 2,
        'input_size': 224,
        'note': 'Placeholder for pre-trained image model'
    }
    
    model_dir = MODEL_DIR
    os.makedirs(model_dir, exist_ok=True)
    
    image_model_path = os.path.join(model_dir, 'image_classifier.pkl')
    with open(image_model_path, 'wb') as f:
        pickle.dump(model_info, f)
    
    print(f"  Saved image model info to {image_model_path}")
    print(f"  (In production, this would be a fine-tuned ResNet50)")

def main():
    """Main training function"""
    print("=" * 60)
    print("Deception Detection Model Training")
    print("=" * 60)
    print()
    
    try:
        train_text_model()
        print()
        train_image_model()
        print()
        print("=" * 60)
        print("Training completed successfully!")
        print("Models saved to:", MODEL_DIR)
        print("=" * 60)
    
    except Exception as e:
        print(f"Error during training: {e}")
        raise

if __name__ == '__main__':
    main()
