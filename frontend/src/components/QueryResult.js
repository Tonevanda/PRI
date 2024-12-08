import React from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

function QueryResult({ query, results }) {
    const navigate = useNavigate();

    const handleClick = () => {
        navigate(`/episode/${query.Episode}`, { state: { results } });
    }

    return (
        <div className="card mb-3 query" onClick={handleClick} style={{ cursor: 'pointer' }}>
            <div className='card-body'>
                <h5 className="card-title">{query.Title}</h5>
                <h6 className="card-subtitle mb-2 text-muted">Episode {query.Episode}</h6>
                <p className="card-text">
                    {`${query.Summary.substring(0, 100)}...`}
                </p>
            </div>
        </div>
    );
};

export default QueryResult;