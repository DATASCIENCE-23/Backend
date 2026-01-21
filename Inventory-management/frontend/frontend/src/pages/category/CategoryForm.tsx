// pages/category/CategoryForm.tsx
import React, { useState, useEffect } from 'react';
import { createCategory, updateCategory } from './category.api';
import type { Category } from './category.types';

interface Props {
  initialData: Category | null;
  onSuccess: () => void;
  onCancel: () => void;
}

const CategoryForm: React.FC<Props> = ({ initialData, onSuccess, onCancel }) => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Populate form if editing
  useEffect(() => {
    if (initialData) {
      setName(initialData.category_name); // Map category_name to input
      setDescription(initialData.description || '');
    }
  }, [initialData]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const payload = { name, description };
      
      if (initialData) {
        await updateCategory(initialData.category_id, payload);
      } else {
        await createCategory(payload);
      }
      onSuccess();
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Error saving category');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="card shadow-sm border-0">
      <div className="card-header bg-white border-bottom-0 pt-4">
        <h4>{initialData ? 'Edit Category' : 'Create New Category'}</h4>
      </div>
      <div className="card-body">
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Category Name <span className="text-danger">*</span></label>
            <input 
              type="text" 
              className="form-control" 
              value={name} 
              onChange={(e) => setName(e.target.value)} 
              required 
              placeholder="e.g. Tablets, Syrups"
            />
          </div>

          <div className="mb-3">
            <label className="form-label">Description</label>
            <textarea 
              className="form-control" 
              rows={3} 
              value={description} 
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Optional details..."
            />
          </div>

          <div className="d-flex justify-content-end gap-2">
            <button type="button" className="btn btn-secondary" onClick={onCancel}>
              Cancel
            </button>
            <button type="submit" className="btn btn-success" disabled={isSubmitting}>
              {isSubmitting ? 'Saving...' : (initialData ? 'Update Category' : 'Save Category')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CategoryForm;