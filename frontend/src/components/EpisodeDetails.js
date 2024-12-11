import React, { useEffect, useState } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "@fortawesome/fontawesome-free/css/all.min.css";
import LoadingOverlay from "./LoadingOverlay";

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


    const handleBackClick = () => {
        navigate('/', { state: { results: location.state?.results, currentPage: location.state?.currentPage } });
    };

    const formatDate = (dateString) => {
        const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
        const date = new Date(dateString);
        return date.toLocaleDateString('en-GB', options);
    };

    // If the episode is not loaded yet, display a loading overlay
    if (!episode) {
        return <LoadingOverlay />;
    }

    // If the episode is loaded, display the episode details
    return (
        <div className="d-flex justify-content-center align-items-start" style={{ minHeight: '100vh', padding: '20px' }}>
            <div className="card" style={{ width: '90%' }}>
                <div className='card-body'>
                    <div className="d-flex justify-content-start">
                        <i className="fas fa-arrow-left" style={{ cursor: 'pointer' }} onClick={handleBackClick}></i>
                    </div>
                    <h3 className="card-title detail-title">{episode.Title}</h3>
                    <h5 className="card-subtitle mb-2 text-muted detail-subtitle">Episode {episode.Episode}</h5>
                    <div className="card-divider"></div>
                    <div className="extra-info" style={{ textAlign: 'left' }}>
                        <p><strong>Season:</strong> {episode.Season}</p>
                        <p><strong>Saga:</strong> {episode.Saga}</p>
                        <p><strong>Arc:</strong> {episode.Arc}</p>
                        <p><strong>Opening:</strong> {episode.Opening}</p>
                        <p><strong>Air Date:</strong> {formatDate(episode.airdate)}</p>
                    </div>
                    <div className="card-divider"></div>
                    <div className="episode-summary-title">
                        <h3>Episode Summary</h3>
                    </div>
                    <div className="episode-summary-text">
                        <p className="card-text">
                            {episode.Summary}
                        </p>
                    </div>
                    <div className="card-divider"></div>
                    <div className="anime-notes">
                        <p><strong>Anime Notes:</strong> {episode.anime_notes}</p>
                    </div>
                </div>
            </div>
        </div>
    );

}

export default EpisodeDetails;