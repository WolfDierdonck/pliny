import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import BubbleChart from './components/BubbleChart';
import Timeline from './components/Timeline';
import { ScoreTable } from './components/ScoreTable';

const App: React.FC = () => {
  return (
    <Router>
      {/* <Navbar /> */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/bubble-chart" element={<BubbleChart />} />
        <Route path="/timeline" element={<Timeline />} />
        <Route path="/ScoreTable" element={<ScoreTable />} />
      </Routes>
    </Router>
  );
};

export default App;
