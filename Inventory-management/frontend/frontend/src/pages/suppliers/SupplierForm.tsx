// src/pages/suppliers/SupplierForm.tsx
import React, { useState, useEffect } from 'react';
import { createSupplier, updateSupplier } from './supplier.api';
import type { Supplier, SupplierCreate } from './supplier.types';

interface Props {
  initialData: Supplier | null;
  onSuccess: () => void;
  onCancel: () => void;
}

const SupplierForm: React.FC<Props> = ({ initialData, onSuccess, onCancel }) => {
  const [formData, setFormData] = useState<SupplierCreate>({
    name: '',
    contact_person: '',
    phone: '',
    email: '',
    address: ''
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (initialData) {
      setFormData({
        name: initialData.name,
        contact_person: initialData.contact_person || '',
        phone: initialData.phone || '',
        email: initialData.email || '',
        address: initialData.address || ''
      });
    }
  }, [initialData]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (initialData) {
        await updateSupplier(initialData.id, formData);
      } else {
        await createSupplier(formData);
      }
      onSuccess();
    } catch (err: any) {
      alert("Error saving supplier. " + (err.response?.data?.detail || ""));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      <form onSubmit={handleSubmit}>
        <div className="row g-3">
          {/* Name & Contact */}
          <div className="col-md-6">
            <label className="form-label">Supplier Name <span className="text-danger">*</span></label>
            <input 
              name="name" 
              className="form-control" 
              value={formData.name} 
              onChange={handleChange} 
              required 
              placeholder="e.g. Apex Pharma Distributors"
            />
          </div>
          <div className="col-md-6">
            <label className="form-label">Contact Person</label>
            <input 
              name="contact_person" 
              className="form-control" 
              value={formData.contact_person} 
              onChange={handleChange} 
              placeholder="e.g. Mr. John Doe"
            />
          </div>

          {/* Contact Details */}
          <div className="col-md-6">
            <label className="form-label">Phone Number</label>
            <input 
              name="phone" 
              className="form-control" 
              value={formData.phone} 
              onChange={handleChange} 
              placeholder="+91 98765..."
            />
          </div>
          <div className="col-md-6">
            <label className="form-label">Email</label>
            <input 
              type="email"
              name="email" 
              className="form-control" 
              value={formData.email} 
              onChange={handleChange} 
              placeholder="contact@apexpharma.com"
            />
          </div>

          {/* Address */}
          <div className="col-12">
            <label className="form-label">Address</label>
            <textarea 
              name="address" 
              className="form-control" 
              rows={2} 
              value={formData.address} 
              onChange={handleChange}
              placeholder="Full billing address..."
            />
          </div>
        </div>

        <div className="d-flex justify-content-end gap-2 mt-4 pt-3 border-top">
          <button type="button" className="btn btn-secondary" onClick={onCancel}>Cancel</button>
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Saving...' : 'Save Supplier'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default SupplierForm;