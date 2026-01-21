// pages/category/category.api.ts
import axios from 'axios';
import type { Category, CategoryCreate, CategoryUpdate } from './category.types';

const API_URL = 'http://localhost:8000/categories';

export const getCategories = async (): Promise<Category[]> => {
  const response = await axios.get(API_URL + '/');
  return response.data;
};

export const createCategory = async (data: CategoryCreate): Promise<Category> => {
  const response = await axios.post(API_URL + '/', data);
  return response.data;
};

export const updateCategory = async (id: number, data: CategoryUpdate): Promise<Category> => {
  const response = await axios.put(`${API_URL}/${id}`, data);
  return response.data;
};

export const deleteCategory = async (id: number): Promise<void> => {
  await axios.delete(`${API_URL}/${id}`);
};