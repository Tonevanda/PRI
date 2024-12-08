import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";

function Filters() {
    return (
        <div className="filters">
            <div className="form-group">
                <label htmlFor="season">Select Arc</label>
                <select className="form-control" id="season">
                    <option value="1">Romance Dawn</option>
                    <option value="2">Orange Town</option>
                    <option value="3">Syrup Village</option>
                </select>
            </div>
            <div className="form-group">
                <label htmlFor="episode">Select Saga</label>
                <select className="form-control" id="episode">
                    <option value="1">East Blue</option>
                    <option value="2">Alabasta</option>
                    <option value="3">Sky Island</option>
                </select>
            </div>
        </div>
    );
}

export default Filters;