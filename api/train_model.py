import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib
import warnings
warnings.filterwarnings('ignore')

# Load dataset (place creditcard.csv in parent directory)
print("Loading dataset...")
df = pd.read_csv('../creditcard.csv')
print(f"Dataset shape: {df.shape}")
print(f"Fraud cases: {df['Class'].sum()} ({df['Class'].mean()*100:.2f}%)")

# Features and target
feature_cols = ['Time', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9',
                'V10', 'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19',
                'V20', 'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27', 'V28', 'Amount']
X = df[feature_cols]
y = df['Class']

# Train-test split with stratification
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Balance training set (undersampling)
train_pos_idx = y_train[y_train == 1].index
train_neg_idx = y_train[y_train == 0].sample(n=len(train_pos_idx), random_state=42).index
train_idx = np.concatenate([train_pos_idx, train_neg_idx])
X_train_bal = X.iloc[train_idx]
y_train_bal = y.iloc[train_idx]

print(f"Balanced training set: {X_train_bal.shape}")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_bal)
X_test_scaled = scaler.transform(X_test)

# Train Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train_scaled, y_train_bal)

# Evaluate
y_pred = model.predict(X_test_scaled)
y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
print("Classification Report:\n", classification_report(y_test, y_pred))
print(f"ROC-AUC: {roc_auc_score(y_test, y_pred_proba):.4f}")

# Save model and scaler
joblib.dump(model, 'model.pkl')
joblib.dump(scaler, 'scaler.pkl')
joblib.dump({'feature_cols': feature_cols}, 'config.pkl')
print("Model and scaler saved successfully!")
