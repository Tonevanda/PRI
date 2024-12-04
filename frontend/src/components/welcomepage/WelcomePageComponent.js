import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import QueryComponent from '../query/QueryComponent.js';

function WelcomePageComponent() {

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
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    };

    const handlePageChange = (page) => {
        setCurrentPage(page);
    }

    const handleReset = () => {
        setInputValue('');
        setResults([]);
        setCurrentPage(1);
    };

    // Calculate the results to display on the current page
    const indexOfLastResult = currentPage * resultsPerPage;
    const indexOfFirstResult = indexOfLastResult - resultsPerPage;
    const currentResults = results.slice(indexOfFirstResult, indexOfLastResult);

    // Calculate the total number of pages
    const totalPages = Math.ceil(results.length / resultsPerPage);

    return (
        <div className="welcome-page container mt-3">
            <div className='row justify-content-center mb-5'>
                <h1 onClick={handleReset} className='display-1' style={{ cursor: 'pointer' }}>One Search</h1>
            </div>
            <div className='row justify-content-center mb-3'>
                <div id="searchform-div" className="col-md-8 mr-2">
                    <form onSubmit={handleSearch}>
                        <div className="input-group mb-2">
                            <input
                                type="text"
                                value={inputValue}
                                onChange={handleInputChange}
                                placeholder="Type something..."
                                className="form-control rounded-pill"
                            />
                        </div>
                    </form>
                </div>
            </div>

            {/* Prints the results received from the server */}
            <div className="query-list">
                {currentResults.map((result, index) => (
                    <QueryComponent key={index} query={result} />
                ))}
            </div>

            {/* Pagination controls */}
            <div className='pagination-controls'>
                {Array.from({ length: totalPages }, (_, index) => (
                    <button
                        key={index}
                        onClick={() => handlePageChange(index + 1)}
                        className={`btn ${currentPage === index + 1 ? 'btn-primary' : 'btn-secondary'} ml-1`}
                    >
                        {index + 1}
                    </button>
                ))}
            </div>
        </div>
    );
};

export default WelcomePageComponent;