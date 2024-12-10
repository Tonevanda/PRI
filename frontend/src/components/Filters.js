import React, { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";

function Filters({ initialFilters, onFiltersChange }) {
    const [selectedArcs, setSelectedArcs] = useState(initialFilters.arcs || []);
    const [selectedSagas, setSelectedSagas] = useState(initialFilters.sagas || []);

    useEffect(() => {
        setSelectedArcs(initialFilters.arcs || []);
        setSelectedSagas(initialFilters.sagas || []);
    }, [initialFilters]);

    const handleArcChange = (event) => {
        const { value, checked } = event.target;
        setSelectedArcs((prevSelectedArcs) => {
            const newSelectedArcs = checked ? [...prevSelectedArcs, value] : prevSelectedArcs.filter((arc) => arc !== value);
            onFiltersChange({ arcs: newSelectedArcs, sagas: selectedSagas });
            return newSelectedArcs;
        });
    };

    const handleSagaChange = (event) => {
        const { value, checked } = event.target;
        setSelectedSagas((prevSelectedSagas) => {
            const newSelectedSagas = checked ? [...prevSelectedSagas, value] : prevSelectedSagas.filter((saga) => saga !== value);
            onFiltersChange({ arcs: selectedArcs, sagas: newSelectedSagas });
            return newSelectedSagas;
        });
    };

    return (
        <div className="filters">
            <div className="form-group">
                <label htmlFor="arc">Select Arc</label>
                <div className="form-check">
                    <input
                        className="form-check-input"
                        type="checkbox"
                        value="Romance Dawn"
                        id="romanceDawn"
                        onChange={handleArcChange}
                        checked={selectedArcs.includes("Romance Dawn")}
                    />
                    <label className="form-check-label" htmlFor="romanceDawn">Romance Dawn</label>
                </div>
                <div className="form-check">
                    <input
                        className="form-check-input"
                        type="checkbox"
                        value="Orange Town"
                        id="orangeTown"
                        onChange={handleArcChange}
                        checked={selectedArcs.includes("Orange Town")}
                    />
                    <label className="form-check-label" htmlFor="orangeTown">Orange Town</label>
                </div>
                <div className="form-check">
                    <input
                        className="form-check-input"
                        type="checkbox"
                        value="Syrup Village"
                        id="syrupVillage"
                        onChange={handleArcChange}
                        checked={selectedArcs.includes("Syrup Village")}
                    />
                    <label className="form-check-label" htmlFor="syrupVillage">Syrup Village</label>
                </div>
            </div>
            <div className="form-group">
                <label htmlFor="saga">Select Saga</label>
                <div id="saga">
                    <div className="form-check">
                        <input
                            className="form-check-input"
                            type="checkbox"
                            value="East Blue"
                            id="eastBlue"
                            onChange={handleSagaChange}
                            checked={selectedSagas.includes("East Blue")}
                        />
                        <label className="form-check-label" htmlFor="eastBlue">East Blue</label>
                    </div>
                    <div className="form-check">
                        <input
                            className="form-check-input"
                            type="checkbox"
                            value="Alabasta"
                            id="alabasta"
                            onChange={handleSagaChange}
                            checked={selectedSagas.includes("Alabasta")}
                        />
                        <label className="form-check-label" htmlFor="alabasta">Alabasta</label>
                    </div>
                    <div className="form-check">
                        <input
                            className="form-check-input"
                            type="checkbox"
                            value="Sky Island"
                            id="skyIsland"
                            onChange={handleSagaChange}
                            checked={selectedSagas.includes("Sky Island")}
                        />
                        <label className="form-check-label" htmlFor="skyIsland">Sky Island</label>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Filters;