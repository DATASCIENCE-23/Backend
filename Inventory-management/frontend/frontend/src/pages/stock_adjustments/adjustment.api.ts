// src/pages/stock-adjustments/adjustment.api.ts
import axios from 'axios';
import type { StockAdjustment, StockAdjustmentCreate } from './adjustment.types';

const API_URL = 'http://localhost:8000/stock-adjustments';

export const getAdjustments = async (): Promise<StockAdjustment[]> => {
  const response = await axios.get(API_URL + '/');
  return response.data;
};

export const createAdjustment = async (data: StockAdjustmentCreate): Promise<StockAdjustment> => {
  const response = await axios.post(API_URL + '/', data);
  return response.data;
};