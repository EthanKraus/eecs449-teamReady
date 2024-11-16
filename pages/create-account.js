import { useState } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';

export default function CreateAccount() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const router = useRouter();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const url = 'http://127.0.0.1:5000/create';

        try {
            const response = await axios.post(
                url,
                { email, password }, // JSON payload
                { headers: { 'Content-Type': 'application/json' } } // Specify JSON format
            );

            if (response.status === 201) {
                alert('Account created successfully!');
                router.push('/login'); // Redirect to login page after successful account creation
            } else {
                alert('Failed to create account.');
            }
        } catch (error) {
            console.error('Error during account creation:', error);
            alert('Error during account creation.');
        }
    };

    return (
        <div className="create-account-container">
            <div className="create-account-box">
                <h2 className="title">Create an account</h2>
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
                        Create Account
                    </button>
                </form>
            </div>
        </div>
    );
}