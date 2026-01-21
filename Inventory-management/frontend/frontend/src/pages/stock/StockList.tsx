// src/pages/stock/StockList.tsx
import React, { useEffect, useState } from "react";
import { getStocks, deleteStock } from "./stock.api";
import type { Stock } from "./stock.types";
import { getItems } from "../items/item.api";
import { getLocations } from "../locations/location.api";
import type { Item } from "../items/item.types";
import type { StoreLocation } from "../locations/location.types";
import PageLayout from "../../components/PageLayout";
import StockForm from "./StockForm";

const StockList: React.FC = () => {
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [items, setItems] = useState<Item[]>([]);
  const [locations, setLocations] = useState<StoreLocation[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [editingStock, setEditingStock] = useState<Stock | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      // Fetch all data in parallel
      const [stockData, itemsData, locsData] = await Promise.all([
        getStocks(),
        getItems(),
        getLocations(),
      ]);
      setStocks(stockData);
      setItems(itemsData);
      setLocations(locsData);
    } catch (e) {
      console.error(e);
    }
  };

  const handleDelete = async (id: number) => {
    if (confirm("Are you sure you want to delete this stock record?")) {
      await deleteStock(id);
      loadData();
    }
  };

  // Helper to find names
  const getItemName = (id: number) =>
    items.find((i) => i.id === id)?.name || `Item #${id}`;
  const getLocName = (id: number) =>
    locations.find((l) => l.id === id)?.name || `Loc #${id}`;

  if (showForm) {
    return (
      <PageLayout title={editingStock ? "Edit Stock Level" : "Add Stock"}>
        <StockForm
          initialData={editingStock}
          onSuccess={() => {
            setShowForm(false);
            loadData();
          }}
          onCancel={() => setShowForm(false)}
        />
      </PageLayout>
    );
  }

  return (
    <PageLayout
      title="Current Stock Levels"
      actionLabel="Add Stock"
      onAction={() => {
        setEditingStock(null);
        setShowForm(true);
      }}
    >
      <div className="table-responsive">
        <table className="table table-hover align-middle mb-0">
          <thead className="bg-light text-secondary">
            <tr>
              <th className="ps-4">Item Name</th>
              <th>Location</th>
              <th>Quantity</th>
              <th>Last Updated</th>
              <th className="text-end pe-4">Actions</th>
            </tr>
          </thead>
          <tbody>
            {stocks.length === 0 ? (
              <tr>
                <td colSpan={5} className="text-center py-4">
                  No stock records found.
                </td>
              </tr>
            ) : (
              stocks.map((stock) => (
                <tr key={stock.id}>
                  <td className="ps-4 fw-bold text-primary">
                    {getItemName(stock.item_id)}
                  </td>
                  <td>
                    <span className="badge bg-light text-dark border">
                      <i className="fas fa-map-marker-alt me-1 text-muted"></i>
                      {getLocName(stock.location_id)}
                    </span>
                  </td>
                  <td>
                    <span
                      className={`badge ${stock.quantity_available < 10 ? "bg-danger" : "bg-success"}`}
                      style={{ fontSize: "0.9rem" }}
                    >
                      {stock.quantity_available}
                    </span>
                  </td>
                  <td className="text-muted small">
                    {new Date(stock.last_updated).toLocaleDateString()}
                  </td>
                  <td className="text-end pe-4">
                    {/* <button
                      className="btn btn-sm btn-light text-primary me-2"
                      onClick={() => {
                        setEditingStock(stock);
                        setShowForm(true);
                      }}
                      title="Edit Stock"
                      aria-label="Edit Stock"
                    >
                      <i className="fas fa-edit"></i>
                    </button> */}
                    <button
                      className="btn btn-sm btn-light text-danger"
                      onClick={() => handleDelete(stock.id)}
                      title="Delete Stock"
                      aria-label="Delete Stock"
                    >
                      <i className="fas fa-trash"></i>
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </PageLayout>
  );
};

export default StockList;
