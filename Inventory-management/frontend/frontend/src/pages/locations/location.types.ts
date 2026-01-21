export interface StoreLocation {
  id: number;
  name: string;
  location_type: string;
}

export interface StoreLocationCreate {
  name: string;
  location_type: string;
}