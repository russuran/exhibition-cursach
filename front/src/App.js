import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Exhibits from './pages/Exhibits';
import Exhibitions from './pages/Exhibitions';
import Employees from './pages/Employees';
import Tickets from './pages/Tickets';
import Restorations from './pages/Restorations';
import ExhibitionContents from './pages/ExhibitionContents';

const App = () => {
    return (
        <Router>
            <Navbar />
            <div style={{ padding: '20px' }}>
                <Routes>
                    <Route path="/exhibits" element={<Exhibits />} />
                    <Route path="/exhibitions" element={<Exhibitions />} />
                    <Route path="/employees" element={<Employees />} />
                    <Route path="/tickets" element={<Tickets />} />
                    <Route path="/restorations" element={<Restorations />} />
                    <Route path="/exhibition-contents" element={<ExhibitionContents />} />
                    <Route path="/" element={<h1>Welcome to the Museum Management System</h1>} />
                </Routes>
            </div>
        </Router>
    );
};

export default App;
