// pages/category/category.types.ts

// What we get FROM the backend (Database structure)
export interface Category {
  category_id: number;
  category_name: string;
  description: string | null;
}

// What we send TO the backend (Pydantic Schema structure)
export interface CategoryCreate {
  name: string;        // The backend schema expects "name", not "category_name"
  description: string;
}

export interface CategoryUpdate {
  name?: string;
  description?: string;
}