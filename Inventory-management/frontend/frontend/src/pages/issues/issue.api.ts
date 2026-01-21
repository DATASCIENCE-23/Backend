import axios from 'axios';
import type { IssueRequest, IssueCreate } from './issue.types';

const API_URL = 'http://localhost:8000/issues';

export const getIssues = async (): Promise<IssueRequest[]> => {
  const response = await axios.get(API_URL + '/');
  return response.data;
};

export const createIssue = async (data: IssueCreate): Promise<IssueRequest> => {
  const response = await axios.post(API_URL + '/', data);
  return response.data;
};