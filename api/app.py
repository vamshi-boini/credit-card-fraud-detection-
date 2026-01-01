from flask import Flask, request, jsonify, render_template_string
import joblib
import pandas as pd
import numpy as np
import traceback
import os

from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Load model, scaler, and config
try:
    model = joblib.load('model.pkl')
    scaler = joblib.load('scaler.pkl')
    config = joblib.load('config.pkl')
    feature_cols = config['feature_cols']
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model, scaler, feature_cols = None, None, None

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Credit Card Fraud Detection API",
        "status": "ready",
        "features_required": len(feature_cols),
        "features": feature_cols
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "model_loaded": model is not None})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data or 'features' not in data:
            return jsonify({"error": "Missing 'features' array in request"}), 400
        
        features = np.array(data['features']).reshape(1, -1)
        if features.shape[1] != len(feature_cols):
            return jsonify({"error": f"Expected {len(feature_cols)} features, got {features.shape[1]}"}), 400
        
        # Scale and predict
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0][1]
        
        return jsonify({
            "fraud": bool(prediction),
            "fraud_probability": float(probability),
            "confidence": float(max(model.predict_proba(features_scaled)[0]))
        })
    except Exception as e:
        print(f"Prediction error: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@app.route('/predict_demo', methods=['GET'])
def predict_demo():
    # Demo with sample fraud/non-fraud
    demo_data = {
        "non_fraud": [0.0] * len(feature_cols),  # Simplified
        "fraud": [0.0] * 29 + [10000.0]  # High amount example
    }
    results = {}
    for label, features in demo_data.items():
        features_scaled = scaler.transform(np.array([features]))
        pred = model.predict(features_scaled)[0]
        prob = model.predict_proba(features_scaled)[0][1]
        results[label] = {"fraud": bool(pred), "probability": prob}
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
