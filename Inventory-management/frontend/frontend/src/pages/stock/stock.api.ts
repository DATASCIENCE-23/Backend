// src/pages/stock/stock.api.ts
import axios from 'axios';
import type { Stock, StockCreate } from './stock.types';

const API_URL = 'http://localhost:8000/stock';

export const getStocks = async (): Promise<Stock[]> => {
  const response = await axios.get(API_URL + '/');
  return response.data;
};

export const addStock = async (data: StockCreate): Promise<Stock> => {
  const response = await axios.post(API_URL + '/', data);
  return response.data;
};

export const updateStock = async (id: number, data: Partial<StockCreate>): Promise<Stock> => {
  const response = await axios.put(`${API_URL}/${id}`, data);
  return response.data;
};

export const deleteStock = async (id: number): Promise<void> => {
  await axios.delete(`${API_URL}/${id}`);
};