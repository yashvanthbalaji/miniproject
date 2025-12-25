// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyD3sd4wJ0NNZkNY-5bqk0EMagKXtdvLyDw",
  authDomain: "cardiac-attack-prediction-dl.firebaseapp.com",
  projectId: "cardiac-attack-prediction-dl",
  storageBucket: "cardiac-attack-prediction-dl.firebasestorage.app",
  messagingSenderId: "176083381660",
  appId: "1:176083381660:web:362cea556fb1199ae9ec59",
  measurementId: "G-JKWSZEJMM0"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Export Auth and Firestore

export const auth = getAuth(app);
export const db = getFirestore(app);
export default app;
