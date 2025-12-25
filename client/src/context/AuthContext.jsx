import { createContext, useContext, useEffect, useState } from "react";
import axios from "axios";
import {
    signInWithEmailAndPassword,
    createUserWithEmailAndPassword,
    onAuthStateChanged,
    signOut,
    sendPasswordResetEmail
} from "firebase/auth";
import { auth } from "../firebase";

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(null); // Add token state
    const [loading, setLoading] = useState(true);

    const signup = async (email, password) => {
        return createUserWithEmailAndPassword(auth, email, password);
    };

    const login = async (email, password) => {
        const cred = await signInWithEmailAndPassword(auth, email, password);
        const t = await cred.user.getIdToken();
        setToken(t); // Set token

        axios.defaults.headers.common["Authorization"] = `Bearer ${t}`;

        return cred;
    };

    const resetPassword = (email) => {
        return sendPasswordResetEmail(auth, email);
    };

    const logout = async () => {
        await signOut(auth);
        delete axios.defaults.headers.common["Authorization"];
        setUser(null);
        setToken(null);
    };

    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
            if (firebaseUser) {
                const t = await firebaseUser.getIdToken();
                setToken(t);
                axios.defaults.headers.common["Authorization"] = `Bearer ${t}`;
                setUser(firebaseUser);
            } else {
                delete axios.defaults.headers.common["Authorization"];
                setUser(null);
                setToken(null);
            }
            setLoading(false);
        });

        return unsubscribe;
    }, []);

    return (
        <AuthContext.Provider value={{ user, token, signup, login, logout, resetPassword, loading }}>
            {!loading && children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);