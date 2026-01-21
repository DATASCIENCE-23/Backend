import React, { useState, useEffect } from "react";
import { createLocation, updateLocation } from "./location.api";
import type { StoreLocation, StoreLocationCreate } from "./location.types";

interface Props {
  initialData: StoreLocation | null;
  onSuccess: () => void;
  onCancel: () => void;
}

const LocationForm: React.FC<Props> = ({
  initialData,
  onSuccess,
  onCancel,
}) => {
  const [formData, setFormData] = useState<StoreLocationCreate>({
    name: "",
    location_type: "",
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (initialData) {
      setFormData({
        name: initialData.name,
        location_type: initialData.location_type || "",
      });
    }
  }, [initialData]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (initialData) {
        await updateLocation(initialData.id, formData);
      } else {
        await createLocation(formData);
      }
      onSuccess();
    } catch (err: any) {
      alert("Error saving location. Check backend.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">Location Name</label>
          <input
            className="form-control"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            placeholder="e.g. Central Pharmacy"
            required
          />
        </div>

        <div className="mb-3">
          <label className="form-label" htmlFor="location-type-select">
            Location Type
          </label>
          <select
            id="location-type-select"
            className="form-select"
            value={formData.location_type}
            onChange={(e) =>
              setFormData({ ...formData, location_type: e.target.value })
            }
          >
            <option value="">Select Type...</option>
            <option value="Main Store">Main Store</option>
            <option value="Sub Store">Sub Store</option>
            <option value="Dispensary">Dispensary</option>
            <option value="Ward Store">Ward Store</option>
          </select>
          <div className="form-text">Categorize where items are stored.</div>
        </div>

        <div className="d-flex justify-content-end gap-2 mt-4">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={onCancel}
          >
            Cancel
          </button>
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? "Saving..." : "Save Location"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default LocationForm;
