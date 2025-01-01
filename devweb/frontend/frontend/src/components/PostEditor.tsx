import React, { useState } from 'react';
import { createPost } from '../services/api';

interface PostEditorProps {
  userId: number | null;
}

const PostEditor: React.FC<PostEditorProps> = ({ userId }) => {
  const [title, setTitle] = useState('');
  const [body, setBody] = useState('');

  const handleCreate = async () => {
    if (userId) {
      const post = { author_id: userId, title, body };
      await createPost(post);
      alert('Post créé !');
    }
  };

  return (
    <div>
      <h1>Créer un post</h1>
      <input
        type="text"
        placeholder="Titre"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <textarea
        placeholder="Contenu"
        value={body}
        onChange={(e) => setBody(e.target.value)}
      />
      <button onClick={handleCreate}>Publier</button>
    </div>
  );
};

export default PostEditor;
