import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import MentorDashboard from './components/MentorDashboard';
import AdminDashboard from './components/AdminDashboard';
import FyeCoordinatorDashboard from './components/FyeCoordinator';

const App = () => (
  <Router>
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/mentor" element={<MentorDashboard />} />
      <Route path="/admin" element={<AdminDashboard />} />
      <Route path="/fye_coordinator" element={<FyeCoordinatorDashboard />} />
    </Routes>
  </Router>
);

export default App;
