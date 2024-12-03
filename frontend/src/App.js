import React, { useState } from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [inputValue, setInputValue] = useState('');
  const [results, setResults] = useState([]);

  // Updates the input value as the user types
  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  }

  // Sends a GET request to the server with the search query
  const handleSearch = async (event) => {
    event.preventDefault();

    /*try{
      const response = await fetch(
        `http://localhost:8983/solr/#/episodes/query?q=*:*&q.op=AND&indent=true&useParams=params`,{
        mode: 'cors',
        headers: {
          'Access-Control-Allow-Origin':'*'
        }
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        throw new TypeError("Expected JSON response");
      }
    }catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    }*/

    try {
      const response = await fetch(`http://localhost:8000/search?query=${inputValue}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        throw new TypeError("Expected JSON response");
      }
      //console.log(response)
      const data = await response.json();
      console.log(data)
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
        {/*Prints the results received from the server*/}
        <ul className='list-group'>
          {results.map((result, index) => (
            <li key={index} className='list-group-item'>{result['Title']}</li>
          ))}
        </ul>
      </header>
    </div>
  );
}

export default App;
