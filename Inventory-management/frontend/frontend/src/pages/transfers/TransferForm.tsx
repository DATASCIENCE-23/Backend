// src/pages/transfers/TransferForm.tsx
import React, { useState, useEffect } from "react";
import { createTransfer } from "./transfer.api";
import type { StockTransferCreate } from "./transfer.types";
import { getItems } from "../items/item.api";
import { getLocations } from "../locations/location.api";
import type { Item } from "../items/item.types";
import type { StoreLocation } from "../locations/location.types";

interface Props {
  onSuccess: () => void;
  onCancel: () => void;
}

const TransferForm: React.FC<Props> = ({ onSuccess, onCancel }) => {
  const [items, setItems] = useState<Item[]>([]);
  const [locations, setLocations] = useState<StoreLocation[]>([]);
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState<StockTransferCreate>({
    item_id: 0,
    from_location_id: 0,
    to_location_id: 0,
    quantity: 1,
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
    e: React.ChangeEvent<HTMLSelectElement | HTMLInputElement>,
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: Number(value) }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.from_location_id === formData.to_location_id) {
      alert("Source and Destination locations cannot be the same.");
      return;
    }
    if (formData.item_id === 0) {
      alert("Please select an item.");
      return;
    }

    setLoading(true);
    try {
      await createTransfer(formData);
      alert("Transfer Successful!");
      onSuccess();
    } catch (err: any) {
      alert("Error: " + (err.response?.data?.detail || "Transfer Failed"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      <div className="alert alert-warning small">
        <i className="fas fa-exclamation-triangle me-2"></i>
        Ensure the Source Location has enough stock before transferring.
      </div>
      <form onSubmit={handleSubmit}>
        <div className="row g-3">
          {/* Item Selection */}
          <div className="col-md-12">
            <label htmlFor="item_id" className="form-label fw-bold">
              Item to Transfer
            </label>
            <select
              id="item_id"
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

          {/* Locations */}
          <div className="col-md-5">
            <label htmlFor="from_location_id" className="form-label">
              From (Source)
            </label>
            <select
              id="from_location_id"
              name="from_location_id"
              className="form-select"
              value={formData.from_location_id}
              onChange={handleChange}
              required
            >
              <option value={0}>Select Source...</option>
              {locations.map((l) => (
                <option key={l.id} value={l.id}>
                  {l.name}
                </option>
              ))}
            </select>
          </div>

          <div className="col-md-2 d-flex align-items-center justify-content-center pt-4">
            <i className="fas fa-arrow-right fa-2x text-muted"></i>
          </div>

          <div className="col-md-5">
            <label className="form-label">To (Destination)</label>
            <label htmlFor="to_location_id" className="form-label">
              To (Destination)
            </label>
            <select
              id="to_location_id"
              name="to_location_id"
              className="form-select"
              value={formData.to_location_id}
              onChange={handleChange}
              required
            >
              <option value={0}>Select Destination...</option>
              {locations.map((l) => (
                <option key={l.id} value={l.id}>
                  {l.name}
                </option>
              ))}
            </select>
          </div>

          {/* Quantity */}
          <div className="col-md-4">
            <label className="form-label fw-bold">Quantity</label>
            <input
              type="number"
              name="quantity"
              className="form-control"
              min="1"
              value={formData.quantity}
              onChange={handleChange}
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
            {loading ? "Processing..." : "Transfer Stock"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default TransferForm;
