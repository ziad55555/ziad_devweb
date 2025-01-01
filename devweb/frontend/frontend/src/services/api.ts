import axios from 'axios';

const API_BASE_URL = 'http://localhost:9456';

// Types
export interface User {
  id: number;
  username: string;
  firstName: string;
  lastName: string;
  email: string;
  avatar: string;
}

export interface Post {
  id?: number;
  author_id: number;
  title: string;
  body: string;
  created?: string;
}

export const fetchPosts = async (): Promise<Post[]> => {
  const response = await axios.get(`${API_BASE_URL}/posts`);
  return response.data;
};

export const createPost = async (post: Post): Promise<Post> => {
  const response = await axios.post(`${API_BASE_URL}/posts`, post);
  return response.data;
};

export const deletePost = async (postId: number): Promise<void> => {
  await axios.delete(`${API_BASE_URL}/posts/${postId}`);
};

export const likePost = async (postId: number, userId: number): Promise<void> => {
  await axios.post(`${API_BASE_URL}/stars`, { post_id: postId, user_id: userId });
};

export const fetchUserById = async (userId: number): Promise<User> => {
  const response = await axios.get(`${API_BASE_URL}/users/${userId}`);
  return response.data;
};

export const fetchUser = async (username: string): Promise<User> => {
  const response = await axios.get(`${API_BASE_URL}/users/${username}`);
  return response.data;
};

export const fetchLikes = async (postId: number): Promise<number> => {
  const response = await axios.get(`${API_BASE_URL}/posts/${postId}/stars`);
  return response.data.count;
};

export const updateUser = async (user: User): Promise<User> => {
  const response = await axios.put(`${API_BASE_URL}/users/${user.id}`, user);
  return response.data;
};





