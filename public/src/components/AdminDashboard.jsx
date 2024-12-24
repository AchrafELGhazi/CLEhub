import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from '../Navbar';

const AdminDashboard = () => {
  const [mentoringSessions, setMentoringSessions] = useState([]);

  useEffect(() => {
    const fetchMentoringSessions = async () => {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8000/admin/mentoring_sessions', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setMentoringSessions(response.data);
    };

    fetchMentoringSessions();
  }, []);

  return (
    <div>
      <Navbar />
      <h2>Admin Dashboard</h2>
      <h3>Mentoring Sessions:</h3>
      <ul>
        {mentoringSessions.map((session) => (
          <li key={session.session_id}>
            {session.title} - {session.deadline}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AdminDashboard;
