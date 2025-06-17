import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000/api/',
});

export const loginUser = (credentials) =>
  API.post('token/', credentials);

export const fetchProducts = () =>
  API.get('products/');

export const createProduct = (product, token) =>
  API.post('products/', product, {
    headers: { Authorization: `Bearer ${token}` },
  });

export default API;
