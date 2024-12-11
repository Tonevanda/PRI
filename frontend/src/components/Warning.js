import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css';

function Warning({ handleCloseWarning }) {
    return (
        <div className="alert alert-warning" role="alert">
            No episodes found for the given query.
            <button type="button" className="btn-close" aria-label="Close" onClick={handleCloseWarning}></button>
        </div>
    );
}

export default Warning;