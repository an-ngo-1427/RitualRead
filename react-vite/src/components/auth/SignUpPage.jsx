import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const SignUpPage = () => {
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        username: '',
    });
    const navigate = useNavigate();
    const [formErrors, setFormErrors] = useState([]);
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log('Form submitted:', formData);
        // Add your form submission logic here
        const newForm = new FormData();
        newForm.append('first_name', formData.first_name);
        newForm.append('last_name', formData.last_name);
        newForm.append('email', formData.email);
        newForm.append('password', formData.password);
        newForm.append('username', formData.username);
        const res = await fetch('/api/auth/signup', {
            method: 'POST',
            body: newForm,
        });
        const data = await res.json();
        if (res.ok) {
            // Redirect to lobby
            navigate('/lobby');
        } else {
            // Handle form errors
            setFormErrors(data.errors);
        }
    };

    return (
        <div className="sign-up-page">
            <h2>Sign Up</h2>
            <ul>
                {formErrors.map((error) => (
                    <li key={error}>{error}</li>
                ))}
            </ul>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="first_name">First Name:</label>
                    <input
                        type="text"
                        id="first_name"
                        name="first_name"
                        value={formData.first_name}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="last_name">Last Name:</label>
                    <input
                        type="text"
                        id="last_name"
                        name="last_name"
                        value={formData.last_name}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="email">Email:</label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="password">Password:</label>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <label htmlFor="username">Username:</label>
                    <input
                        type="text"
                        id="username"
                        name="username"
                        value={formData.username}
                        onChange={handleChange}
                        required
                    />
                </div>
                <button type="submit" isDisabled={formErrors.length}>Sign Up</button>
            </form>
        </div>
    );
};

export default SignUpPage;
