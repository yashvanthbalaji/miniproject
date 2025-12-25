import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link } from 'react-router-dom';
import '../index.css';

const ForgotPassword = () => {
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { resetPassword } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            setMessage('');
            setError('');
            setLoading(true);
            await resetPassword(email);
            setMessage('Check your inbox for further instructions');
        } catch (err) {
            setError('Failed to reset password. ' + err.message);
        }
        setLoading(false);
    };

    return (
        <div className="container" style={{ maxWidth: '400px' }}>
            <header>
                <h2>Password Reset</h2>
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
                {message && <div className="success-message" style={{ color: 'green', marginBottom: '1rem' }}>{message}</div>}
                {error && <div className="error-message">{error}</div>}

                <button disabled={loading} type="submit" className="predict-btn">
                    Reset Password
                </button>

                <p style={{ textAlign: 'center', marginTop: '1rem' }}>
                    <Link to="/login" style={{ color: '#e94560' }}>Login</Link>
                </p>
            </form>
        </div>
    );
};

export default ForgotPassword;
