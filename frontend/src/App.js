import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import QueryComponent from './query/QueryComponent'; // Import the QueryComponent

function App() {
  const [inputValue, setInputValue] = useState('');
  const [results, setResults] = useState([]);

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSearch = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch(`http://localhost:8000/search?query=${inputValue}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        throw new TypeError("Expected JSON response");
      }
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="container mt-3">
          <div className="row justify-content-center">
            <div className="col-md-8 mr-2">
              <form onSubmit={handleSearch}>
                <div className="input-group mb-2">
                  <input
                    type="text"
                    value={inputValue}
                    onChange={handleInputChange}
                    placeholder="Type something..."
                    className="form-control"
                  />
                  <div className="input-group-append">
                    <button type="submit" className="btn btn-primary ml-2">Search</button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
        {/* Prints the results received from the server */}
        <div className="query-list">
          {results.map((result, index) => (
            <QueryComponent key={index} query={result} />
          ))}
        </div>
      </header>
    </div>
  );
}

export default App;