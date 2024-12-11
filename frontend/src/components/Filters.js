import React, { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";

function Filters({ initialFilters, onFiltersChange }) {
    const [selectedArcs, setSelectedArcs] = useState(initialFilters.arcs || []);
    const [selectedSagas, setSelectedSagas] = useState(initialFilters.sagas || []);
    const [uniqueArcs, setUniqueArcs] = useState([]);
    const [uniqueSagas, setUniqueSagas] = useState([]);

    useEffect(() => {
        setSelectedArcs(initialFilters.arcs || []);
        setSelectedSagas(initialFilters.sagas || []);
    }, [initialFilters]);

    useEffect(() => {
        const fetchUniqueValues = async () => {
            try {
                const response = await fetch('http://localhost:8000/get-unique-values/');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setUniqueArcs(data.arcs);
                setUniqueSagas(data.sagas);
            } catch (error) {
                console.error('Error fetching unique values:', error);
            }
        }
        fetchUniqueValues();
    }, []);

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
        <div className="filters-container">
            <div className="form-group">
                <label htmlFor="saga" className="section-title">Select Saga</label>
                {uniqueSagas.map((saga) => (
                    <div className="form-check" key={saga}>
                        <input
                            className="form-check-input"
                            type="checkbox"
                            value={saga}
                            id={saga}
                            onChange={handleSagaChange}
                            checked={selectedSagas.includes(saga)}
                        />
                        <label className="form-check-label" htmlFor={saga}>{saga}</label>
                    </div>
                ))}
            </div>
            <div className="form-group">
                <label htmlFor="arc" className="section-title">Select Arc</label>
                {uniqueArcs.map((arc) => (
                    <div className="form-check" key={arc}>
                        <input
                            className="form-check-input"
                            type="checkbox"
                            value={arc}
                            id={arc}
                            onChange={handleArcChange}
                            checked={selectedArcs.includes(arc)}
                        />
                        <label className="form-check-label" htmlFor={arc}>{arc}</label>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Filters;