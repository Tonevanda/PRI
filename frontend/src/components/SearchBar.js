import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Filters from './Filters';

function SearchBar({ inputValue, handleInputChange, handleSearch }) {
    const [showFilters, setShowFilters] = useState(false);
    const [filters, setFilters] = useState({ arcs: [], sagas: [] });

    const handleFilterClick = () => {
        setShowFilters(!showFilters);
    }

    const handleClose = () => {
        setShowFilters(false);
    };

    const handleFiltersChange = (newFilters) => {
        setFilters(newFilters);
    }

    const handleSearchWithFilters = (event) => {
        event.preventDefault();
        const queryParams = new URLSearchParams({
            query: inputValue,
            arcs: filters.arcs.join(','),
            sagas: filters.sagas.join(',')
        }).toString();
        handleSearch(queryParams);
    }

    return (
        <div className='mb-3 w-50'>
            <form onSubmit={handleSearchWithFilters} className="w-100">
                <div className="input-group mb-2 mx-auto">
                    <span className="input-icon-left">
                        <i className="fas fa-search"></i>
                    </span>
                    <input
                        type="text"
                        value={inputValue}
                        onChange={handleInputChange}
                        className="form-control"
                    />
                    <span className="input-icon-right" onClick={handleFilterClick}>
                        <i className="fas fa-filter"></i>
                    </span>
                </div>
            </form>

            {showFilters && (
                <div className="modal show d-block" tabIndex="-1" role="dialog">
                    <div className="modal-dialog" role="document">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h5 className="modal-title">Filters</h5>
                            </div>
                            <div className="modal-body">
                                <Filters initialFilters={filters} onFiltersChange={handleFiltersChange} />
                            </div>
                            <div className="modal-footer">
                                <button type="button" className="btn btn-secondary" onClick={handleClose}>Close</button>
                            </div>
                        </div>
                    </div>
                </div>
            )}

        </div>
    );
};

export default SearchBar;