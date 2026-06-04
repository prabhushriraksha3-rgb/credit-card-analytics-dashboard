import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# -----------------------------------
# Load Dataset
# -----------------------------------

df = pd.read_csv("credit_card_transactions.csv")

print("Dataset Loaded Successfully")
print(df.head())

# -----------------------------------
# Encode Categorical Columns
# -----------------------------------

encoders = {}

categorical_columns = [
    "Card_Type",
    "Merchant_Category",
    "Transaction_Status"
]

for col in categorical_columns:
    encoder = LabelEncoder()
    df[col] = encoder.fit_transform(df[col])

    encoders[col] = encoder

# -----------------------------------
# Features and Target
# -----------------------------------

X = df[
    [
        "Amount",
        "Card_Type",
        "Merchant_Category",
        "Transaction_Status"
    ]
]

y = df["Is_Fraud"]

# -----------------------------------
# Train Test Split
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# -----------------------------------
# Train Model
# -----------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------------
# Predictions
# -----------------------------------

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# -----------------------------------
# Save Model
# -----------------------------------

joblib.dump(model, "fraud_model.pkl")
joblib.dump(encoders, "encoders.pkl")

print("\nModel Saved Successfully")
print("fraud_model.pkl created")
print("encoders.pkl created")
