import axios from 'axios';
import type { Purchase, PurchaseCreate } from './purchase.types';

const API_URL = 'http://localhost:8000/purchases';

export const getPurchases = async (): Promise<Purchase[]> => {
  const response = await axios.get(API_URL + '/');
  return response.data;
};

export const createPurchase = async (data: PurchaseCreate): Promise<Purchase> => {
  const response = await axios.post(API_URL + '/', data);
  return response.data;
};