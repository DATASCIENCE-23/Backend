// src/pages/transfers/transfer.types.ts

export interface StockTransfer {
  id: number;
  item_id: number;
  from_location_id: number;
  to_location_id: number;
  quantity: number;
  transfer_date: string;
}

export interface StockTransferCreate {
  item_id: number;
  from_location_id: number;
  to_location_id: number;
  quantity: number;
}