// src/pages/items/ItemForm.tsx
import React, { useEffect, useState } from "react";
import { createItem, updateItem } from "./item.api";
import type { Item, ItemCreate } from "./item.types";
import { getCategories } from "../category/category.api";
import type { Category } from "../category/category.types";

interface Props {
  initialData: Item | null;
  onSuccess: () => void;
  onCancel: () => void;
}

const ItemForm: React.FC<Props> = ({ initialData, onSuccess, onCancel }) => {
  const [formData, setFormData] = useState<ItemCreate>({
    code: "",
    name: "",
    unit: "pcs",
    unit_price: 0,
    minimum_stock_level: 10,
    expiry_applicable: true,
    category_id: 0,
    status: "active",
  });

  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getCategories().then(setCategories).catch(console.error);
    if (initialData) {
      setFormData({
        code: initialData.code,
        name: initialData.name,
        unit: initialData.unit,
        unit_price: initialData.unit_price,
        minimum_stock_level: initialData.minimum_stock_level,
        expiry_applicable: initialData.expiry_applicable,
        category_id: initialData.category_id,
        status: initialData.status,
      });
    }
  }, [initialData]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    const { name, value, type } = e.target;
    if (type === "checkbox") {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData((prev) => ({ ...prev, [name]: checked }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = {
        ...formData,
        unit_price: Number(formData.unit_price),
        minimum_stock_level: Number(formData.minimum_stock_level),
        category_id: Number(formData.category_id),
      };

      if (initialData) {
        await updateItem(initialData.id, payload);
      } else {
        await createItem(payload);
      }
      onSuccess();
    } catch (err: any) {
      alert(err.response?.data?.detail || "Error saving item");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      <form onSubmit={handleSubmit}>
        <div className="row g-3">
          <div className="col-md-4">
            <label className="form-label">Item Code</label>
            <input
              name="code"
              className="form-control"
              value={formData.code}
              onChange={handleChange}
              required
              placeholder="Enter item code"
            />
          </div>
          <div className="col-md-8">
            <label className="form-label">Item Name</label>
            <input
              name="name"
              className="form-control"
              value={formData.name}
              onChange={handleChange}
              required
              placeholder="Enter item name"
            />
          </div>

          <div className="col-md-6">
            <label className="form-label" htmlFor="categorySelect">
              Category
            </label>
            <select
              id="categorySelect"
              name="category_id"
              className="form-select"
              value={formData.category_id}
              onChange={handleChange}
              required
            >
              <option value="">Select Category...</option>
              {categories.map((c) => (
                <option key={c.category_id} value={c.category_id}>
                  {c.category_name}
                </option>
              ))}
            </select>
          </div>
          <div className="col-md-3">
            <label className="form-label">Price</label>
            <div className="input-group">
              <span className="input-group-text">$</span>
              <input
                type="number"
                name="unit_price"
                className="form-control"
                value={formData.unit_price}
                onChange={handleChange}
                required
                placeholder="Enter price"
                title="Enter the unit price"
              />
            </div>
          </div>
          <div className="col-md-3">
            <label className="form-label" htmlFor="unitSelect">
              Unit
            </label>
            <select
              id="unitSelect"
              name="unit"
              className="form-select"
              value={formData.unit}
              onChange={handleChange}
            >
              <option value="pcs">Pcs</option>
              <option value="box">Box</option>
              <option value="kg">Kg</option>
              <option value="liters">Liters</option>
            </select>
          </div>

          <div className="col-md-4">
            <label className="form-label">Min Stock Level</label>
            <input
              type="number"
              name="minimum_stock_level"
              className="form-control"
              value={formData.minimum_stock_level}
              onChange={handleChange}
              placeholder="Enter minimum stock level"
              title="Enter the minimum stock level"
            />
          </div>
          <div className="col-md-4 d-flex align-items-end">
            <div className="form-check mb-2">
              <input
                className="form-check-input"
                type="checkbox"
                name="expiry_applicable"
                checked={formData.expiry_applicable}
                onChange={handleChange}
                id="expiryCheck"
              />
              <label className="form-check-label" htmlFor="expiryCheck">
                Expiry Applicable?
              </label>
            </div>
          </div>
          <div className="col-md-4">
            <label className="form-label" htmlFor="statusSelect">
              Status
            </label>
            <select
              id="statusSelect"
              name="status"
              className="form-select"
              value={formData.status}
              onChange={handleChange}
            >
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
            </select>
          </div>
        </div>

        <div className="d-flex justify-content-end gap-2 mt-4 pt-3 border-top">
          <button type="button" className="btn btn-light" onClick={onCancel}>
            Cancel
          </button>
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? "Saving..." : "Save Item"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ItemForm;
