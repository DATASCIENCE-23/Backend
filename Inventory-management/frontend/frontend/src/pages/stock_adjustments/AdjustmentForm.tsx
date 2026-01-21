// src/pages/stock-adjustments/AdjustmentForm.tsx
import React, { useState, useEffect } from "react";
import { createAdjustment } from "./adjustment.api";
import type { StockAdjustmentCreate } from "./adjustment.types";
import { getItems } from "../items/item.api";
import { getLocations } from "../locations/location.api";
import type { Item } from "../items/item.types";
import type { StoreLocation } from "../locations/location.types";

interface Props {
  onSuccess: () => void;
  onCancel: () => void;
}

const AdjustmentForm: React.FC<Props> = ({ onSuccess, onCancel }) => {
  const [items, setItems] = useState<Item[]>([]);
  const [locations, setLocations] = useState<StoreLocation[]>([]);
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState<StockAdjustmentCreate>({
    item_id: 0,
    location_id: 0,
    adjustment_type: "SUBTRACT", // Default to subtract (most common for damage)
    quantity_changed: 1,
    reason: "",
  });

  useEffect(() => {
    Promise.all([getItems(), getLocations()])
      .then(([iData, lData]) => {
        setItems(iData);
        setLocations(lData);
      })
      .catch(console.error);
  }, []);

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >,
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]:
        name === "item_id" ||
        name === "location_id" ||
        name === "quantity_changed"
          ? Number(value)
          : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.item_id === 0 || formData.location_id === 0) {
      alert("Please select both Item and Location");
      return;
    }

    setLoading(true);
    try {
      await createAdjustment(formData);
      alert("Stock Adjusted Successfully");
      onSuccess();
    } catch (err: any) {
      alert("Error: " + (err.response?.data?.detail || "Failed"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      <form onSubmit={handleSubmit}>
        <div className="row g-3">
          {/* Item & Location */}
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
              required
            >
              <option value={0}>Select Item...</option>
              {items.map((i) => (
                <option key={i.id} value={i.id}>
                  {i.name} ({i.code})
                </option>
              ))}
            </select>
          </div>
          <div className="col-md-6">
            <label className="form-label" htmlFor="location_id_select">
              Location
            </label>
            <select
              id="location_id_select"
              name="location_id"
              className="form-select"
              value={formData.location_id}
              onChange={handleChange}
              required
            >
              <option value={0}>Select Store...</option>
              {locations.map((l) => (
                <option key={l.id} value={l.id}>
                  {l.name}
                </option>
              ))}
            </select>
          </div>

          {/* Action Type */}
          <div className="col-md-12">
            <label className="form-label d-block">Adjustment Type</label>
            <div className="btn-group" role="group">
              <input
                type="radio"
                className="btn-check"
                name="adjustment_type"
                id="typeSub"
                value="SUBTRACT"
                checked={formData.adjustment_type === "SUBTRACT"}
                onChange={handleChange}
              />
              <label className="btn btn-outline-danger" htmlFor="typeSub">
                <i className="fas fa-minus-circle me-2"></i> Subtract
                (Damage/Loss)
              </label>

              <input
                type="radio"
                className="btn-check"
                name="adjustment_type"
                id="typeAdd"
                value="ADD"
                checked={formData.adjustment_type === "ADD"}
                onChange={handleChange}
              />
              <label className="btn btn-outline-success" htmlFor="typeAdd">
                <i className="fas fa-plus-circle me-2"></i> Add
                (Correction/Found)
              </label>
            </div>
          </div>

          {/* Quantity & Reason */}
          <div className="col-md-4">
            <label className="form-label">Quantity</label>
            <input
              type="number"
              name="quantity_changed"
              className="form-control"
              min="1"
              value={formData.quantity_changed}
              onChange={handleChange}
              required
              placeholder="Enter quantity"
            />
          </div>
          <div className="col-md-8">
            <label className="form-label">Reason</label>
            <textarea
              name="reason"
              className="form-control"
              rows={1}
              value={formData.reason}
              onChange={handleChange}
              required
              placeholder="e.g. Expired batch, Glass broken during transport..."
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
          <button
            type="submit"
            className={`btn ${formData.adjustment_type === "ADD" ? "btn-success" : "btn-danger"}`}
            disabled={loading}
          >
            {loading ? "Processing..." : "Confirm Adjustment"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default AdjustmentForm;
