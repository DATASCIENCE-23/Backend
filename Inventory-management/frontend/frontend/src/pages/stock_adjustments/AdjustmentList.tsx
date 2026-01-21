// src/pages/stock-adjustments/AdjustmentList.tsx
import React, { useEffect, useState } from 'react';
import { getAdjustments } from './adjustment.api';
import type { StockAdjustment } from './adjustment.types';
import { getItems } from '../items/item.api';
import { getLocations } from '../locations/location.api';
import type { Item } from '../items/item.types';
import type { StoreLocation } from '../locations/location.types';
import PageLayout from '../../components/PageLayout';
import AdjustmentForm from './AdjustmentForm';

const AdjustmentList: React.FC = () => {
  const [adjustments, setAdjustments] = useState<StockAdjustment[]>([]);
  const [items, setItems] = useState<Item[]>([]);
  const [locations, setLocations] = useState<StoreLocation[]>([]);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => { loadData(); }, []);

  const loadData = async () => {
    try {
      const [adjData, itemData, locData] = await Promise.all([
        getAdjustments(), getItems(), getLocations()
      ]);
      setAdjustments(adjData);
      setItems(itemData);
      setLocations(locData);
    } catch (e) { console.error(e); }
  };

  const getName = (id: number, list: any[]) => list.find(x => x.id === id)?.name || id;

  if (showForm) {
    return (
      <PageLayout title="New Stock Adjustment">
        <AdjustmentForm onSuccess={() => { setShowForm(false); loadData(); }} onCancel={() => setShowForm(false)} />
      </PageLayout>
    );
  }

  return (
    <PageLayout title="Stock Adjustment History" actionLabel="New Adjustment" onAction={() => setShowForm(true)}>
      <div className="table-responsive">
        <table className="table table-hover align-middle mb-0">
          <thead className="bg-light text-secondary">
            <tr>
              <th className="ps-4">Date</th>
              <th>Item</th>
              <th>Location</th>
              <th>Type</th>
              <th>Qty</th>
              <th>Reason</th>
            </tr>
          </thead>
          <tbody>
            {adjustments.length === 0 ? (
               <tr><td colSpan={6} className="text-center py-4">No adjustments recorded.</td></tr>
            ) : (
              adjustments.map(adj => (
                <tr key={adj.id}>
                  <td className="ps-4 text-muted small">{adj.adjustment_date}</td>
                  <td className="fw-bold">{getName(adj.item_id, items)}</td>
                  <td>{getName(adj.location_id, locations)}</td>
                  <td>
                    <span className={`badge ${adj.adjustment_type === 'ADD' ? 'bg-success' : 'bg-danger'}`}>
                      {adj.adjustment_type}
                    </span>
                  </td>
                  <td className="fw-bold">{adj.quantity_changed}</td>
                  <td className="text-muted small fst-italic">{adj.reason}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </PageLayout>
  );
};

export default AdjustmentList;