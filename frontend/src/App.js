import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import WelcomePageComponent from './components/welcomepage/WelcomePageComponent';

function App() {
  return (
    <div className='App'>
      <header className='App-header'>
        <WelcomePageComponent />
      </header>
    </div>
  );
}

export default App;