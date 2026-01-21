// src/pages/suppliers/SupplierList.tsx
import React, { useEffect, useState } from "react";
import { getSuppliers, deleteSupplier } from "./supplier.api";
import type { Supplier } from "./supplier.types";
import PageLayout from "../../components/PageLayout";
import SupplierForm from "./SupplierForm";

const SupplierList: React.FC = () => {
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [editingSupplier, setEditingSupplier] = useState<Supplier | null>(null);
  const [search, setSearch] = useState("");

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const data = await getSuppliers();
      setSuppliers(data);
    } catch (e) {
      console.error(e);
    }
  };

  const handleDelete = async (id: number) => {
    if (confirm("Delete this supplier?")) {
      await deleteSupplier(id);
      loadData();
    }
  };

  const filtered = suppliers.filter(
    (s) =>
      s.name.toLowerCase().includes(search.toLowerCase()) ||
      (s.contact_person &&
        s.contact_person.toLowerCase().includes(search.toLowerCase())),
  );

  if (showForm) {
    return (
      <PageLayout title={editingSupplier ? "Edit Supplier" : "Add Supplier"}>
        <SupplierForm
          initialData={editingSupplier}
          onSuccess={() => {
            setShowForm(false);
            loadData();
          }}
          onCancel={() => setShowForm(false)}
        />
      </PageLayout>
    );
  }

  return (
    <PageLayout
      title="Suppliers Directory"
      actionLabel="Add Supplier"
      onAction={() => {
        setEditingSupplier(null);
        setShowForm(true);
      }}
    >
      <div className="p-3 bg-light border-bottom">
        <input
          className="form-control"
          placeholder="Search suppliers..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ maxWidth: "300px" }}
        />
      </div>

      <div className="table-responsive">
        <table className="table table-hover align-middle mb-0">
          <thead className="bg-light text-secondary">
            <tr>
              <th className="ps-4">Name</th>
              <th>Contact Person</th>
              <th>Phone / Email</th>
              <th>Address</th>
              <th className="text-end pe-4">Actions</th>
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr>
                <td colSpan={5} className="text-center py-4">
                  No suppliers found.
                </td>
              </tr>
            ) : (
              filtered.map((sup) => (
                <tr key={sup.id}>
                  <td className="ps-4 fw-bold text-dark">{sup.name}</td>
                  <td>
                    {sup.contact_person || (
                      <span className="text-muted">-</span>
                    )}
                  </td>
                  <td>
                    <div className="small">
                      <i className="fas fa-phone me-1 text-muted"></i>{" "}
                      {sup.phone || "-"}
                    </div>
                    <div className="small text-primary">
                      <i className="fas fa-envelope me-1 text-muted"></i>{" "}
                      {sup.email || "-"}
                    </div>
                  </td>
                  <td
                    className="text-muted small"
                    style={{ maxWidth: "200px" }}
                  >
                    {sup.address || "-"}
                  </td>
                  <td className="text-end pe-4">
                    <button
                      className="btn btn-sm btn-light text-primary me-2"
                      title="Edit Supplier"
                      onClick={() => {
                        setEditingSupplier(sup);
                        setShowForm(true);
                      }}
                    >
                      <i className="fas fa-edit"></i>
                    </button>
                    <button
                      className="btn btn-sm btn-light text-danger"
                      type="button"
                      title="Delete Supplier"
                      aria-label="Delete Supplier"
                      onClick={() => handleDelete(sup.id)}
                    >
                      <i className="fas fa-trash" aria-hidden="true"></i>
                    </button>
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

export default SupplierList;
