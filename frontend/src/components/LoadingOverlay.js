import React from "react";

function LoadingOverlay() {
    return (
        <div className="loading-overlay">
            <div className="spinner-border text-primary" role="status">
                <span className="sr-only">Loading...</span>
            </div>
            <div className="loading-text">Loading Episode Details...</div>
        </div>
    );
}

export default LoadingOverlay;