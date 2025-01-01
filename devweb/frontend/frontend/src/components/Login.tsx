import React, { useState } from 'react';
import { fetchUser } from '../services/api';
import { useNavigate } from 'react-router-dom';

interface LoginProps {
  setIsLoggedIn: React.Dispatch<React.SetStateAction<boolean>>;
  setUserId: React.Dispatch<React.SetStateAction<number | null>>;
}

const Login: React.FC<LoginProps> = ({ setIsLoggedIn, setUserId }) => {
  const [username, setUsername] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const user = await fetchUser(username);
      setIsLoggedIn(true);
      setUserId(user.id);
      navigate('/');
    } catch (error) {
      setErrorMessage('Utilisateur non trouvé.');
    }
  };

  return (
    <div>
      <h2>Connexion</h2>
      <input
        type="text"
        placeholder="Nom d'utilisateur"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <button onClick={handleLogin}>Se connecter</button>
      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
    </div>
  );
};

export default Login;
