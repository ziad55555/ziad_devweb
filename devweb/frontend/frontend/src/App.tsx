import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import Home from './components/Home';
import Profile from './components/Profile';
import PostEditor from './components/PostEditor';

const App: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userId, setUserId] = useState<number | null>(null);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home isLoggedIn={isLoggedIn} userId={userId} />} />
        <Route path="/login" element={<Login setIsLoggedIn={setIsLoggedIn} setUserId={setUserId} />} />
        <Route path="/profile" element={<Profile userId={userId} />} />
        <Route path="/editor" element={<PostEditor userId={userId} />} />
      </Routes>
    </Router>
  );
};

export default App;
