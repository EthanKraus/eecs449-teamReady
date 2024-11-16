import { useState } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';

export default function Login({ onLogin }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isLogin, setIsLogin] = useState(true);
<<<<<<< HEAD:src/app/login.js
    const [message, setMessage] = useState('');
    const [error, setError] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!username || !password) {
            setMessage('All fields are required.');
            setError(true);
            return;
        }

=======
    const router = useRouter();

    const handleSubmit = async (e) => {
        e.preventDefault();
>>>>>>> 4b6fb984af7abeee3b5805a45739397a4be9051e:pages/login.js
        const url = isLogin ? 'http://127.0.0.1:5000/login' : 'http://127.0.0.1:5000/create';
        const operation = isLogin ? 'login' : 'create account';

        try {
            const response = await axios.post(
                url,
                { username, password }, // JSON payload
                {
                    headers: { 'Content-Type': 'application/json' },
                    withCredentials: true,
                } // Specify JSON format
            );

            if (response.status === 200 || response.status === 201) {
<<<<<<< HEAD:src/app/login.js
                setMessage(response.data.message);
                setError(false);
                if (isLogin) onLogin();
                else setIsLogin(true);
            }
        } catch (error) {
            const errorMessage = error.response?.data?.error || `An error occurred while trying to ${operation}.`;
            setMessage(errorMessage);
            setError(true);
=======
                onLogin();
                if (isLogin) {
                    router.push('/page'); // Navigate to the Page component after successful login
                } else {
                    alert('Account created successfully! Please log in.');
                    setIsLogin(true);
                }
            } else {
                alert(`Failed to ${operation}.`);
            }
        } catch (error) {
            console.error(`Error during ${operation}:`, error);
            alert(`Error during ${operation}.`);
>>>>>>> 4b6fb984af7abeee3b5805a45739397a4be9051e:pages/login.js
        }
    };

    return (
        <div className="login-container">
            <div className="login-box">
<<<<<<< HEAD:src/app/login.js
                
                    {isLogin ? 
                        <h2 className="title">Log In</h2>
                        :
                        <h2 className="title">Create an account</h2>
                    }
                {message && (
                    <div className={`message ${error ? 'error' : 'success'}`}>
                        {message}
                    </div>
                )}
=======
                {isLogin ? 
                    <h2 className="title">Log In</h2>
                    :
                    <h2 className="title">Create an account</h2>
                }
>>>>>>> 4b6fb984af7abeee3b5805a45739397a4be9051e:pages/login.js
                <form onSubmit={handleSubmit} className="form">
                    <div className="input-group">
                        <label className="label">Username</label>
                        <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="input"
                            placeholder="Enter your username"
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