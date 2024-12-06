import React from "react";

function Pagination({ totalPages, currentPage, handlePageChange }) {
    return (
        <div className='pagination-controls mt-3'>
            {Array.from({ length: totalPages }, (_, index) => (
                <button
                    key={index}
                    onClick={() => handlePageChange(index + 1)}
                    className={`btn ${currentPage === index + 1 ? 'btn-primary' : 'btn-secondary'}`}
                    style={{ marginLeft: '5px' }}>
                    {index + 1}
                </button>
            ))}
        </div>
    )
}

export default Pagination;