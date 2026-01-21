import React, { useState, useEffect } from "react";
import { createIssue } from "./issue.api";
import type { IssueItem } from "./issue.types";
import { getItems } from "../items/item.api";
import type { Item } from "../items/item.types";

interface Props {
  onSuccess: () => void;
  onCancel: () => void;
}

const IssueForm: React.FC<Props> = ({ onSuccess, onCancel }) => {
  const [itemsList, setItemsList] = useState<Item[]>([]);
  const [loading, setLoading] = useState(false);

  // Form State
  const [deptId, setDeptId] = useState<number | "">("");
  const [cart, setCart] = useState<IssueItem[]>([{ item_id: 0, quantity: 1 }]);

  useEffect(() => {
    getItems().then(setItemsList).catch(console.error);
  }, []);

  const updateRow = (index: number, field: keyof IssueItem, value: number) => {
    const newCart = [...cart];
    newCart[index] = { ...newCart[index], [field]: value };
    setCart(newCart);
  };

  const addRow = () => setCart([...cart, { item_id: 0, quantity: 1 }]);

  const removeRow = (index: number) => {
    if (cart.length > 1) setCart(cart.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!deptId) {
      alert("Please Enter Department ID");
      return;
    }

    const validItems = cart.filter((i) => i.item_id > 0 && i.quantity > 0);
    if (validItems.length === 0) {
      alert("Please add at least one item.");
      return;
    }

    setLoading(true);
    try {
      await createIssue({
        department_id: Number(deptId),
        items: validItems,
      });
      alert("Issue Approved & Stock Deducted!");
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
        {/* Department */}
        <div className="mb-4">
          <label className="form-label fw-bold">Department ID</label>
          <input
            type="number"
            className="form-control"
            style={{ maxWidth: "200px" }}
            value={deptId}
            onChange={(e) => setDeptId(Number(e.target.value))}
            required
            placeholder="e.g. 101"
          />
          <div className="form-text">
            Enter the ID of the department requesting items.
          </div>
        </div>

        {/* Items Table */}
        <h5 className="mb-3 text-secondary">Items to Issue</h5>
        <div className="table-responsive mb-3">
          <table className="table table-bordered align-middle">
            <thead className="table-light">
              <tr>
                <th style={{ width: "60%" }}>Item</th>
                <th style={{ width: "30%" }}>Quantity</th>
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
                      aria-label="Select item to issue"
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
                      value={row.quantity}
                      onChange={(e) =>
                        updateRow(index, "quantity", Number(e.target.value))
                      }
                      min="1"
                      placeholder="Enter quantity"
                      title="Quantity"
                    />
                  </td>
                  <td className="text-center">
                    {cart.length > 1 && (
                      <button
                        type="button"
                        className="btn btn-sm btn-outline-danger"
                        onClick={() => removeRow(index)}
                        title="Remove item"
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
          <i className="fas fa-plus"></i> Add Another Item
        </button>

        <div className="d-flex justify-content-end gap-2 border-top pt-3">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={onCancel}
          >
            Cancel
          </button>
          <button type="submit" className="btn btn-success" disabled={loading}>
            {loading ? "Processing..." : "Approve Issue"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default IssueForm;
