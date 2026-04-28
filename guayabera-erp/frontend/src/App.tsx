import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { RootState } from './store';

// Layouts
import MainLayout from './components/layouts/MainLayout';

// Pages
import LoginPage from './components/pages/auth/LoginPage';
import DashboardPage from './components/pages/DashboardPage';

// Admin Pages
import EmpresaPage from './components/pages/admin/EmpresaPage';

// Finance Pages
import CuentasPage from './components/pages/finance/CuentasPage';
import PolizasPage from './components/pages/finance/PolizasPage';
import BancosPage from './components/pages/finance/BancosPage';
import BalanzaPage from './components/pages/finance/BalanzaPage';
import AsientosAutomaticosPage from './components/pages/finance/AsientosAutomaticosPage';

// Production Page
import ProductionDashboard from './components/pages/production/ProductionDashboard';

// Sales Page
import SalesDashboard from './components/pages/sales/SalesDashboard';

// Inventory Page
import InventoryDashboard from './components/pages/inventory/InventoryDashboard';
import TomaInventario from './components/pages/inventory/TomaInventario';

// HR Page
import HRDashboard from './components/pages/hr/HRDashboard';
import HRDashboardNewFeatures from './components/pages/hr/HRDashboardNewFeatures';

// Supply Chain Page
import SupplyChainDashboard from './components/pages/supply_chain/SupplyChainDashboard';

// Invoice Page
import InvoiceDashboard from './components/pages/invoice/InvoiceDashboard';

// Payroll Page
import PayrollDashboard from './components/pages/payroll/PayrollDashboard';

// Agents Page
import AgentsDashboard from './components/pages/agents/AgentsDashboard';

// Purchases Page
import PurchasesDashboard from './components/pages/purchases/PurchasesDashboard';

// CAD Page
import CADDashboard from './components/pages/cad/CADDashboard';

// Size Chart Page
import SizeChartDashboard from './components/pages/sizechart/SizeChartDashboard';

// Helpdesk Page
import HelpdeskDashboard from './components/pages/helpdesk/HelpdeskDashboard';

// Requisitions Page
import RequisitionsDashboard from './components/pages/requisitions/RequisitionsDashboard';

// Notifications Page
import NotificationsDashboard from './components/pages/notifications/NotificationsDashboard';

// Quality Control Page
import QualityControlDashboard from './components/pages/qualitycontrol/QualityControlDashboard';

// Advanced Accounting Page
import AdvancedAccountingDashboard from './components/pages/advancedaccounting/AdvancedAccountingDashboard';

// Logistics Page
import LogisticsDashboard from './components/pages/logistics/LogisticsDashboard';

// CRM Page
import CrmDashboard from './components/pages/crm/CrmDashboard';

// Project Management Page
import ProjectManagementDashboard from './components/pages/projectmanagement/ProjectManagementDashboard';

// Asset Management Page
import AssetManagementDashboard from './components/pages/assetmanagement/AssetManagementDashboard';

// Business Intelligence Page
import BusinessIntelligenceDashboard from './components/pages/businessintelligence/BusinessIntelligenceDashboard';

// Reports Page
import ReportsDashboard from './components/pages/reports/ReportsDashboard';

// Permissions Page
import PermissionsDashboard from './components/pages/permissions/PermissionsDashboard';

// Settings Page
import SystemSettings from './components/pages/settings/SystemSettings';

// Protected Route Component
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const isAuthenticated = useSelector((state: RootState) => state.auth.isAuthenticated);
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return <>{children}</>;
};

const App: React.FC = () => {
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/login" element={<LoginPage />} />
      
      {/* Protected routes */}
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <MainLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<DashboardPage />} />
        
        {/* Admin */}
        <Route path="admin/empresa" element={<EmpresaPage />} />
        
        {/* Finance */}
        <Route path="finance/cuentas" element={<CuentasPage />} />
        <Route path="finance/polizas" element={<PolizasPage />} />
        <Route path="finance/bancos" element={<BancosPage />} />
        <Route path="finance/balanza" element={<BalanzaPage />} />
        <Route path="finance/asientos-automaticos" element={<AsientosAutomaticosPage />} />
        
        {/* Production */}
        <Route path="production" element={<ProductionDashboard />} />
        
        {/* Sales */}
        <Route path="sales" element={<SalesDashboard />} />
        
        {/* Inventory */}
        <Route path="inventory" element={<InventoryDashboard />} />
        <Route path="inventory/toma-inventario" element={<TomaInventario />} />
        
        {/* HR */}
        <Route path="hr" element={<HRDashboard />} />
        <Route path="hr/anuncios-vacaciones" element={<HRDashboardNewFeatures />} />
        
        {/* Supply Chain */}
        <Route path="supply-chain" element={<SupplyChainDashboard />} />
        
        {/* Invoice */}
        <Route path="invoice" element={<InvoiceDashboard />} />
        
        {/* Payroll */}
        <Route path="payroll" element={<PayrollDashboard />} />
        
        {/* Agents */}
        <Route path="agents" element={<AgentsDashboard />} />
        
        {/* Purchases */}
        <Route path="purchases" element={<PurchasesDashboard />} />
        
        {/* CAD */}
        <Route path="cad" element={<CADDashboard />} />
        
        {/* Size Chart */}
        <Route path="size-chart" element={<SizeChartDashboard />} />
        
        {/* Helpdesk */}
        <Route path="helpdesk" element={<HelpdeskDashboard />} />
        
        {/* Requisitions */}
        <Route path="requisitions" element={<RequisitionsDashboard />} />
        
        {/* Notifications */}
        <Route path="notifications" element={<NotificationsDashboard />} />
        
        {/* Quality Control */}
        <Route path="quality-control" element={<QualityControlDashboard />} />
        
        {/* Advanced Accounting */}
        <Route path="advanced-accounting" element={<AdvancedAccountingDashboard />} />
        
        {/* Logistics */}
        <Route path="logistics" element={<LogisticsDashboard />} />
        
        {/* CRM */}
        <Route path="crm" element={<CrmDashboard />} />
        
        {/* Project Management */}
        <Route path="project-management" element={<ProjectManagementDashboard />} />
        
        {/* Asset Management */}
        <Route path="asset-management" element={<AssetManagementDashboard />} />
        
        {/* Business Intelligence */}
        <Route path="business-intelligence" element={<BusinessIntelligenceDashboard />} />
        
        {/* Reports */}
        <Route path="reports" element={<ReportsDashboard />} />
        
        {/* Permissions */}
        <Route path="permissions" element={<PermissionsDashboard />} />
        
        {/* Settings */}
        <Route path="settings" element={<SystemSettings />} />
      </Route>
      
      {/* Catch all */}
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
};

export default App;