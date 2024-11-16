import { useState } from 'react';
import './login.css';
import axios from 'axios';

export default function Login({ onLogin }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLogin, setIsLogin] = useState(true);

    const handleSubmit = async (e) => {
        e.preventDefault();
        // add the login logic or call to backend for authentication here.
        // placeholder: assume successful login if all fields filled
        // if (email && password) {
        //     onLogin();
        // } else {
        //     alert('Please enter a email and password.');
        // }

        const url = isLogin ? 'http://127.0.0.1:5000/login' : 'http://127.0.0.1:5000/create';
        const operation = isLogin ? 'login' : 'create account';

        try {
            const response = await axios.post(
                url,
                { email, password }, // JSON payload
                { headers: { 'Content-Type': 'application/json' } } // Specify JSON format
            );

            if (response.status === 200 || response.status === 201) {
                alert(response.data.message);
                if (isLogin) onLogin();
                else setIsLogin(true);
            }
        } catch (error) {
            console.error(error);
            alert(error.response?.data?.error || `Failed to ${operation}.`);
        }
    };

    return (
        <div className="login-container">
            <div className="login-box">
                
                    {isLogin ? 
                        <h2 className="title">Log In</h2>
                        :
                        <h2 className="title">Create an account</h2>
                    }
                <form onSubmit={handleSubmit} className="form">
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
                        {isLogin ? 'Login' : 'Create Account'}
                    </button>
                    <div className="text-center">
                        {isLogin ? (
                                <button
                                    type="button"
                                    className="link-btn"
                                    onClick={() => setIsLogin(false)}
                                >
                                    New to ShopSmart? Create an account
                                </button>
                        ) : (
                                <button
                                    type="button"
                                    className="link-btn"
                                    onClick={() => setIsLogin(true)}
                                >
                                    Already have an account? Log in
                                </button>
                        )}
                    </div>
                </form>
            </div>
        </div>
    );
}
