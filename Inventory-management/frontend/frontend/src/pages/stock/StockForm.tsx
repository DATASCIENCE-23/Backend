// src/pages/stock/StockForm.tsx
import React, { useState, useEffect } from "react";
import { addStock, updateStock } from "./stock.api";
import type { Stock, StockCreate } from "./stock.types";
import { getItems } from "../items/item.api";
import { getLocations } from "../locations/location.api";
import type { Item } from "../items/item.types";
import type { StoreLocation } from "../locations/location.types";

interface Props {
  initialData: Stock | null;
  onSuccess: () => void;
  onCancel: () => void;
}

const StockForm: React.FC<Props> = ({ initialData, onSuccess, onCancel }) => {
  const [formData, setFormData] = useState<StockCreate>({
    item_id: 0,
    location_id: 0,
    quantity_available: 0,
  });

  const [items, setItems] = useState<Item[]>([]);
  const [locations, setLocations] = useState<StoreLocation[]>([]);
  const [loading, setLoading] = useState(false);

  // Load Dropdown Data
  useEffect(() => {
    Promise.all([getItems(), getLocations()])
      .then(([itemsData, locsData]) => {
        setItems(itemsData);
        setLocations(locsData);
      })
      .catch(console.error);

    if (initialData) {
      setFormData({
        item_id: initialData.item_id,
        location_id: initialData.location_id,
        quantity_available: initialData.quantity_available,
      });
    }
  }, [initialData]);

  const handleChange = (
    e: React.ChangeEvent<HTMLSelectElement | HTMLInputElement>,
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: Number(value) }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.item_id === 0 || formData.location_id === 0) {
      alert("Please select both an Item and a Location");
      return;
    }

    setLoading(true);
    try {
      if (initialData) {
        await updateStock(initialData.id, formData);
      } else {
        await addStock(formData);
      }
      onSuccess();
    } catch (err: any) {
      alert(
        "Error saving stock: " +
          (err.response?.data?.detail || "Unknown error"),
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      <div className="alert alert-info small">
        <i className="fas fa-info-circle me-2"></i>
        {initialData
          ? "Update the quantity directly."
          : "If stock exists for this item & location, quantity will be added to the existing record."}
      </div>

      <form onSubmit={handleSubmit}>
        <div className="row g-3">
          {/* Item Selection */}
          <div className="col-md-6">
            <label className="form-label" htmlFor="item_id_select">
              Item
            </label>
            <select
              id="item_id_select"
              name="item_id"
              className="form-select"
              value={formData.item_id}
              onChange={handleChange}
              disabled={!!initialData} // Lock item if editing
            >
              <option value={0}>Select Item...</option>
              {items.map((item) => (
                <option key={item.id} value={item.id}>
                  {item.name} ({item.code})
                </option>
              ))}
            </select>
          </div>

          {/* Location Selection */}
          <div className="col-md-6">
            <label className="form-label" htmlFor="location_id_select">
              Store Location
            </label>
            <select
              id="location_id_select"
              name="location_id"
              className="form-select"
              value={formData.location_id}
              onChange={handleChange}
              disabled={!!initialData} // Lock location if editing
            >
              <option value={0}>Select Location...</option>
              {locations.map((loc) => (
                <option key={loc.id} value={loc.id}>
                  {loc.name}
                </option>
              ))}
            </select>
          </div>

          {/* Quantity */}
          <div className="col-md-4">
            <label className="form-label">Quantity</label>
            <input
              type="number"
              name="quantity_available"
              className="form-control"
              value={formData.quantity_available}
              onChange={handleChange}
              min="0"
              required
              placeholder="Enter quantity"
            />
          </div>
        </div>

        <div className="d-flex justify-content-end gap-2 mt-4 pt-3 border-top">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={onCancel}
          >
            Cancel
          </button>
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? "Saving..." : initialData ? "Update Stock" : "Add Stock"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default StockForm;
