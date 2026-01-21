// src/components/PageLayout.tsx
import React from 'react';
import type { ReactNode } from 'react';

interface PageLayoutProps {
  title: string;
  actionLabel?: string;       // Text for the button (e.g., "Add Doctor")
  onAction?: () => void;      // Function to run when button is clicked
  children: ReactNode;        // The Table or Form goes here
}

const PageLayout: React.FC<PageLayoutProps> = ({ title, actionLabel, onAction, children }) => {
  return (
    <div className="container-fluid p-4">
      
      {/* 1. Standard Header Section */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h3 className="mb-0 fw-bold text-dark">{title}</h3>
          <p className="text-muted small mb-0">Manage your hospital {title.toLowerCase()} here.</p>
        </div>
        
        {/* Optional "Add New" Button */}
        {actionLabel && onAction && (
          <button className="btn btn-primary shadow-sm" onClick={onAction}>
            <i className="fas fa-plus me-2"></i> {actionLabel}
          </button>
        )}
      </div>

      {/* 2. Consistent White Card for Content */}
      <div className="card shadow-sm border-0" style={{ borderRadius: '12px', overflow: 'hidden' }}>
        <div className="card-body p-0">
          {children}
        </div>
      </div>

    </div>
  );
};

export default PageLayout;