# ❤️ Cardiac Attack Risk Prediction by Deep learning

A **production‑ready full‑stack mini project** that predicts **cardiac attack risk** using patient vitals and lifestyle factors. The system is powered by **Deep Learning**, secured with **Firebase Authentication**, and deployed **online** for real‑world use.

> 🚀 **Live Backend**: [https://cardiac-backend-xe0p.onrender.com](https://cardiac-backend-xe0p.onrender.com)

---

## 🔍 Project Overview

This application allows users to **sign up, log in, and predict heart attack risk** using a trained neural network model. Predictions are returned instantly through a FastAPI backend. The project is designed for **college mini‑projects**, **ML demonstrations**, and **full‑stack learning**.

---

## ✨ Key Features

### 🧠 Deep Learning Prediction

* Multi‑Layer Perceptron (MLP) Neural Network
* Trained on **UCI**, **synthetic**, and **lifestyle** datasets
* Returns **probability‑based cardiac risk score**

### 🔐 Secure Authentication

* Firebase Authentication (Signup / Login)
* JWT‑protected API routes
* Only authenticated users can access predictions

### ⚡ Fast & Interactive

* FastAPI backend with async endpoints
* React frontend with **Dark Mode** and responsive UI
* Real‑time predictions (no page reloads)

### ☁️ Cloud Deployment

* Backend hosted on **Render**
* Frontend deployable via **Firebase Hosting**
* Firebase Admin SDK for secure server‑side access

---

## 🏗️ Tech Stack

| Layer    | Technology                            |
| -------- | ------------------------------------- |
| Frontend | React, Vite, Tailwind CSS             |
| Backend  | FastAPI, Uvicorn                      |
| ML       | Scikit‑Learn (MLPClassifier)          |
| Auth     | Firebase Authentication               |
| Database | SQLite / Firestore                    |
| Hosting  | Render (Backend), Firebase (Frontend) |

---

## 📂 Project Structure

```
cardiac-prediction/
│
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── auth/                # Authentication routes & utils
│   ├── profile_routes.py    # Protected user APIs
│   ├── database.py          # Firebase / DB initialization
│   ├── models/              # Trained ML models (.pkl)
│   └── requirements.txt
│
├── client/
│   ├── src/
│   │   ├── components/      # Login, Signup, Predictor UI
│   │   ├── context/         # Auth Context
│   │   └── pages/
│   └── package.json
│
├── train_model.py           # Model training
├── generate_data.py         # Dataset generation
├── cardiac.db               # Local SQLite DB
└── README.md
```

---

## ▶️ Local Development

### 1️⃣ Backend Setup

```bash
pip install -r backend/requirements.txt
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs at:

```
http://localhost:8000
```

---

### 2️⃣ Frontend Setup

```bash
cd client
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

## 🌐 Production Deployment

### Backend (Render)

* Build Command:

```bash
pip install -r backend/requirements.txt
```

* Start Command:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

* Environment Variable:

```
FIREBASE_CREDENTIALS=<Firebase service account JSON>
```

---

### Frontend (Firebase Hosting)

```bash
npm run build
firebase deploy
```

Add deployed frontend domain to:

```
Firebase Console → Authentication → Authorized Domains
```

---

## 🔐 Authentication Flow

1. User signs up or logs in
2. Firebase issues JWT
3. JWT sent in API requests
4. Backend verifies token
5. Prediction endpoint unlocked

---


---

## ⭐ Future Improvements

* Doctor/Admin dashboard
* Email & SMS alerts
* Model retraining pipeline
* Improved risk explainability

---

> ⚠️ **Disclaimer**: This project is for educational purposes only and should not be used for real medical diagnosis.
