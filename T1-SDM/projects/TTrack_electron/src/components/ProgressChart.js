/**
 * ProgressChart Component
 * Visual representation of academic progress using SVG
 */
import React from 'react';

const ProgressChart = ({ percentage, size = 120, strokeWidth = 10 }) => {
  // Calculate parameters for the SVG circle
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;
  const center = size / 2;
  
  // Determine color based on completion percentage
  const getColor = (percent) => {
    if (percent < 30) return '#ef4444'; // red
    if (percent < 70) return '#f59e0b'; // amber
    return '#10b981'; // green
  };
  
  const color = getColor(percentage);
  
  return (
    <div className="progress-chart">
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        {/* Background circle */}
        <circle
          cx={center}
          cy={center}
          r={radius}
          fill="none"
          stroke="#e2e8f0"
          strokeWidth={strokeWidth}
        />
        
        {/* Progress circle */}
        <circle
          cx={center}
          cy={center}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          transform={`rotate(-90, ${center}, ${center})`}
        />
        
        {/* Percentage text */}
        <text
          x={center}
          y={center + 5}
          textAnchor="middle"
          dominantBaseline="middle"
          fontSize="1.5rem"
          fontWeight="bold"
          fill={color}
        >
          {percentage}%
        </text>
      </svg>
      <div className="progress-label" style={{ color }}>Completion</div>
    </div>
  );
};

export default ProgressChart;
