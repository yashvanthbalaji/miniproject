import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';
import '../index.css';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            await login(email, password);
            navigate('/dashboard');
        } catch (err) {
            setError('Invalid credentials. Please try again.');
            console.error(err);
        }
    };

    return (
        <div className="container" style={{ maxWidth: '400px' }}>
            <header>
                <h2>Login</h2>
            </header>
            <form onSubmit={handleSubmit} className="risk-form">
                <div className="input-group">
                    <label>Email</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div className="input-group">
                    <label>Password</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                {error && <div className="error-message">{error}</div>}

                <div style={{ textAlign: 'right', marginTop: '0.5rem' }}>
                    <Link to="/forgot-password" style={{ color: '#bbb', fontSize: '0.9rem' }}>Forgot Password?</Link>
                </div>

                <button type="submit" className="predict-btn" style={{ marginTop: '1rem' }}>Login</button>

                <p style={{ textAlign: 'center', marginTop: '1rem' }}>
                    Don't have an account? <Link to="/signup" style={{ color: '#e94560' }}>Sign up</Link>
                </p>
            </form>
        </div>
    );
};

export default Login;
