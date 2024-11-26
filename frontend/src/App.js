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

  const handleSearch = async (event) => {
    event.preventDefault(); // Prevent the default form submission

    try {
      const response = await fetch(`http://localhost:3000/search?query=${inputValue}`);
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
