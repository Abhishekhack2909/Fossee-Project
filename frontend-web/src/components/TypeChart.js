/**
 * TypeChart Component
 *
 * Displays a bar chart of equipment type distribution using Chart.js
 * Shows count of each equipment type (Pump, Valve, etc.)
 */
import React from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
);

function TypeChart({ distribution }) {
  if (!distribution || Object.keys(distribution).length === 0) {
    return null;
  }

  // Prepare data for Chart.js
  const labels = Object.keys(distribution);
  const values = Object.values(distribution);

  // Chart colors - vibrant palette
  const backgroundColors = [
    "rgba(102, 126, 234, 0.8)",
    "rgba(118, 75, 162, 0.8)",
    "rgba(40, 167, 69, 0.8)",
    "rgba(255, 193, 7, 0.8)",
    "rgba(220, 53, 69, 0.8)",
    "rgba(23, 162, 184, 0.8)",
  ];

  const data = {
    labels,
    datasets: [
      {
        label: "Count",
        data: values,
        backgroundColor: backgroundColors.slice(0, labels.length),
        borderColor: backgroundColors
          .slice(0, labels.length)
          .map((c) => c.replace("0.8", "1")),
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  return (
    <div className="card">
      <h2>Equipment Type Distribution</h2>
      <div className="chart-container">
        <Bar data={data} options={options} />
      </div>
    </div>
  );
}

export default TypeChart;
