/**
 * History Component
 *
 * Displays list of last 5 uploaded datasets
 * Each item shows timestamp, total count, and download button
 */
import React from "react";

function History({ history, onItemClick, onDownloadReport }) {
  if (!history || history.length === 0) {
    return (
      <div className="card">
        <h2>Upload History</h2>
        <p style={{ color: "#999", fontSize: "0.9rem" }}>No uploads yet</p>
      </div>
    );
  }

  /**
   * Format timestamp for display
   */
  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  /**
   * Handle download button click
   * Prevents the click from bubbling to parent (which would select the item)
   */
  const handleDownload = (e, id) => {
    e.stopPropagation();
    onDownloadReport(id);
  };

  return (
    <div className="card">
      <h2>Upload History</h2>
      <ul className="history-list">
        {history.map((item) => (
          <li
            key={item.id}
            className="history-item"
            onClick={() => onItemClick(item)}
          >
            <div className="date">{formatDate(item.uploaded_at)}</div>
            <div className="stats">{item.total_count} equipment records</div>
            <div className="actions">
              <button
                className="download-btn"
                onClick={(e) => handleDownload(e, item.id)}
              >
                Download PDF
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default History;
