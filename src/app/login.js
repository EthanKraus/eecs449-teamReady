import { useState } from 'react';
import './login.css';

export default function Login({ onLogin }) {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        // add the login logic or call to backend for authentication here.
        // placeholder: assume successful login if all fields filled
        if (username && email && password) {
            onLogin();
        } else {
            alert('Please enter a username, email, and password.');
        }
    };

    return (
        <div className="login-container">
            <div className="login-box">
                <h2 className="title">Create an account</h2>
                <form onSubmit={handleSubmit} className="form">
                    <div className="input-group">
                        <label className="label">User name</label>
                        <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="input"
                            placeholder="Enter your user name"
                        />
                    </div>
                    <div className="input-group">
                        <label className="label">Email address</label>
                        <input
                            type="text"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="input"
                            placeholder="Enter your email address"
                        />
                    </div>
                    <div className="input-group">
                        <label className="label">Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="input"
                            placeholder="Enter your password"
                        />
                    </div>
                    <button
                        type="submit"
                        className="submit-btn"
                    >
                        Login
                    </button>
                    <label className="text-center">Already have an account? Log in</label>
                </form>
            </div>
        </div>
    );
}
