import React, { useState, useEffect } from 'react';
import './DutyCalculator.css';

const DutyCalculator = ({ selectedItem, onClose }) => {
    const [price, setPrice] = useState(1000);
    const [currency, setCurrency] = useState('USD');

    // Basic rates
    const MPF_RATE = 0.003464; // Approx 0.3464%
    const HMF_RATE = 0.00125;  // 0.125%

    // Parse Duty from string (e.g. "2.5%" -> 0.025, "Free" -> 0)
    const getDutyRate = (rateStr) => {
        if (!rateStr || rateStr.toLowerCase().includes('free')) return 0;
        // Extract number
        const match = rateStr.match(/(\d+(\.\d+)?)%/);
        if (match) return parseFloat(match[1]) / 100;
        // Handle specific rates like "1.9c/kg"? For demo, default to 0 if complex
        return 0;
    };

    const dutyRateVal = getDutyRate(selectedItem?.duty?.rate);
    const dutyCost = price * dutyRateVal;
    const mpfCost = price * MPF_RATE;
    const hmfCost = price * HMF_RATE;
    const totalCost = dutyCost + mpfCost + hmfCost;

    return (
        <div className="calculator-overlay">
            <div className="calculator-modal">
                <button className="close-btn" onClick={onClose}>×</button>
                <h3>🇺🇸 US Customs Cost Estimator</h3>

                <div className="calc-row">
                    <label>Product:</label>
                    <div className="val">{selectedItem?.full_name?.substring(0, 50)}...</div>
                </div>
                <div className="calc-row">
                    <label>HTS Code:</label>
                    <div className="val highlight">{selectedItem?.hts_code}</div>
                </div>

                <div className="calc-inputs">
                    <div className="input-group">
                        <label>Price (FOB)</label>
                        <input
                            type="number"
                            value={price}
                            onChange={(e) => setPrice(parseFloat(e.target.value) || 0)}
                        />
                    </div>
                    <div className="input-group">
                        <label>Currency</label>
                        <select value={currency} onChange={(e) => setCurrency(e.target.value)}>
                            <option value="USD">USD</option>
                            <option value="EUR">EUR</option>
                        </select>
                    </div>
                </div>

                <div className="calc-results">
                    <h4>Estimated Costs</h4>
                    <div className="result-row">
                        <span>Customs Duty ({selectedItem?.duty?.rate})</span>
                        <span>${dutyCost.toFixed(2)}</span>
                    </div>
                    <div className="result-row">
                        <span>MPF (0.3464%)</span>
                        <span>${mpfCost.toFixed(2)}</span>
                    </div>
                    <div className="result-row">
                        <span>HMF (0.125%)</span>
                        <span>${hmfCost.toFixed(2)}</span>
                    </div>
                    <div className="result-total">
                        <span>TOTAL:</span>
                        <span>${totalCost.toFixed(2)}</span>
                    </div>
                    <p className="disclaimer">*Basic estimation. Specific duties may apply.</p>
                </div>
            </div>
        </div>
    );
};

export default DutyCalculator;
