import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  // Existing ticket dashboard state
  const [tickets, setTickets] = useState([]);
  const [page, setPage] = useState(1);
  const [size] = useState(10);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // AI similarity-search state
  const [searchText, setSearchText] = useState('');
  const [similarTickets, setSimilarTickets] = useState([]);
  const [searchLoading, setSearchLoading] = useState(false);
  const [searchError, setSearchError] = useState('');
  const [hasSearched, setHasSearched] = useState(false);

  // Fetch paginated tickets
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

  // Search for similar historical tickets
  const handleSimilarSearch = async (event) => {
    event.preventDefault();

    const query = searchText.trim();

    if (!query) {
      setSearchError('Please enter a support issue to search.');
      setSimilarTickets([]);
      setHasSearched(false);
      return;
    }

    setSearchLoading(true);
    setSearchError('');
    setSimilarTickets([]);
    setHasSearched(false);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/similar?text=${encodeURIComponent(query)}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === 'string'
            ? data.detail
            : 'Failed to search similar tickets.'
        );
      }

      setSimilarTickets(data.results || []);
      setHasSearched(true);
    } catch (err) {
      setSearchError(
        `${err.message}. Please check that the backend is running.`
      );
    } finally {
      setSearchLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>Support Tickets</h1>
          <p>Aanchal Boutique — Customer Support Dashboard</p>
        </div>
      </header>

      <main className="main-content">

        {/* AI Similarity Search */}
        <section className="search-section">
          <h2>AI Similar Ticket Search</h2>

          <p className="search-description">
            Enter a customer issue to find the three most similar
            past support tickets using AI.
          </p>

          <form onSubmit={handleSimilarSearch} className="search-form">
            <input
              type="text"
              value={searchText}
              onChange={(event) => setSearchText(event.target.value)}
              placeholder="Example: I need to exchange my dress for a larger size"
              maxLength={1000}
              aria-label="Search for similar support tickets"
            />

            <button type="submit" disabled={searchLoading}>
              {searchLoading ? 'Searching...' : 'Find Similar Tickets'}
            </button>
          </form>

          {searchError && (
            <p className="error">{searchError}</p>
          )}

          {searchLoading && (
            <p className="loading-message">
              AI is searching past support tickets...
            </p>
          )}

          {hasSearched && !searchLoading && (
            <div className="search-results">
              <h3>Similar Past Tickets</h3>

              {similarTickets.length === 0 ? (
                <p>No similar tickets were found.</p>
              ) : (
                <div className="similar-ticket-list">
                  {similarTickets.map((ticket) => (
                    <article
                      className="similar-ticket-card"
                      key={ticket.id}
                    >
                      <div className="similar-ticket-heading">
                        <h4>{ticket.subject}</h4>

                        <span className="ticket-id">
                          Ticket #{ticket.id}
                        </span>
                      </div>

                      <p className="similar-ticket-customer">
                        Customer: {ticket.customer_name}
                      </p>

                      <p className="similar-ticket-body">
                        {ticket.body}
                      </p>

                      <div className="similarity-information">
                        <span>Similarity score</span>

                        <strong>
                          {(
                            ticket.similarity_score * 100
                          ).toFixed(2)}%
                        </strong>
                      </div>
                    </article>
                  ))}
                </div>
              )}
            </div>
          )}
        </section>

        {/* Existing Ticket Dashboard */}
        <section className="tickets-section">
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
                          {new Date(
                            ticket.date
                          ).toLocaleDateString()}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="pagination">
                <button
                  onClick={() =>
                    setPage((current) => current - 1)
                  }
                  disabled={page <= 1}
                >
                  Previous
                </button>

                <span>
                  Page {page} of {totalPages}
                </span>

                <button
                  onClick={() =>
                    setPage((current) => current + 1)
                  }
                  disabled={page >= totalPages}
                >
                  Next
                </button>
              </div>
            </>
          )}
        </section>

      </main>
    </div>
  );
}

export default App;