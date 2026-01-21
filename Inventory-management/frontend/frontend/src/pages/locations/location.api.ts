import axios from 'axios';
import type { StoreLocation, StoreLocationCreate } from './location.types';

const API_URL = 'http://localhost:8000/locations';

export const getLocations = async (): Promise<StoreLocation[]> => {
  const response = await axios.get(API_URL + '/');
  return response.data;
};

export const createLocation = async (data: StoreLocationCreate): Promise<StoreLocation> => {
  const response = await axios.post(API_URL + '/', data);
  return response.data;
};

export const updateLocation = async (id: number, data: StoreLocationCreate): Promise<void> => {
  await axios.put(`${API_URL}/${id}`, data);
};

export const deleteLocation = async (id: number): Promise<void> => {
  await axios.delete(`${API_URL}/${id}`);
};