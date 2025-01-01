import React, { useState, useEffect } from 'react';
import { fetchPosts, Post } from '../services/api';

const Home: React.FC = () => {
  const [posts, setPosts] = useState<Post[]>([]);

  useEffect(() => {
    const loadPosts = async () => {
      try {
        const data = await fetchPosts();
        setPosts(data);
      } catch (error) {
        console.error('Error fetching posts:', error);
      }
    };
    loadPosts();
  }, []);

  return (
    <div className="home-container">
      <h2>Liste des billets</h2>
      {posts.length > 0 ? (
        posts.map((post) => (
          <div key={post.id} className="post">
            <h3>{post.title}</h3>
            <p>{post.body}</p>
            <p>Posté par l'utilisateur ID: {post.author_id}</p>
          </div>
        ))
      ) : (
        <p>Aucun billet disponible.</p>
      )}
    </div>
  );
};

export default Home;
