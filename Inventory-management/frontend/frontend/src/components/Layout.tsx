// src/components/Layout.tsx
import React from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';

const Layout: React.FC = () => {
  const location = useLocation();
  const isActive = (path: string) => location.pathname === path ? 'active' : '';

  return (
    <div className="d-flex" style={{ minHeight: '100vh' }}>
      
      {/* Modern Dark Sidebar */}
      <div className="d-flex flex-column p-3 text-white" 
           style={{ width: '260px', backgroundColor: '#0f172a', position: 'fixed', height: '100vh', zIndex: 1000 }}>
        
        {/* Logo Area */}
        <div className="mb-4 px-2 py-3 d-flex align-items-center border-bottom border-secondary">
          <div className="bg-primary rounded-circle d-flex align-items-center justify-content-center me-3" style={{width: 40, height: 40}}>
            <i className="fas fa-heartbeat text-white"></i>
          </div>
          
        </div>

        {/* Navigation */}
        <ul className="nav nav-pills flex-column mb-auto">
          <li className="nav-item">
            <Link to="/" className={`nav-link ${isActive('/')}`}>
              <i className="fas fa-th-large"></i> Dashboard
            </Link>
          </li>
          <li>
            <Link to="/categories" className={`nav-link ${isActive('/categories')}`}>
              <i className="fas fa-boxes"></i> Categories
            </Link>
          </li>
        <li>
            <Link to="/issues" className={`nav-link ${isActive('/issues')}`}>
              <i className="fas fa-hand-holding-medical"></i> Issues
        </Link>
        </li>
          <li>
            <Link to="/items" className={`nav-link ${isActive('/items')}`}>
              <i className="fas fa-pills"></i> Items
            </Link>
          </li>
          <li>
            <Link to="/purchases" className={`nav-link ${isActive('/purchases')}`}>
              <i className="fas fa-shopping-cart"></i> Purchases
            </Link>
          </li>
          <li>
            <Link to = "/stock" className={`nav-link ${isActive('/stock')}`}>
              <i className="fas fa-warehouse"></i> Stock Management
            </Link>
          </li>
          <li>
            <Link to="/adjustments" className={`nav-link ${isActive('/adjustments')}`}>
              <i className="fas fa-sliders-h"></i> Adjustments
            </Link>
          </li>
          <li>
            <Link to="/audits" className={`nav-link ${isActive('/audits')}`}>
              <i className="fas fa-clipboard-check"></i> Stock Audits
            </Link>
          </li>
          <li>
            <Link to="/transfers" className={`nav-link ${isActive('/transfers')}`}>
              <i className="fas fa-exchange-alt"></i> Stock Transfers
            </Link>
          </li>

          <li>
            <Link to="/locations" className={`nav-link ${isActive('/locations')}`}>
                <i className="fas fa-map-marker-alt"></i> Store Locations
            </Link>
          </li>

          <li>
            <Link to = "/suppliers" className={`nav-link ${isActive('/suppliers')}`}>
              <i className="fas fa-truck"></i> Suppliers
            </Link>
          </li>
        </ul>

        {/* User Profile at Bottom */}
        {/* <div className="mt-auto pt-3 border-top border-secondary">
          <div className="d-flex align-items-center px-2">
            <img src="https://ui-avatars.com/api/?name=Admin+User&background=random" alt="" width="32" height="32" className="rounded-circle me-2"/>
            <div>
              <strong className="d-block" style={{fontSize: '0.9rem'}}>Dr. Admin</strong>
            </div>
          </div>
        </div> */}
      </div>

      {/* Main Content Wrapper */}
      <div className="flex-grow-1" style={{ marginLeft: '260px' }}>
        {/* Top Header */}
        <header className="bg-white shadow-sm border-bottom py-3 px-4 d-flex justify-content-between align-items-center sticky-top">
          <h5 className="mb-0 text-dark fw-bold text-capitalize">
            {location.pathname === '/' ? 'Dashboard' : location.pathname.replace('/', '')}
          </h5>
          <div className="d-flex gap-3">
          </div>
        </header>

        {/* Page Content */}
        <div className="p-4">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default Layout;