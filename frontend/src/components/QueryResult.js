import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

const QueryResult = ({ query }) => {
    const [isExpanded, setIsExpanded] = useState(false);

    const handleExpand = () => {
        setIsExpanded(!isExpanded);
    }

    return (
        <div className="card mb-3" onClick={handleExpand} style={{ cursor: 'pointer' }}>
            <div className='card-body'>
                <h5 className="card-title">{query.Title}</h5>
                <h6 className="card-subtitle mb-2 text-muted">Episode {query.Episode}</h6>
                <p className="card-text">
                    {isExpanded ? <span>{query.Summary}</span> : `${query.Summary.substring(0, 100)}...`}
                </p>
            </div>
        </div>
    );
};

export default QueryResult;