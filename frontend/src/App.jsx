import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SignIn from './authentication/SignIn';
import SignUp from './authentication/SignUp';
import LeaveBalance from './leave/LeaveBalance';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SignIn />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/leave-balance" element={<LeaveBalance />} />
      </Routes>
    </Router>
  );
}

export default App;
