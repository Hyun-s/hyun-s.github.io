import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Home from './pages/Home';
import CV from './pages/CV';
import Calendar from './pages/Calendar';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/cv" element={<CV />} />
            <Route path="/calendar" element={<Calendar />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;