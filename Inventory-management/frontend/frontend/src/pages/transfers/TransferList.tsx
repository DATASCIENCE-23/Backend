// src/pages/transfers/TransferList.tsx
import React, { useEffect, useState } from 'react';
import { getTransfers } from './transfer.api';
import type { StockTransfer } from './transfer.types';
import { getItems } from '../items/item.api';
import { getLocations } from '../locations/location.api';
import type { Item } from '../items/item.types';
import type { StoreLocation } from '../locations/location.types';
import PageLayout from '../../components/PageLayout';
import TransferForm from './TransferForm';

const TransferList: React.FC = () => {
  const [transfers, setTransfers] = useState<StockTransfer[]>([]);
  const [items, setItems] = useState<Item[]>([]);
  const [locations, setLocations] = useState<StoreLocation[]>([]);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => { loadData(); }, []);

  const loadData = async () => {
    try {
      const [tData, iData, lData] = await Promise.all([
        getTransfers(), getItems(), getLocations()
      ]);
      setTransfers(tData);
      setItems(iData);
      setLocations(lData);
    } catch (e) { console.error(e); }
  };

  const getName = (id: number, list: any[]) => list.find(x => x.id === id)?.name || id;

  if (showForm) {
    return (
      <PageLayout title="New Stock Transfer">
        <TransferForm onSuccess={() => { setShowForm(false); loadData(); }} onCancel={() => setShowForm(false)} />
      </PageLayout>
    );
  }

  return (
    <PageLayout title="Stock Transfer History" actionLabel="New Transfer" onAction={() => setShowForm(true)}>
      <div className="table-responsive">
        <table className="table table-hover align-middle mb-0">
          <thead className="bg-light text-secondary">
            <tr>
              <th className="ps-4">Date</th>
              <th>Item</th>
              <th>From</th>
              <th>To</th>
              <th>Quantity</th>
            </tr>
          </thead>
          <tbody>
            {transfers.length === 0 ? (
               <tr><td colSpan={5} className="text-center py-4">No transfers recorded.</td></tr>
            ) : (
              transfers.map(t => (
                <tr key={t.id}>
                  <td className="ps-4 text-muted small">{t.transfer_date}</td>
                  <td className="fw-bold text-primary">{getName(t.item_id, items)}</td>
                  <td>
                    <span className="badge bg-light text-dark border">{getName(t.from_location_id, locations)}</span>
                  </td>
                  <td>
                    <span className="badge bg-light text-dark border">{getName(t.to_location_id, locations)}</span>
                  </td>
                  <td className="fw-bold">{t.quantity}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </PageLayout>
  );
};

export default TransferList;