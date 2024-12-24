import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from '../Navbar';

const MentorDashboard = () => {
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    const fetchSessions = async () => {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8000/mentor/sessions', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setSessions(response.data);
    };

    fetchSessions();
  }, []);

  return (
    <div>
      <Navbar />
      <h2>Mentor Dashboard</h2>
      <h3>Your Mentoring Sessions:</h3>
      <ul>
        {sessions.map((session) => (
          <li key={session.session_id}>
            {session.title} - {session.deadline}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MentorDashboard;
