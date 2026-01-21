export interface IssueItem {
  item_id: number;
  quantity: number;
}

export interface IssueCreate {
  department_id: number;
  items: IssueItem[];
}

export interface IssueRequest {
  id: number;
  department_id: number;
  request_date: string;
  status: string;
}