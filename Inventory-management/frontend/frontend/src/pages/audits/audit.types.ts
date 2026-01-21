// src/pages/audits/audit.types.ts

export interface AuditItem {
  item_id: number;
  physical_quantity: number;
}

export interface AuditCreate {
  location_id: number;
  remarks: string;
  items: AuditItem[];
}

export interface StockAudit {
  id: number;
  location_id: number;
  audit_date: string;
  remarks: string;
}