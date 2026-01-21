// src/pages/audits/audit.api.ts
import axios from 'axios';
import type { StockAudit, AuditCreate } from './audit.types';

const API_URL = 'http://localhost:8000/stock-audits';

export const getAudits = async (): Promise<StockAudit[]> => {
  const response = await axios.get(API_URL + '/');
  return response.data;
};

export const createAudit = async (data: AuditCreate): Promise<StockAudit> => {
  const response = await axios.post(API_URL + '/', data);
  return response.data;
};