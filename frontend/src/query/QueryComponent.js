import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

const QueryComponent = ({ query }) => {
    return (
        <div className="card mb-3">
            <div className='card-body'>
                <h5 className="card-title">{query.Title}</h5>
                <h6 className="card-subtitle mb-2 text-muted">{query.Episode}</h6>
                <p className="card-text">{query.Summary}</p>
            </div>
        </div>
    );
};

export default QueryComponent;