import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
DATASET_PATH = "chronic_kidney_disease.csv"

if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(f"Error: Dataset file '{DATASET_PATH}' not found!")

df = pd.read_csv(DATASET_PATH)

# Target column
TARGET_COLUMN = "classification"
if TARGET_COLUMN not in df.columns:
    raise KeyError(f"Error: Column '{TARGET_COLUMN}' not found in dataset!")

# Drop 'id' column if it exists
if "id" in df.columns:
    df.drop(columns=["id"], inplace=True)

# Handle missing values
for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].fillna(df[col].mode()[0])  # Fill categorical missing values
    else:
        df[col] = df[col].fillna(df[col].median())  # Fill numerical missing values

# Encode categorical features
label_encoders = {}
categorical_columns = df.select_dtypes(include=["object"]).columns

for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Features & target
X = df.drop(columns=[TARGET_COLUMN])
y = df[TARGET_COLUMN]

# Ensure feature order consistency
feature_order = X.columns.tolist()

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train RandomForest model with optimized parameters
model = RandomForestClassifier(
    n_estimators=300,  # Increased trees for better accuracy
    max_depth=10,  # Limit tree depth to prevent overfitting
    random_state=42,
    class_weight="balanced"  # Handle class imbalance if present
)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model Accuracy: {accuracy:.4f}")
print("\n🔹 Classification Report:\n", classification_report(y_test, y_pred))

# Save model, scaler, and label encoders
MODEL_PATH = "kidney_disease_model.pkl"
SCALER_PATH = "scaler.pkl"
LABEL_ENCODERS_PATH = "label_encoders.pkl"
FEATURE_ORDER_PATH = "feature_order.pkl"  # Save feature order

joblib.dump(model, MODEL_PATH)
joblib.dump(scaler, SCALER_PATH)
joblib.dump(label_encoders, LABEL_ENCODERS_PATH)
joblib.dump(feature_order, FEATURE_ORDER_PATH)  

print(f"✅ Model saved as '{MODEL_PATH}'")
print(f"✅ Scaler saved as '{SCALER_PATH}'")
print(f"✅ LabelEncoders saved as '{LABEL_ENCODERS_PATH}'")
print(f"✅ Feature order saved as '{FEATURE_ORDER_PATH}'")
