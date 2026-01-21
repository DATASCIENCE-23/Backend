// src/pages/transfers/transfer.api.ts
import axios from 'axios';
import type { StockTransfer, StockTransferCreate } from './transfer.types';

const API_URL = 'http://localhost:8000/stock-transfers';

export const getTransfers = async (): Promise<StockTransfer[]> => {
  const response = await axios.get(API_URL + '/');
  return response.data;
};

export const createTransfer = async (data: StockTransferCreate): Promise<StockTransfer> => {
  const response = await axios.post(API_URL + '/', data);
  return response.data;
};