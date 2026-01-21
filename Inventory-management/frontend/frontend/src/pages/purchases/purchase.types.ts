export interface PurchaseItem {
  item_id: number;
  quantity: number;
  purchase_price: number;
}

export interface PurchaseCreate {
  supplier_id: number;
  invoice_number: string;
  items: PurchaseItem[];
}

export interface Purchase {
  id: number;
  supplier_id: number;
  invoice_number: string;
  purchase_date: string;
  total_amount: number;
}