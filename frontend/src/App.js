import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

// Visible fields with labels
const FEATURE_LABELS = [
  { key: 'Time', label: 'Time (seconds since first transaction)' },
  { key: 'V1', label: 'V1 (anonymized feature 1)' },
  { key: 'V2', label: 'V2 (anonymized feature 2)' },
  { key: 'V3', label: 'V3 (anonymized feature 3)' },
  { key: 'V4', label: 'V4 (anonymized feature 4)' },
  { key: 'Amount', label: 'Amount (€)' }
];

function App() {
  // State
  const [inputs, setInputs] = useState({
    Time: 0,
    V1: 0,
    V2: 0,
    V3: 0,
    V4: 0,
    Amount: 0
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Handle change for labeled inputs
  const handleChange = (key, value) => {
    setInputs(prev => ({
      ...prev,
      [key]: parseFloat(value) || 0
    }));
  };

  // Build full 30-feature vector in SAME order as backend feature_cols
  const buildFeaturesArray = () => {
    const { Time, V1, V2, V3, V4, Amount } = inputs;

    return [
      Time,  // Time
      V1,    // V1
      V2,    // V2
      V3,    // V3
      V4,    // V4
      0,     // V5
      0,     // V6
      0,     // V7
      0,     // V8
      0,     // V9
      0,     // V10
      0,     // V11
      0,     // V12
      0,     // V13
      0,     // V14
      0,     // V15
      0,     // V16
      0,     // V17
      0,     // V18
      0,     // V19
      0,     // V20
      0,     // V21
      0,     // V22
      0,     // V23
      0,     // V24
      0,     // V25
      0,     // V26
      0,     // V27
      0,     // V28
      Amount // Amount
    ];
  };

  // Call backend
  const predictFraud = async () => {
    setLoading(true);
    setResult(null);
    try {
      const features = buildFeaturesArray();
     const response = await axios.post('http://127.0.0.1:5000/predict', {
  features
});

      setResult(response.data);
    } catch (error) {
      setResult({ error: 'Prediction failed. Check backend is running.' });
    }
    setLoading(false);
  };

  return (
    <div className="app">
      <header>
        <h1>🛡️ Credit Card Fraud Detection</h1>
        <p>Enter transaction details to check for fraud</p>
      </header>

      <main>
        <div className="form-container">
          <div className="field-list">
            {FEATURE_LABELS.map((field) => (
              <div key={field.key} className="field-row">
                <label>{field.label}</label>
                <input
                  type="number"
                  step="0.01"
                  value={inputs[field.key]}
                  onChange={(e) => handleChange(field.key, e.target.value)}
                  className="feature-input"
                />
              </div>
            ))}
          </div>

          <button
            onClick={predictFraud}
            disabled={loading}
            className="predict-btn"
          >
            {loading ? 'Analyzing...' : 'Detect Fraud'}
          </button>
        </div>

        {result && (
          <div className={`result ${result.fraud ? 'fraud' : 'safe'}`}>
            {!result.error && (
              <>
                <h2>
                  {result.fraud ? '🚨 FRAUD DETECTED' : '✅ Transaction Safe'}
                </h2>
                {result.fraud_probability !== undefined && (
                  <p>
                    Fraud Probability:{' '}
                    <strong>
                      {(result.fraud_probability * 100).toFixed(2)}%
                    </strong>
                  </p>
                )}
                {result.confidence && (
                  <p>
                    Model Confidence:{' '}
                    {(result.confidence * 100).toFixed(1)}%
                  </p>
                )}
              </>
            )}
            {result.error && (
              <p style={{ color: 'red', marginTop: '10px' }}>
                {result.error}
              </p>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
