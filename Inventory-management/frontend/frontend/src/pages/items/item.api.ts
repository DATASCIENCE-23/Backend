// src/pages/items/item.api.ts
import axios from 'axios';
import type{ Item, ItemCreate } from './item.types';

const API_URL = 'http://localhost:8000/items';

export const getItems = async (): Promise<Item[]> => {
  const response = await axios.get(API_URL + '/');
  return response.data;
};

export const createItem = async (data: ItemCreate): Promise<Item> => {
  const response = await axios.post(API_URL + '/', data);
  return response.data;
};

export const updateItem = async (id: number, data: Partial<ItemCreate>): Promise<Item> => {
  const response = await axios.put(`${API_URL}/${id}`, data);
  return response.data;
};

export const deleteItem = async (id: number): Promise<void> => {
  await axios.delete(`${API_URL}/${id}`);
};