"""
Train machine learning model to predict meningitis outbreaks
Using real WHO AFRO data patterns
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

print("="*60)
print("🦠 Training Meningitis Outbreak Predictor")
print("="*60)

# Load data
df = pd.read_csv("data/meningitis_west_africa.csv")
print(f"\n📊 Loaded {len(df)} records")

# Feature engineering - meningitis risk factors
# Based on known patterns: dry season (Dec-June) is high risk[citation:2]
df['dry_season'] = df['month'].apply(lambda x: 1 if x in [12,1,2,3,4,5,6] else 0)
df['harmattan_month'] = df['month'].apply(lambda x: 1 if x in [12,1,2] else 0)

# Create risk score based on historical data patterns
def calculate_risk(row):
    risk = 0
    if row['dry_season']:
        risk += 40
    if row['harmattan_month']:
        risk += 20
    if row['cases'] > 800:
        risk += 30
    elif row['cases'] > 400:
        risk += 15
    return min(risk, 100)

df['risk_score'] = df.apply(calculate_risk, axis=1)

# Features for prediction
feature_cols = ['month', 'cases', 'deaths', 'dry_season', 'harmattan_month', 'risk_score']
X = df[feature_cols]
y = df['outbreak']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n🎯 Model Accuracy: {accuracy:.1%}")
print(f"\n📋 Classification Report:")
print(classification_report(y_test, y_pred, target_names=["No Outbreak", "Outbreak"]))

# Feature importance
importance = pd.DataFrame({
    'feature': feature_cols,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(f"\n📊 Feature Importance:")
for _, row in importance.iterrows():
    print(f"   {row['feature']}: {row['importance']:.1%}")

# Save model
joblib.dump(model, "meningitis_model.pkl")
joblib.dump(feature_cols, "feature_cols.pkl")
print(f"\n✅ Model saved to meningitis_model.pkl")