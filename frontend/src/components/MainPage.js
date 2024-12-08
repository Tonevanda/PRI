import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import QueryResult from './QueryResult.js';
import SearchBar from './SearchBar.js';
import Pagination from './Pagination.js';

function MainPage() {
    const location = useLocation();
    const [inputValue, setInputValue] = useState('');
    const [results, setResults] = useState(location.state?.results || []);
    const [currentPage, setCurrentPage] = useState(1);
    const resultsPerPage = 5;

    useEffect(() => {
        if (location.state?.results) {
            setResults(location.state.results);
        }
        if (location.state?.currentPage) {
            setCurrentPage(location.state.currentPage);
        }
    }, [location.state]);


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

            {/* Title */}
            <div className='mb-5'>
                <h1 onClick={handleReset} className='title' style={{ cursor: 'pointer' }}>One Search</h1>
            </div>

            {/* Search bar */}
            <SearchBar
                inputValue={inputValue}
                handleInputChange={handleInputChange}
                handleSearch={handleSearch}
            />

            {/* Prints the results received from the server */}
            <div className="query-list">
                {currentResults.map((result, index) => (
                    <QueryResult key={index} query={result} results={results} currentPage={currentPage} />
                ))}
            </div>

            {/* Pagination controls */}
            <Pagination
                totalPages={totalPages}
                currentPage={currentPage}
                handlePageChange={handlePageChange}
            />
        </div>
    );
}

export default MainPage;