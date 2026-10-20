import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [tickets, setTickets] = useState([]);
  const [page, setPage] = useState(1);
  const [size] = useState(10);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchTickets = async () => {
      setLoading(true);
      setError('');

      try {
        const response = await fetch(
          `http://127.0.0.1:8000/tickets?page=${page}&size=${size}`
        );

        if (!response.ok) {
          throw new Error('Failed to fetch tickets');
        }

        const data = await response.json();

        if (!Array.isArray(data.tickets)) {
          throw new Error('Invalid ticket data received from the API');
        }

        setTickets(data.tickets);
        setTotal(data.total);
        setTotalPages(data.total_pages);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchTickets();
  }, [page, size]);

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

        <p>Total tickets: {total}</p>

        {loading && <p>Loading tickets...</p>}

        {error && <p className="error">{error}</p>}

        {!loading && !error && (
          <>
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Customer</th>
                    <th>Subject</th>
                    <th>Message</th>
                    <th>Date</th>
                  </tr>
                </thead>

                <tbody>
                  {tickets.map((ticket) => (
                    <tr key={ticket.id}>
                      <td>{ticket.id}</td>
                      <td>{ticket.customer_name}</td>
                      <td>{ticket.subject}</td>
                      <td>
                        {ticket.body.length > 100
                          ? `${ticket.body.slice(0, 100)}...`
                          : ticket.body}
                      </td>
                      <td>
                        {new Date(ticket.date).toLocaleDateString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="pagination">
              <button
                onClick={() => setPage((current) => current - 1)}
                disabled={page <= 1}
              >
                Previous
              </button>

              <span>
                Page {page} of {totalPages}
              </span>

              <button
                onClick={() => setPage((current) => current + 1)}
                disabled={page >= totalPages}
              >
                Next
              </button>
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;