// src/pages/items/item.types.ts

export interface Item {
  id: number;
  code: string;
  name: string;
  unit: string;
  unit_price: number;
  minimum_stock_level: number;
  expiry_applicable: boolean;
  category_id: number;
  status: 'active' | 'inactive';
}

export interface ItemCreate {
  code: string;
  name: string;
  unit: string;
  unit_price: number;
  minimum_stock_level: number;
  expiry_applicable: boolean;
  category_id: number;
  status: 'active' | 'inactive';
}