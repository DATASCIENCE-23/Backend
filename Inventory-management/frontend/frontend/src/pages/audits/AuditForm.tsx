// src/pages/audits/AuditForm.tsx
import React, { useState, useEffect } from "react";
import { createAudit } from "./audit.api";
import type { AuditItem } from "./audit.types";
import { getLocations } from "../locations/location.api";
import { getItems } from "../items/item.api";
import type { StoreLocation } from "../locations/location.types";
import type { Item } from "../items/item.types";

interface Props {
  onSuccess: () => void;
  onCancel: () => void;
}

const AuditForm: React.FC<Props> = ({ onSuccess, onCancel }) => {
  const [locations, setLocations] = useState<StoreLocation[]>([]);
  const [itemsList, setItemsList] = useState<Item[]>([]);

  const [locationId, setLocationId] = useState<number | "">("");
  const [remarks, setRemarks] = useState("");
  const [cart, setCart] = useState<AuditItem[]>([
    { item_id: 0, physical_quantity: 0 },
  ]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    Promise.all([getLocations(), getItems()])
      .then(([locData, itemData]) => {
        setLocations(locData);
        setItemsList(itemData);
      })
      .catch(console.error);
  }, []);

  const updateRow = (index: number, field: keyof AuditItem, value: number) => {
    const newCart = [...cart];
    newCart[index] = { ...newCart[index], [field]: value };
    setCart(newCart);
  };

  const addRow = () => setCart([...cart, { item_id: 0, physical_quantity: 0 }]);

  const removeRow = (index: number) => {
    if (cart.length > 1) setCart(cart.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!locationId) {
      alert("Please select a location");
      return;
    }

    const validItems = cart.filter((i) => i.item_id > 0);
    if (validItems.length === 0) {
      alert("Please add at least one item to audit");
      return;
    }

    setLoading(true);
    try {
      await createAudit({
        location_id: Number(locationId),
        remarks: remarks,
        items: validItems,
      });
      alert("Audit Completed. Stock Updated!");
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
        <div className="row g-3 mb-4">
          <div className="col-md-6">
            <label
              htmlFor="audit-location-select"
              className="form-label fw-bold"
            >
              Store Location
            </label>
            <select
              id="audit-location-select"
              className="form-select"
              value={locationId}
              onChange={(e) => setLocationId(Number(e.target.value))}
              required
            >
              <option value="">Select Location...</option>
              {locations.map((l) => (
                <option key={l.id} value={l.id}>
                  {l.name}
                </option>
              ))}
            </select>
          </div>
          <div className="col-md-6">
            <label className="form-label fw-bold">Remarks</label>
            <input
              className="form-control"
              value={remarks}
              onChange={(e) => setRemarks(e.target.value)}
              placeholder="e.g. Annual Audit 2026"
            />
          </div>
        </div>

        <h5 className="mb-3 text-secondary">Physical Counts</h5>
        <div className="table-responsive mb-3">
          <table className="table table-bordered align-middle">
            <thead className="table-light">
              <tr>
                <th style={{ width: "60%" }}>Item</th>
                <th style={{ width: "30%" }}>Physical Qty (Counted)</th>
                <th style={{ width: "10%" }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {cart.map((row, index) => (
                <tr key={index}>
                  <td>
                    <select
                      className="form-select"
                      value={row.item_id}
                      onChange={(e) =>
                        updateRow(index, "item_id", Number(e.target.value))
                      }
                      aria-label="Select Item"
                    >
                      <option value={0}>Select Item...</option>
                      {itemsList.map((i) => (
                        <option key={i.id} value={i.id}>
                          {i.name} ({i.code})
                        </option>
                      ))}
                    </select>
                  </td>
                  <td>
                    <input
                      type="number"
                      className="form-control"
                      value={row.physical_quantity}
                      onChange={(e) =>
                        updateRow(
                          index,
                          "physical_quantity",
                          Number(e.target.value),
                        )
                      }
                      min="0"
                      placeholder="Enter counted quantity"
                    />
                  </td>
                  <td className="text-center">
                    {cart.length > 1 && (
                      <button
                        type="button"
                        className="btn btn-sm btn-outline-danger"
                        onClick={() => removeRow(index)}
                        title="Remove Item Row"
                      >
                        <i className="fas fa-trash"></i>
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <button
          type="button"
          className="btn btn-sm btn-outline-primary mb-4"
          onClick={addRow}
        >
          <i className="fas fa-plus"></i> Add Item Row
        </button>

        <div className="d-flex justify-content-end gap-2 border-top pt-3">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={onCancel}
          >
            Cancel
          </button>
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? "Processing..." : "Submit Audit"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default AuditForm;
