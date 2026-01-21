// src/pages/stock/stock.types.ts

export interface Stock {
  id: number;
  item_id: number;
  location_id: number;
  quantity_available: number;
  last_updated: string;
}

export interface StockCreate {
  item_id: number;
  location_id: number;
  quantity_available: number;
}