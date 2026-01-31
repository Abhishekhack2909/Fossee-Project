/**
 * Main App Component
 *
 * This is the root component that brings together all features:
 * - File upload
 * - Summary display
 * - Chart visualization
 * - History list
 */
import React, { useState, useEffect } from "react";
import FileUpload from "./components/FileUpload";
import Summary from "./components/Summary";
import TypeChart from "./components/TypeChart";
import History from "./components/History";

// API base URL - Django backend
const API_BASE = "http://localhost:8000/api";

function App() {
  // State for current summary (after upload)
  const [summary, setSummary] = useState(null);

  // State for upload history
  const [history, setHistory] = useState([]);

  // Loading and error states
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  /**
   * Fetch history on component mount
   */
  useEffect(() => {
    fetchHistory();
  }, []);

  /**
   * Fetch upload history from backend
   */
  const fetchHistory = async () => {
    try {
      const response = await fetch(`${API_BASE}/history/`);
      const data = await response.json();
      setHistory(data);
    } catch (err) {
      console.error("Failed to fetch history:", err);
    }
  };

  /**
   * Handle file upload
   * Called by FileUpload component when user selects a file
   */
  const handleUpload = async (file) => {
    setLoading(true);
    setError(null);

    // Create form data for multipart upload
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_BASE}/upload/`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Upload failed");
      }

      // Update current summary
      setSummary(data);

      // Refresh history
      fetchHistory();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Handle clicking on a history item
   * Shows that dataset's summary
   */
  const handleHistoryClick = (item) => {
    setSummary(item);
  };

  /**
   * Download PDF report for a dataset
   */
  const handleDownloadReport = (id) => {
    window.open(`${API_BASE}/report/${id}/`, "_blank");
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Chemical Equipment Parameter Visualizer</h1>
      </header>

      <main className="app-main">
        {/* Left Panel: Upload and History */}
        <aside className="sidebar">
          <FileUpload onUpload={handleUpload} loading={loading} />

          {error && <div className="error-message">{error}</div>}

          <History
            history={history}
            onItemClick={handleHistoryClick}
            onDownloadReport={handleDownloadReport}
          />
        </aside>

        {/* Right Panel: Summary and Chart */}
        <section className="content">
          {summary ? (
            <>
              <Summary data={summary} />
              <TypeChart distribution={summary.type_distribution} />
            </>
          ) : (
            <div className="placeholder">
              <p>Upload a CSV file to see the analysis</p>
              <p className="hint">
                CSV must have columns: Equipment Name, Type, Flowrate, Pressure,
                Temperature
              </p>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
