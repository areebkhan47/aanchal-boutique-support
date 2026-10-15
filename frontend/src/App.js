import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/tickets')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to fetch tickets');
        }

        return response.json();
      })
      .then((data) => {
        setTickets(data);
        setLoading(false);
      })
      .catch((error) => {
        setError(error.message);
        setLoading(false);
      });
  }, []);

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>Support Tickets</h1>
          <p>Aanchal Boutique — Customer Support Dashboard</p>
        </div>
      </header>

      <main className="main-content">
        <h2>Customer Tickets</h2>

        {loading && <p>Loading tickets...</p>}

        {error && <p className="error">{error}</p>}

        {!loading && !error && (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Subject</th>
                  <th>Excerpt</th>
                </tr>
              </thead>

              <tbody>
                {tickets.map((ticket) => (
                  <tr key={ticket.id}>
                    <td>{ticket.id}</td>
                    <td>{ticket.subject}</td>
                    <td>{ticket.excerpt}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;