import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import MainPage from './components/MainPage';
import EpisodeDetails from './components/EpisodeDetails';

function App() {
  return (
    <div className='App'>
      <Router>
        <Routes>
          <Route path='/' element={<MainPage />} />
          <Route path='/episode/:episode_id' element={<EpisodeDetails />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;