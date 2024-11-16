import { useState } from 'react';
import './login.css';
import axios from 'axios';

export default function ChangePassword({ onPasswordChange }) {
    const [currentPassword, setCurrentPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [message, setMessage] = useState('');
    const [error, setError] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!currentPassword || !newPassword) {
            setMessage('All fields are required.');
            setError(true);
            return;
        }

        try {
            const response = await axios.post(
                'http://127.0.0.1:5000/change_password',
                { current_password: currentPassword, new_password: newPassword },
                {
                    headers: { 'Content-Type': 'application/json' },
                    withCredentials: true,
                }
            );

            if (response.status === 200) {
                setMessage(response.data.message);
                setError(false);
                onPasswordChange(); // Notify parent component if needed
            }
        } catch (error) {
            const errorMessage = error.response?.data?.error || 'An error occurred while changing your password.';
            setMessage(errorMessage);
            setError(true);
        }
    };

    return (
        <div className="login-container">
            <div className="login-box">
                <h2 className="title">Change Password</h2>
                {message && (
                    <div className={`message ${error ? 'error' : 'success'}`}>
                        {message}
                    </div>
                )}
                <form onSubmit={handleSubmit} className="form">
                    <div className="input-group">
                        <label className="label">Current Password</label>
                        <input
                            type="password"
                            value={currentPassword}
                            onChange={(e) => setCurrentPassword(e.target.value)}
                            className="input"
                            placeholder="Enter your current password"
                        />
                    </div>
                    <div className="input-group">
                        <label className="label">New Password</label>
                        <input
                            type="password"
                            value={newPassword}
                            onChange={(e) => setNewPassword(e.target.value)}
                            className="input"
                            placeholder="Enter your new password"
                        />
                    </div>
                    <button
                        type="submit"
                        className="submit-btn"
                    >
                        Change Password
                    </button>
                </form>
            </div>
        </div>
    );
}
