import React, { useEffect, useState } from "react";
import { getLocations, deleteLocation } from "./location.api";
import type { StoreLocation } from "./location.types";
import PageLayout from "../../components/PageLayout";
import LocationForm from "./LocationForm";

const LocationList: React.FC = () => {
  const [locations, setLocations] = useState<StoreLocation[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [editingLoc, setEditingLoc] = useState<StoreLocation | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const data = await getLocations();
      setLocations(data);
    } catch (e) {
      console.error(e);
    }
  };

  const handleDelete = async (id: number) => {
    if (confirm("Delete this location?")) {
      await deleteLocation(id);
      loadData();
    }
  };

  if (showForm) {
    return (
      <PageLayout title={editingLoc ? "Edit Location" : "Add Store Location"}>
        <LocationForm
          initialData={editingLoc}
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
      title="Store Locations"
      actionLabel="Add Location"
      onAction={() => {
        setEditingLoc(null);
        setShowForm(true);
      }}
    >
      <div className="table-responsive">
        <table className="table table-hover align-middle mb-0">
          <thead className="bg-light text-secondary">
            <tr>
              <th className="ps-4">ID</th>
              <th>Name</th>
              <th>Type</th>
              <th className="text-end pe-4">Actions</th>
            </tr>
          </thead>
          <tbody>
            {locations.length === 0 ? (
              <tr>
                <td colSpan={4} className="text-center py-4">
                  No locations defined.
                </td>
              </tr>
            ) : (
              locations.map((loc) => (
                <tr key={loc.id}>
                  <td className="ps-4 fw-bold">#{loc.id}</td>
                  <td>{loc.name}</td>
                  <td>
                    <span className="badge bg-secondary">
                      {loc.location_type || "General"}
                    </span>
                  </td>
                  <td className="text-end pe-4">
                    <button
                      className="btn btn-sm btn-light text-primary me-2"
                      onClick={() => {
                        setEditingLoc(loc);
                        setShowForm(true);
                      }}
                      title="Edit Location"
                      aria-label="Edit Location"
                    >
                      <i className="fas fa-edit"></i>
                    </button>
                    <button
                      className="btn btn-sm btn-light text-danger"
                      onClick={() => handleDelete(loc.id)}
                      title="Delete Location"
                      aria-label="Delete Location"
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

export default LocationList;
