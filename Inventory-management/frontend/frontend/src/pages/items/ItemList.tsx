// src/pages/items/ItemList.tsx
import React, { useEffect, useState } from 'react';
import { getItems, deleteItem } from './item.api';
import type { Item } from './item.types';
import PageLayout from '../../components/PageLayout';
import ItemForm from './ItemForm';

const ItemList: React.FC = () => {
  const [items, setItems] = useState<Item[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [editingItem, setEditingItem] = useState<Item | null>(null);
  const [search, setSearch] = useState('');

  useEffect(() => { loadData(); }, []);

  const loadData = async () => {
    try {
      const data = await getItems();
      setItems(data);
    } catch (e) { console.error(e); }
  };

  const handleDelete = async (id: number) => {
    if (confirm("Delete this item?")) {
      await deleteItem(id);
      loadData();
    }
  };

  const filtered = items.filter(m => 
    m.name.toLowerCase().includes(search.toLowerCase()) || 
    m.code.toLowerCase().includes(search.toLowerCase())
  );

  if (showForm) {
    return (
      <PageLayout title={editingItem ? "Edit Item" : "Add Item"}>
        <ItemForm 
          initialData={editingItem} 
          onSuccess={() => { setShowForm(false); loadData(); }} 
          onCancel={() => setShowForm(false)} 
        />
      </PageLayout>
    );
  }

  return (
    <PageLayout 
      title="Inventory Items" 
      actionLabel="Add Item" 
      onAction={() => { setEditingItem(null); setShowForm(true); }}
    >
      <div className="p-3 bg-light border-bottom">
        <input 
          className="form-control" 
          placeholder="Search items..." 
          value={search}
          onChange={e => setSearch(e.target.value)} 
          style={{ maxWidth: '300px' }}
        />
      </div>

      <div className="table-responsive">
        <table className="table table-hover align-middle mb-0">
          <thead className="bg-light text-secondary small text-uppercase">
            <tr>
              <th className="ps-4">Code</th>
              <th>Name</th>
              <th>Price</th>
              <th>Unit</th>
              <th>Status</th>
              <th className="text-end pe-4">Actions</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map(item => (
              <tr key={item.id}>
                <td className="ps-4 fw-bold text-primary">{item.code}</td>
                <td>
                  <div className="fw-semibold">{item.name}</div>
                  <small className="text-muted">Cat ID: {item.category_id}</small>
                </td>
                <td>${item.unit_price.toFixed(2)}</td>
                <td><span className="badge bg-light text-dark border">{item.unit}</span></td>
                <td>
                  <span className={`badge ${item.status === 'active' ? 'bg-success' : 'bg-secondary'}`}>
                    {item.status}
                  </span>
                </td>
                <td className="text-end pe-4">
                  <button
                    className="btn btn-sm btn-light text-primary me-1"
                    onClick={() => { setEditingItem(item); setShowForm(true); }}
                    title="Edit Item"
                  >
                    <i className="fas fa-edit"></i>
                  </button>
                  <button
                    className="btn btn-sm btn-light text-danger"
                    onClick={() => handleDelete(item.id)}
                    title="Delete Item"
                  >
                    <i className="fas fa-trash"></i>
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

export default ItemList;