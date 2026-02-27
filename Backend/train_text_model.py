import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

# -----------------------------------------
# 1. LOAD DATASET
# -----------------------------------------
df = pd.read_csv(os.path.join('final datasets', "final_master_dataset.csv"))

print("Total rows:", len(df))

# Remove empty text rows
df = df.dropna(subset=["text"])

X = df["text"]
y = df["label"]

# -----------------------------------------
# 2. TRAIN-TEST SPLIT
# -----------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------------------
# 3. TEXT → TF-IDF VECTORS
# -----------------------------------------
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# -----------------------------------------
# 4. TRAIN MODEL
# -----------------------------------------
model = LogisticRegression(max_iter=3000)
model.fit(X_train_vec, y_train)

# -----------------------------------------
# 5. TEST MODEL
# -----------------------------------------
pred = model.predict(X_test_vec)

print("\nAccuracy:", accuracy_score(y_test, pred))
print("\nClassification Report:\n", classification_report(y_test, pred))

 # -----------------------------------------
# 6. SAVE MODEL
# -----------------------------------------
# Save to Backend/models/ for backend usage
models_dir = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(models_dir, exist_ok=True)
with open(os.path.join(models_dir, "text_classifier.pkl"), "wb") as f:
    pickle.dump(model, f)
with open(os.path.join(models_dir, "vectorizer.pkl"), "wb") as f:
    pickle.dump(vectorizer, f)

print("\nModel saved as models/text_classifier.pkl")
print("Vectorizer saved as models/vectorizer.pkl")
with open(os.path.join(models_dir, "vectorizer.pkl"), "wb") as f:
    pickle.dump(vectorizer, f)

print("\nModel saved as models/text_classifier.pkl")
print("Vectorizer saved as models/vectorizer.pkl")
