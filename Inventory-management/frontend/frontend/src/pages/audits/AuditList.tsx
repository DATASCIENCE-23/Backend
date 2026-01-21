// src/pages/audits/AuditList.tsx
import React, { useEffect, useState } from 'react';
import { getAudits } from './audit.api';
import type { StockAudit } from './audit.types';
import { getLocations } from '../locations/location.api';
import type { StoreLocation } from '../locations/location.types';
import PageLayout from '../../components/PageLayout';
import AuditForm from './AuditForm';

const AuditList: React.FC = () => {
  const [audits, setAudits] = useState<StockAudit[]>([]);
  const [locations, setLocations] = useState<StoreLocation[]>([]);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => { loadData(); }, []);

  const loadData = async () => {
    try {
      const [aData, lData] = await Promise.all([getAudits(), getLocations()]);
      setAudits(aData);
      setLocations(lData);
    } catch (e) { console.error(e); }
  };

  const getLocName = (id: number) => locations.find(l => l.id === id)?.name || id;

  if (showForm) {
    return (
      <PageLayout title="New Stock Audit">
        <AuditForm onSuccess={() => { setShowForm(false); loadData(); }} onCancel={() => setShowForm(false)} />
      </PageLayout>
    );
  }

  return (
    <PageLayout title="Stock Audits" actionLabel="Perform Audit" onAction={() => setShowForm(true)}>
      <div className="table-responsive">
        <table className="table table-hover align-middle mb-0">
          <thead className="bg-light text-secondary">
            <tr>
              <th className="ps-4">ID</th>
              <th>Date</th>
              <th>Location</th>
              <th>Remarks</th>
            </tr>
          </thead>
          <tbody>
            {audits.length === 0 ? (
               <tr><td colSpan={4} className="text-center py-4">No audits found.</td></tr>
            ) : (
              audits.map(audit => (
                <tr key={audit.id}>
                  <td className="ps-4 fw-bold">#{audit.id}</td>
                  <td>{audit.audit_date}</td>
                  <td>
                    <span className="badge bg-light text-dark border">
                      <i className="fas fa-map-marker-alt me-1 text-muted"></i>
                      {getLocName(audit.location_id)}
                    </span>
                  </td>
                  <td className="text-muted">{audit.remarks || '-'}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </PageLayout>
  );
};

export default AuditList;