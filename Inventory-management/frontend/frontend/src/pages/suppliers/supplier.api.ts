// src/pages/suppliers/supplier.api.ts
import axios from 'axios';
import type { Supplier, SupplierCreate } from './supplier.types';

// Adjust port if necessary
const API_URL = 'http://localhost:8000/suppliers';

export const getSuppliers = async (): Promise<Supplier[]> => {
  const response = await axios.get(API_URL + '/');
  return response.data;
};

export const createSupplier = async (data: SupplierCreate): Promise<Supplier> => {
  const response = await axios.post(API_URL + '/', data);
  return response.data;
};

export const updateSupplier = async (id: number, data: SupplierCreate): Promise<Supplier> => {
  const response = await axios.put(`${API_URL}/${id}`, data);
  return response.data;
};

export const deleteSupplier = async (id: number): Promise<void> => {
  await axios.delete(`${API_URL}/${id}`);
};