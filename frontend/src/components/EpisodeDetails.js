import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

function EpisodeDetails() {
    const { episode_id } = useParams();
    const [episode, setEpisode] = useState(null);

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

    if (!episode) {
        return <div>Loading Episode Details...</div>;
    }

    return (
        <div className="card mb-3" style={{ cursor: 'pointer' }}>
            <div className='card-body'>
                <h5 className="card-title">{episode.Title}</h5>
                <h6 className="card-subtitle mb-2 text-muted">Episode {episode.Episode}</h6>
                <p className="card-text">
                    {`${episode.Summary.substring(0, 100)}...`}
                </p>
            </div>
        </div>
    );

}

export default EpisodeDetails;