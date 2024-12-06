import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

function SearchBar({ inputValue, handleInputChange, handleSearch }) {
    return (
        <div className='mb-3 w-50'>
            <form onSubmit={handleSearch} className="w-100">
                <div className="input-group mb-2 mx-auto">
                    <input
                        type="text"
                        value={inputValue}
                        onChange={handleInputChange}
                        className="form-control"
                    />
                    <span className="input-icon">
                        <i className="fas fa-search"></i>
                    </span>
                </div>
            </form>
        </div>
    );
};

export default SearchBar;