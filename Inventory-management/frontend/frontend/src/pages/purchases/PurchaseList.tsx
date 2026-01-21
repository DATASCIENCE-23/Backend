import React, { useEffect, useState } from 'react';
import { getPurchases } from './purchase.api';
import type { Purchase } from './purchase.types';
import { getSuppliers } from '../suppliers/supplier.api'; // To show supplier name
import type { Supplier } from '../suppliers/supplier.types';
import PageLayout from '../../components/PageLayout';
import PurchaseForm from './PurchaseForm';

const PurchaseList: React.FC = () => {
  const [purchases, setPurchases] = useState<Purchase[]>([]);
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => { loadData(); }, []);

  const loadData = async () => {
    try {
      const [pData, sData] = await Promise.all([getPurchases(), getSuppliers()]);
      setPurchases(pData);
      setSuppliers(sData);
    } catch (e) { console.error(e); }
  };

  const getSupplierName = (id: number) => suppliers.find(s => s.id === id)?.name || `ID #${id}`;

  if (showForm) {
    return (
      <PageLayout title="New Purchase Entry">
        <PurchaseForm onSuccess={() => { setShowForm(false); loadData(); }} onCancel={() => setShowForm(false)} />
      </PageLayout>
    );
  }

  return (
    <PageLayout title="Purchase History" actionLabel="New Purchase" onAction={() => setShowForm(true)}>
      <div className="table-responsive">
        <table className="table table-hover align-middle mb-0">
          <thead className="bg-light text-secondary">
            <tr>
              <th className="ps-4">ID</th>
              <th>Date</th>
              <th>Invoice #</th>
              <th>Supplier</th>
              <th>Total Amount</th>
            </tr>
          </thead>
          <tbody>
            {purchases.length === 0 ? (
               <tr><td colSpan={5} className="text-center py-4">No purchases recorded yet.</td></tr>
            ) : (
              purchases.map(p => (
                <tr key={p.id}>
                  <td className="ps-4 text-muted">#{p.id}</td>
                  <td>{p.purchase_date}</td>
                  <td className="fw-bold">{p.invoice_number}</td>
                  <td>{getSupplierName(p.supplier_id)}</td>
                  <td className="fw-bold text-success">${p.total_amount.toFixed(2)}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </PageLayout>
  );
};

export default PurchaseList;