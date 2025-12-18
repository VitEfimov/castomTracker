import React, { useState } from 'react';

const Search = ({ onSearch }) => {
    const [query, setQuery] = useState('');

    const handleSearch = (e) => {
        e.preventDefault();
        onSearch(query);
    };

    // Optional: Search on clear
    const handleChange = (e) => {
        const val = e.target.value;
        setQuery(val);
        if (val === '') {
            onSearch('');
        }
    }

    return (
        <div className="search-container">
            <form onSubmit={handleSearch} className="search-form">
                <input
                    type="text"
                    className="search-input"
                    placeholder="Search goods (e.g. 'Laptop', 'Coffee')..."
                    value={query}
                    onChange={handleChange}
                />
                <button type="submit" className="search-button">
                    Search
                </button>
            </form>
        </div>
    );
};

export default Search;
