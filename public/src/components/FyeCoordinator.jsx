import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from '../Navbar';

const FyeCoordinatorDashboard = () => {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const fetchEvents = async () => {
      const token = localStorage.getItem('token');
      const coordinatorId = localStorage.getItem('userId');
      const response = await axios.get(`http://localhost:8000/fye_coordinator/assigned_events/${coordinatorId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setEvents(response.data);
    };

    fetchEvents();
  }, []);

  return (
    <div>
      <Navbar />
      <h2>FYE Coordinator Dashboard</h2>
      <h3>Assigned Events:</h3>
      <ul>
        {events.map((event) => (
          <li key={event.event_id}>
            {event.title} - {event.date_of_event}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default FyeCoordinatorDashboard;
