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
        <h2>Recent Uploads</h2>
        <p style={{ color: "#999", fontSize: "0.9rem" }}>No data yet</p>
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
      <h2>Recent Uploads</h2>
      <div className="history-list">
        {history.map((item) => (
          <div
            key={item.id}
            className="history-item"
            onClick={() => onItemClick(item)}
          >
            <div className="timestamp">{formatDate(item.uploaded_at)}</div>
            <div className="count">{item.total_count} records</div>
            <button
              className="download-btn"
              onClick={(e) => handleDownload(e, item.id)}
            >
              Download Report
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default History;
