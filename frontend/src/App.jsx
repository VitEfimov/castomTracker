import React, { useState, useEffect } from 'react';
import Grid from './components/Grid';
import Search from './components/Search';
import AISearchResults from './components/AISearchResults';
import HTSTree from './components/HTSTree';
import DutyCalculator from './components/DutyCalculator';
import './App.css';

function App() {
  const [rowData, setRowData] = useState([]);
  const [apiData, setApiData] = useState([]); // Store USITC API results
  const [loading, setLoading] = useState(false);
  const [currentQuery, setCurrentQuery] = useState("");
  const [selectedForCalc, setSelectedForCalc] = useState(null);
  const [activeTab, setActiveTab] = useState('local'); // 'local' or 'api'

  const API_URL = "http://localhost:8000/api";

  useEffect(() => {
    handleSearch("");
  }, []);

  const handleSearch = async (query) => {
    setLoading(true);
    setCurrentQuery(query);

    try {
      if (activeTab === 'local') {
        const response = await fetch(`${API_URL}/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        setRowData(data);
      } else {
        // Call proxy for USITC
        const response = await fetch(`${API_URL}/usitc-search?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        // USITC API returns raw list or object? check_api.py showed it returns list if successful but we need to check structure
        // check_api.py output was a bit garbled but seems to be a list of objects
        setApiData(data);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  // Refetch when tab changes if we have a query
  useEffect(() => {
    if (currentQuery) {
      handleSearch(currentQuery);
    }
  }, [activeTab]);

  const onFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/sync`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      console.log("Sync result:", data);
      alert(`Sync Complete! Processed ${data.rows} rows.`);
    } catch (error) {
      console.error("Error uploading:", error);
      alert("Error uploading file");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>US Customs Tracker</h1>
        <div className="header-actions">
          <label className="import-btn">
            Import XLSX
            <input type="file" accept=".xlsx" hidden onChange={onFileUpload} />
          </label>
          <button className="export-btn" onClick={() => alert('Export implementation pending backend connection')}>
            Export XLSX
          </button>
        </div>
      </header>

      <main className="main-content">
        <div className="tabs">
          <button
            className={`tab-btn ${activeTab === 'local' ? 'active' : ''}`}
            onClick={() => setActiveTab('local')}
          >
            Local Search
          </button>
          <button
            className={`tab-btn ${activeTab === 'api' ? 'active' : ''}`}
            onClick={() => setActiveTab('api')}
          >
            USITC API (Live)
          </button>
        </div>

        <div className="search-section">
          <Search onSearch={handleSearch} />
          <div className="similar-queries">
            {['graphic tablet', 'tablet folder', 'Apple iPad', 'Samsung Galaxy'].map(q => (
              <span key={q} className="query-chip" onClick={() => handleSearch(q)}>{q}</span>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="loading">Loading...</div>
        ) : (
          <>
            {activeTab === 'local' ? (
              // LOCAL TAB CONTENT
              <>
                {currentQuery ? (
                  <div className="results-section">
                    <AISearchResults results={rowData} onCalculate={setSelectedForCalc} />
                    <div style={{ marginTop: '2rem' }}>
                      <h4>Detailed Data View</h4>
                      <div className="grid-container" style={{ height: '400px' }}>
                        <Grid rowData={rowData} />
                      </div>
                    </div>
                  </div>
                ) : (
                  <HTSTree />
                )}
              </>
            ) : (
              // API TAB CONTENT
              // API TAB CONTENT
              <div className="results-section">
                {apiData && apiData.length > 0 ? (
                  <table className="api-results-table">
                    <thead>
                      <tr>
                        <th>HTS #</th>
                        <th>Description</th>
                        <th>Rate</th>
                      </tr>
                    </thead>
                    <tbody>
                      {apiData.slice(0, 50).map((item, idx) => (
                        <tr key={idx}>
                          <td>{item.hts_code}</td>
                          <td>{item.description}</td>
                          <td>{item.duties?.general || 'N/A'}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                ) : (
                  <div className="no-results">
                    {currentQuery ? "No results found from USITC API." : "Enter a search term to query USITC."}
                  </div>
                )}
              </div>
            )}
          </>
        )}
      </main>

      {selectedForCalc && (
        <DutyCalculator
          selectedItem={selectedForCalc}
          onClose={() => setSelectedForCalc(null)}
        />
      )}
    </div>
  );
}

export default App;
