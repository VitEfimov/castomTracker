import React from 'react';
import './AISearchResults.css';

const AISearchResults = ({ results, onCalculate }) => {
    if (!results || results.length === 0) return null;

    return (
        <div className="ai-results-container">
            <h3>Artificial intelligence recommends {results.length} possible codes:</h3>
            <table className="ai-results-table">
                <thead>
                    <tr>
                        <th>HTS Code</th>
                        <th>Probability</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
                    {results.map((item, index) => (
                        <tr key={item._id || index}>
                            <td className="code-cell">
                                <a href="#" className="hts-link">{item.hts_code}</a>
                                <div className="action-icons">
                                    <span title="Copy">📄</span>
                                    <span title="Calculate Duty" onClick={() => onCalculate && onCalculate(item)} style={{ cursor: 'pointer' }}>🧮</span>
                                </div>
                            </td>
                            <td className="prob-cell">
                                <div className="prob-wrapper">
                                    <div
                                        className="prob-bar"
                                        style={{ width: item.probability, backgroundColor: getProbColor(item.probability) }}
                                    ></div>
                                    <span className="prob-text">{item.probability}</span>
                                </div>
                            </td>
                            <td className="desc-cell">{item.full_name}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

// Helper for color coding probabilities
const getProbColor = (probStr) => {
    const prob = parseFloat(probStr);
    if (prob > 70) return '#4caf50'; // Green
    if (prob > 40) return '#ff9800'; // Orange
    return '#f44336'; // Red
};

export default AISearchResults;
