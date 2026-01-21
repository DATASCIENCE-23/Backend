// src/routes/AppRoutes.tsx
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from '../components/Layout';

import CategoryList from '../pages/category/CategoryList';
import IssueList from '../pages/issues/IssueList';
import ItemList from '../pages/items/ItemList';
import LocationList from '../pages/locations/LocationList';
import SupplierList from '../pages/suppliers/SupplierList';
import StockList from '../pages/stock/StockList';
import PurchaseList from '../pages/purchases/PurchaseList';
import AdjustmentList from '../pages/stock_adjustments/AdjustmentList';
import AuditList from '../pages/audits/AuditList';
import TransferList from '../pages/transfers/TransferList';


const AppRoutes: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        {/* The Layout wraps all these routes */}
        <Route path="/" element={<Layout />}>
          <Route path="categories" element={<CategoryList />} />
          <Route path="issues" element={<IssueList />} />
          <Route path="items" element={<ItemList />} />
          <Route path="purchases" element={<PurchaseList />} />
          <Route path="stock" element={<StockList />} />
          <Route path="adjustments" element={<AdjustmentList />} />
          <Route path="audits" element={<AuditList />} />
          <Route path="transfers" element={<TransferList />} />  
          <Route path = "locations" element={<LocationList />} />
          <Route path = "suppliers" element={<SupplierList />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default AppRoutes;