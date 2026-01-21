// src/pages/stock-adjustments/adjustment.types.ts

export interface StockAdjustment {
  id: number;
  item_id: number;
  location_id: number;
  adjustment_type: 'ADD' | 'SUBTRACT';
  quantity_changed: number;
  reason: string;
  adjustment_date: string;
}

export interface StockAdjustmentCreate {
  item_id: number;
  location_id: number;
  adjustment_type: 'ADD' | 'SUBTRACT';
  quantity_changed: number;
  reason: string;
}