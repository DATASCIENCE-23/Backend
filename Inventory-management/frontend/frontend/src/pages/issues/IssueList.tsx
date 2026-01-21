import React, { useEffect, useState } from 'react';
import { getIssues } from './issue.api';
import type { IssueRequest } from './issue.types';
import PageLayout from '../../components/PageLayout';
import IssueForm from './IssueForm';

const IssueList: React.FC = () => {
  const [issues, setIssues] = useState<IssueRequest[]>([]);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => { loadData(); }, []);

  const loadData = async () => {
    try {
      const data = await getIssues();
      setIssues(data);
    } catch (e) { console.error(e); }
  };

  if (showForm) {
    return (
      <PageLayout title="New Issue Request">
        <IssueForm onSuccess={() => { setShowForm(false); loadData(); }} onCancel={() => setShowForm(false)} />
      </PageLayout>
    );
  }

  return (
    <PageLayout title="Issue Requests" actionLabel="Create Issue" onAction={() => setShowForm(true)}>
      <div className="table-responsive">
        <table className="table table-hover align-middle mb-0">
          <thead className="bg-light text-secondary">
            <tr>
              <th className="ps-4">Req ID</th>
              <th>Date</th>
              <th>Department ID</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {issues.length === 0 ? (
               <tr><td colSpan={4} className="text-center py-4">No issue requests found.</td></tr>
            ) : (
              issues.map(req => (
                <tr key={req.id}>
                  <td className="ps-4 fw-bold">#{req.id}</td>
                  <td>{req.request_date}</td>
                  <td>
                    <span className="badge bg-info text-dark">Dept {req.department_id}</span>
                  </td>
                  <td>
                    <span className={`badge ${req.status === 'approved' ? 'bg-success' : 'bg-warning'}`}>
                      {req.status.toUpperCase()}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </PageLayout>
  );
};

export default IssueList;