/**
 * Summary Component
 *
 * Displays computed statistics from the uploaded CSV:
 * - Total equipment count
 * - Average flowrate
 * - Average pressure
 * - Average temperature
 */
import React from "react";

function Summary({ data }) {
  if (!data) return null;

  const stats = [
    { label: "Total Count", value: data.total_count },
    { label: "Avg Flowrate", value: data.avg_flowrate?.toFixed(2) },
    { label: "Avg Pressure", value: data.avg_pressure?.toFixed(2) },
    { label: "Avg Temperature", value: data.avg_temperature?.toFixed(2) },
  ];

  return (
    <div className="card">
      <h2>Summary Statistics</h2>
      <div className="summary-grid">
        {stats.map((stat) => (
          <div key={stat.label} className="summary-item">
            <div className="label">{stat.label}</div>
            <div className="value">{stat.value}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Summary;
