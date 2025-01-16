import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import React, { useState } from "react";

function SignIn() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Prepare data as URLSearchParams
    const data = new URLSearchParams();
    data.append('username', email); // This corresponds to form_data.username
    data.append('password', password);

    try {
      const response = await axios.post('http://localhost:8000/signin', data, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      const token = response.data.access_token; // Get JWT token from response

      // Store the JWT token in localStorage
      localStorage.setItem('auth_token', token);

      // console.log('Sign-in successful');
      // console.log('Navigating to /chat');
      // localStorage.setItem("patient_email", email); // Store the email in localStorage
      // console.log(email);

      navigate('/leave-balance');

    } catch (err) {
      setError('Invalid credentials. Please try again.');
      console.error(err);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-blue-50">
      <h2 className="text-3xl font-bold text-[#4a3267] mb-6">Sign In</h2>
      <form onSubmit={handleSubmit} className="w-full max-w-md p-6 bg-white rounded-lg shadow-md">
        <div className="mb-4">
          <label className="block text-gray-700 font-medium">Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
          />
        </div>
        <div className="mb-6">
          <label className="block text-gray-700 font-medium">Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
          />
        </div>
        {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
        <button
          type="submit"
          className="w-full px-4 py-2 text-white bg-[#4a3267] rounded-lg font-medium hover:bg-[#c6bade] transition"
        >
          Sign In
        </button>
        <p className="mt-4 text-center text-gray-600">
          New here?{' '}
          <Link to="/signup" className="text-[#4a3267] font-medium hover:underline">
            Create an account
          </Link>
        </p>
      </form>
    </div>
  );
}

export default SignIn;
