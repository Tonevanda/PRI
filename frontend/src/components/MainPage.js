import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import QueryResult from './QueryResult.js';

function MainPage() {
    const [inputValue, setInputValue] = useState('');
    const [results, setResults] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const resultsPerPage = 5;

    const handleInputChange = (event) => {
        setInputValue(event.target.value);
    };

    const handleSearch = async (event) => {
        event.preventDefault();

        try {
            const response = await fetch(`http://localhost:8000/search?query=${inputValue}`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                throw new TypeError("Expected JSON response");
            }
            const data = await response.json();
            setResults(data);
            setCurrentPage(1); // Reset to the first page on new search
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    };

    const handleReset = () => {
        setInputValue('');
        setResults([]);
        setCurrentPage(1);
    };

    const handlePageChange = (pageNumber) => {
        setCurrentPage(pageNumber);
    };

    // Calculate the results to display on the current page
    const indexOfLastResult = currentPage * resultsPerPage;
    const indexOfFirstResult = indexOfLastResult - resultsPerPage;
    const currentResults = results.slice(indexOfFirstResult, indexOfLastResult);

    // Calculate the total number of pages
    const totalPages = Math.ceil(results.length / resultsPerPage);

    return (
        <div className={`welcome-page ${results.length === 0 ? 'initial' : ''}`}>
            <div className='mb-5'>
                <h1 onClick={handleReset} className='display-1' style={{ cursor: 'pointer' }}>One Search</h1>
            </div>
            <div className='mb-3 w-50'>
                <form onSubmit={handleSearch} className="w-100">
                    <div className="input-group mb-2 mx-auto">
                        <input
                            type="text"
                            value={inputValue}
                            onChange={handleInputChange}
                            placeholder="Type something..."
                            className="form-control rounded-pill"
                        />
                        <span className="input-icon">
                            <i className="fas fa-search"></i>
                        </span>
                    </div>
                </form>
            </div>

            {/* Prints the results received from the server */}
            <div className="query-list">
                {currentResults.map((result, index) => (
                    <QueryResult key={index} query={result} />
                ))}
            </div>

            {/* Pagination controls */}
            <div className='pagination-controls mt-3'>
                {Array.from({ length: totalPages }, (_, index) => (
                    <button
                        key={index}
                        onClick={() => handlePageChange(index + 1)}
                        className={`btn ${currentPage === index + 1 ? 'btn-primary' : 'btn-secondary'}`}
                        style={{ marginLeft: '5px' }} // Add inline style for margin
                    >
                        {index + 1}
                    </button>
                ))}
            </div>
        </div>
    );
}

export default MainPage;