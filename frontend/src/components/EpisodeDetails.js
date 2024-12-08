import React, { useEffect, useState } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "@fortawesome/fontawesome-free/css/all.min.css";

function EpisodeDetails() {
    const { episode_id } = useParams();
    const [episode, setEpisode] = useState(null);
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        const fetchEpisode = async () => {
            try {
                const response = await fetch(`http://localhost:8000/episode/${episode_id}`);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const contentType = response.headers.get('content-type');
                if (!contentType || !contentType.includes('application/json')) {
                    throw new TypeError("Expected JSON response");
                }
                const data = await response.json();
                setEpisode(data[0]);
            }
            catch (error) {
                console.error('Error fetching episode:', error);
            }
        }
        fetchEpisode();
    },
        [episode_id]
    );

    useEffect(() => {
        if (episode) {
            document.title = `Episode ${episode.Episode} | One Search`;
        }
        else {
            document.title = 'One Search';
        }
    },
        [episode]
    );

    if (!episode) {
        return <div>Loading Episode Details...</div>;
    }

    const handleBackClick = () => {
        navigate('/', { state: { results: location.state?.results, currentPage: location.state?.currentPage } });
    };

    return (
        <div className="d-flex justify-content-center align-items-start" style={{ minHeight: '100vh', padding: '20px' }}>
            <div className="card" style={{ width: '90%' }}>
                <div className='card-body'>
                    <div className="d-flex justify-content-start">
                        <i className="fas fa-arrow-left" style={{ cursor: 'pointer' }} onClick={handleBackClick}></i>
                    </div>
                    <h5 className="card-title">{episode.Title}</h5>
                    <h6 className="card-subtitle mb-2 text-muted">Episode {episode.Episode}</h6>
                    <div className="card-divider"></div>
                    <div style={{ textAlign: 'left' }}>
                        <p className="card-text">
                            {episode.Summary}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );

}

export default EpisodeDetails;