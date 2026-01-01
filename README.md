
# 🛡️ Credit Card Fraud Detection (ML + Web App)

A full-stack **credit card fraud detection** project using a machine learning model (Random Forest) with a Flask API backend and a React frontend interface. The app predicts whether a transaction is fraudulent based on anonymized features from a real-world dataset.

---

## 🚀 Features

- Trained ML model on the popular **Kaggle Credit Card Fraud Detection** dataset.
- Handles **highly imbalanced data** using undersampling techniques.
- REST **API** built with Flask (`/predict`, `/health` endpoints).
- Modern **React UI** with a clean design and labeled inputs.
- Ready for deployment on **Vercel** (frontend + backend).

---

## 📂 Project Structure

```bash
credit-card-fraud-detection-ml/
├── api/
│   ├── app.py              # Flask API (backend)
│   ├── train_model.py      # Script to train and save model
│   ├── model.pkl           # Trained model (not in repo if ignored)
│   ├── scaler.pkl          # Scaler (not in repo if ignored)
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js          # React UI logic
│   │   ├── App.css         # Styling
│   │   └── index.js        # React entry point
│   └── package.json        # Frontend dependencies & scripts
├── vercel.json             # Vercel deployment config
├── .gitignore
└── README.md
Note: venv/, node_modules/, creditcard.csv and *.pkl are ignored and not pushed to GitHub.

📊 Dataset
This project uses the Credit Card Fraud Detection dataset from Kaggle. The dataset contains anonymized features (V1–V28), Time, Amount, and target Class (0 = normal, 1 = fraud).

Dataset link: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

How to add the dataset locally
Download creditcard.csv from Kaggle.

Place creditcard.csv in the project root (same level as api/ and frontend/).

The training script api/train_model.py expects the file at ../creditcard.csv relative to the api folder.

The CSV file is not included in this repository due to GitHub’s file size limit and best practices.

🧠 Model Training (Backend)
1. Create and activate Python virtual environment
bash
cd credit-card-fraud-detection-ml

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
# source venv/bin/activate
2. Install backend dependencies
bash
cd api
pip install -r requirements.txt
3. Train the model
Make sure creditcard.csv is in the project root, then:

bash
python train_model.py
This will:

Load and split the dataset.

Undersample the majority class (non-fraud) to handle imbalance.

Scale features with StandardScaler.

Train a RandomForestClassifier.

Save model.pkl, scaler.pkl, and config.pkl inside api/.

4. Run the Flask API locally
bash
python app.py
# or
# gunicorn --bind 0.0.0.0:5000 app:app
API endpoints:

GET /health → status of the API and model.

POST /predict → accepts JSON with features: [30 numbers], returns fraud prediction and probability.

Example request:

json
POST /predict
{
  "features": [0.0, -1.2, 0.3, ..., 100.0]
}
💻 Frontend (React)
1. Install frontend dependencies
bash
cd ../frontend
npm install
2. Start the React development server
bash
npm start
React app: http://localhost:3000

Flask API: http://localhost:5000

In App.js, the frontend sends a POST request to:

javascript
await axios.post('http://127.0.0.1:5000/predict', { features });
Change this URL to your deployed backend URL when you deploy to Vercel.

UI Behavior
Shows labeled fields: Time, V1, V2, V3, V4, Amount.

Internally builds a 30-length feature array (remaining PCA features set to 0) to match the model’s input.

Displays:

Fraud / Safe status

Fraud probability

Model confidence

☁️ Deployment (Vercel)
Push this repo to GitHub (without venv, node_modules, or creditcard.csv).

Connect the repo to Vercel.

Vercel will:

Build the React app from frontend/.

Use api/app.py as a Python serverless function (via vercel.json).

You may need to:

Upload model.pkl and scaler.pkl with the code, or

Retrain / load them another way in the deployed environment.

🧾 .gitignore (Important)
Make sure your .gitignore includes at least:

text
venv/
node_modules/
creditcard.csv
*.pkl
__pycache__/
.env
This keeps your repo lightweight and avoids pushing large or generated files.

✅ Future Improvements
Use SMOTE or advanced methods for imbalance handling.

Add ROC / PR curves and metrics dashboard.

Use user authentication for secure API access.

Containerize with Docker.

Store models in cloud storage or model registry.

🙌 Credits
Dataset: “Credit Card Fraud Detection” – Kaggle.

Backend: Flask, scikit-learn, pandas.

Frontend: React, Axios.

text
