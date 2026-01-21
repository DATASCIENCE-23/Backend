import React, { useState, useEffect } from "react";
import { createPurchase } from "./purchase.api";
import type { PurchaseItem } from "./purchase.types";
import { getSuppliers } from "../suppliers/supplier.api";
import { getItems } from "../items/item.api";
import type { Supplier } from "../suppliers/supplier.types";
import type { Item } from "../items/item.types";

interface Props {
  onSuccess: () => void;
  onCancel: () => void;
}

const PurchaseForm: React.FC<Props> = ({ onSuccess, onCancel }) => {
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [itemsList, setItemsList] = useState<Item[]>([]);

  const [supplierId, setSupplierId] = useState<number | "">("");
  const [invoiceNo, setInvoiceNo] = useState("");
  const [cart, setCart] = useState<PurchaseItem[]>([
    { item_id: 0, quantity: 1, purchase_price: 0 },
  ]);
  const [loading, setLoading] = useState(false);

  // Load Data for Dropdowns
  useEffect(() => {
    Promise.all([getSuppliers(), getItems()])
      .then(([supData, itemData]) => {
        setSuppliers(supData);
        setItemsList(itemData);
      })
      .catch(console.error);
  }, []);

  // Cart Management
  const updateRow = (
    index: number,
    field: keyof PurchaseItem,
    value: number,
  ) => {
    const newCart = [...cart];
    newCart[index] = { ...newCart[index], [field]: value };
    setCart(newCart);
  };

  const addRow = () =>
    setCart([...cart, { item_id: 0, quantity: 1, purchase_price: 0 }]);

  const removeRow = (index: number) => {
    if (cart.length > 1) setCart(cart.filter((_, i) => i !== index));
  };

  // Calculate Total
  const grandTotal = cart.reduce(
    (sum, item) => sum + item.quantity * item.purchase_price,
    0,
  );

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!supplierId || !invoiceNo) {
      alert("Please fill supplier and invoice details");
      return;
    }

    // Filter invalid rows
    const validItems = cart.filter((i) => i.item_id > 0 && i.quantity > 0);
    if (validItems.length === 0) {
      alert("Add at least one item");
      return;
    }

    setLoading(true);
    try {
      await createPurchase({
        supplier_id: Number(supplierId),
        invoice_number: invoiceNo,
        items: validItems,
      });
      alert("Purchase Recorded & Stock Updated!");
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
        {/* Header Details */}
        <div className="row g-3 mb-4 border-bottom pb-4">
          <div className="col-md-6">
            <label htmlFor="supplier-select" className="form-label fw-bold">
              Supplier
            </label>
            <select
              id="supplier-select"
              className="form-select"
              value={supplierId}
              onChange={(e) => setSupplierId(Number(e.target.value))}
              required
            >
              <option value="">Select Supplier...</option>
              {suppliers.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name}
                </option>
              ))}
            </select>
          </div>
          <div className="col-md-6">
            <label className="form-label fw-bold">Invoice Number</label>
            <input
              className="form-control"
              value={invoiceNo}
              onChange={(e) => setInvoiceNo(e.target.value)}
              required
              placeholder="e.g. INV-2026-001"
            />
          </div>
        </div>

        {/* Dynamic Items Table */}
        <h5 className="mb-3 text-secondary">Items</h5>
        <div className="table-responsive mb-3">
          <table className="table table-bordered align-middle">
            <thead className="table-light">
              <tr>
                <th style={{ width: "40%" }}>Item Name</th>
                <th style={{ width: "15%" }}>Qty</th>
                <th style={{ width: "20%" }}>Unit Price</th>
                <th style={{ width: "15%" }}>Total</th>
                <th style={{ width: "10%" }}>Action</th>
              </tr>
            </thead>
            <tbody>
              {cart.map((row, index) => (
                <tr key={index}>
                  <td>
                    <select
                      className="form-select form-select-sm"
                      value={row.item_id}
                      onChange={(e) =>
                        updateRow(index, "item_id", Number(e.target.value))
                      }
                      aria-label="Select item"
                    >
                      <option value={0}>Select Item...</option>
                      {itemsList.map((i) => (
                        <option key={i.id} value={i.id}>
                          {i.name} ({i.unit})
                        </option>
                      ))}
                    </select>
                  </td>
                  <td>
                    <input
                      type="number"
                      className="form-control form-control-sm"
                      value={row.quantity}
                      onChange={(e) =>
                        updateRow(index, "quantity", Number(e.target.value))
                      }
                      min="1"
                      placeholder="Quantity"
                    />
                  </td>
                  <td>
                    <input
                      type="number"
                      className="form-control form-control-sm"
                      value={row.purchase_price}
                      onChange={(e) =>
                        updateRow(
                          index,
                          "purchase_price",
                          Number(e.target.value),
                        )
                      }
                      min="0"
                      step="0.01"
                      placeholder="Unit Price"
                      title="Enter unit price"
                    />
                  </td>
                  <td className="text-end fw-bold text-muted">
                    ${(row.quantity * row.purchase_price).toFixed(2)}
                  </td>
                  <td className="text-center">
                    {cart.length > 1 && (
                      <button
                        type="button"
                        className="btn btn-sm btn-outline-danger"
                        onClick={() => removeRow(index)}
                        title="Remove item"
                        aria-label="Remove item"
                      >
                        <i className="fas fa-trash" aria-hidden="true"></i>
                        <span className="visually-hidden">Remove item</span>
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

        {/* Footer & Totals */}
        <div className="d-flex justify-content-between align-items-center border-top pt-3">
          <div className="fs-4 fw-bold text-dark">
            Grand Total:{" "}
            <span className="text-primary">${grandTotal.toFixed(2)}</span>
          </div>
          <div className="d-flex gap-2">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={onCancel}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn btn-success px-4"
              disabled={loading}
            >
              {loading ? "Processing..." : "Confirm Purchase"}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default PurchaseForm;
