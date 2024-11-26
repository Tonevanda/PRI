import React, { useState } from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [inputValue, setInputValue] = useState('');
  const [results, setResults] = useState([]);

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  }

  /*
  const handleSearch = async () => {
    const response = await fetch(`http://localhost:3000/search?query=${inputValue}`);
    const data = await response.json();
    setResults(data);
  }*/

  const handleSearch = (event) => {
    // Simulate fetching 10 results based on the input value
    event.preventDefault();
    const fetchedResults = Array.from({ length: 10 }, (_, index) => `${inputValue} result ${index + 1}`);
    setResults(fetchedResults);
  };

  return (
    <div className="App">
      <header className="App-header">
        <form onSubmit={handleSearch}>
          <input
            type="text"
            value={inputValue}
            onChange={handleInputChange}
            placeholder="Type something..."
            className='form-control mb-2'
          />
          <button type='submit' className='btn btn-primary mb-2'>Search</button>
        </form>
        <ul className='list-group'>
          {results.map((result, index) => (
            <li key={index} className='list-group-item'>{result}</li>
          ))}
        </ul>
      </header>
    </div>
  );
}

export default App;
