import React, { useState, useEffect } from 'react';
import { fetchUserById, updateUser, User } from '../services/api';

interface ProfileProps {
  userId: number;
}

const Profile: React.FC<ProfileProps> = ({ userId }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    const loadUser = async () => {
      try {
        const data = await fetchUserById(userId);
        setUser(data);
      } catch (error) {
        console.error('Error fetching user:', error);
      }
    };
    loadUser();
  }, [userId]);

  const handleSave = async () => {
    if (user) {
      try {
        const updatedUser = await updateUser(user);
        setUser(updatedUser);
        setIsEditing(false);
      } catch (error) {
        console.error('Error updating user:', error);
      }
    }
  };

  if (!user) return <div>Chargement...</div>;

  return (
    <div className="profile-container">
      <h2>Profil</h2>
      {isEditing ? (
        <div>
          <label>
            Nom d'utilisateur:
            <input
              type="text"
              value={user.username || ''}
              onChange={(e) =>
                setUser({ ...user, username: e.target.value })
              }
            />
          </label>
          <label>
            Prénom:
            <input
              type="text"
              value={user.firstName || ''}
              onChange={(e) =>
                setUser({ ...user, firstName: e.target.value })
              }
            />
          </label>
          <label>
            Nom:
            <input
              type="text"
              value={user.lastName || ''}
              onChange={(e) =>
                setUser({ ...user, lastName: e.target.value })
              }
            />
          </label>
          <button onClick={handleSave}>Enregistrer</button>
          <button onClick={() => setIsEditing(false)}>Annuler</button>
        </div>
      ) : (
        <div>
          <p>Nom d'utilisateur: {user.username}</p>
          <p>Prénom: {user.firstName}</p>
          <p>Nom: {user.lastName}</p>
          <p>Email: {user.email}</p>
          <button onClick={() => setIsEditing(true)}>Modifier le profil</button>
        </div>
      )}
    </div>
  );
};

export default Profile;
