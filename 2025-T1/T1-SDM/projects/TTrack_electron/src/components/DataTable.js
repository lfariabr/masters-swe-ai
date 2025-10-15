/**
 * DataTable Component
 * Displays tabular data with formatting
 */
import React from 'react';

const DataTable = ({ title, data }) => {
  if (!data || !data.length) {
    return (
      <div className="box">
        <h3>{title}</h3>
        <div className="empty-state">No data uploaded yet</div>
      </div>
    );
  }

  return (
    <div className="box">
      <h3>{title}</h3>
      <div className="scroll-box">
        {Array.isArray(data) ? (
          <table className="data-table">
            <thead>
              <tr>
                {Object.keys(data[0]).map(key => (
                  <th key={key}>{key}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row, index) => (
                <tr key={index}>
                  {Object.values(row).map((value, i) => (
                    <td key={i}>{value !== null ? value.toString() : ""}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <pre>{JSON.stringify(data, null, 2)}</pre>
        )}
      </div>
    </div>
  );
};

export default DataTable;
