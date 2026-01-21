// src/pages/category/CategoryList.tsx
import React, { useEffect, useState } from 'react';
import { getCategories, deleteCategory } from './category.api';
import type { Category } from './category.types';
import CategoryForm from './CategoryForm';
import PageLayout from '../../components/PageLayout'; // Import the new template

const CategoryList: React.FC = () => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [search, setSearch] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingCategory, setEditingCategory] = useState<Category | null>(null);

  useEffect(() => { loadCategories(); }, []);

  const loadCategories = async () => {
    try {
      const data = await getCategories();
      setCategories(data);
    } catch (err) { console.error(err); }
  };

  const handleDelete = async (id: number) => {
    if (confirm('Delete this category?')) {
      await deleteCategory(id);
      loadCategories();
    }
  };

  const handleSaveSuccess = () => {
    setShowForm(false);
    loadCategories();
  };

  // Filter Logic
  const filtered = categories.filter(c => 
    c.category_name.toLowerCase().includes(search.toLowerCase())
  );

  // VIEW 1: The Form (If adding/editing)
  if (showForm) {
    return (
      <PageLayout title={editingCategory ? "Edit Category" : "New Category"}>
        <div className="p-4">
           <CategoryForm 
             initialData={editingCategory} 
             onSuccess={handleSaveSuccess} 
             onCancel={() => setShowForm(false)} 
           />
        </div>
      </PageLayout>
    );
  }

  // VIEW 2: The List (Default)
  return (
    <PageLayout 
      title="Inventory Categories" 
      actionLabel="Add Category" 
      onAction={() => { setEditingCategory(null); setShowForm(true); }}
    >
      {/* Search Bar Area */}
      <div className="p-3 bg-light border-bottom">
        <input 
          type="text" 
          className="form-control" 
          placeholder="🔍 Search categories..." 
          style={{ maxWidth: '300px' }}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* The Table */}
      <div className="table-responsive">
        <table className="table table-hover align-middle mb-0">
          <thead className="bg-light text-secondary">
            <tr>
              <th className="ps-4">ID</th>
              <th>Name</th>
              <th>Description</th>
              <th className="text-end pe-4">Actions</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((cat) => (
              <tr key={cat.category_id}>
                <td className="ps-4 fw-bold">#{cat.category_id}</td>
                <td>{cat.category_name}</td>
                <td className="text-muted">{cat.description || '-'}</td>
                <td className="text-end pe-4">
                  <button onClick={() => { setEditingCategory(cat); setShowForm(true); }} className="btn btn-sm btn-light text-primary me-2">
                    <i className="fas fa-edit"></i> {/* Icon needs FontAwesome in index.html */}
                  </button>
                  <button
                    type="button"
                    onClick={() => handleDelete(cat.category_id)}
                    className="btn btn-sm btn-light text-danger"
                    title="Delete category"
                    aria-label="Delete category"
                  >
                    <i className="fas fa-trash" aria-hidden="true"></i>
                    <span className="visually-hidden">Delete</span>
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </PageLayout>
  );
};

export default CategoryList;