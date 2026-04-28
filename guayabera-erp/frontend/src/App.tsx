import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { RootState } from './store';

// Layouts
import MainLayout from './components/layouts/MainLayout';

// Pages
import LoginPage from './components/pages/auth/LoginPage';
import DashboardPage from './components/pages/DashboardPage';
import ExecutiveDashboard from './components/pages/ExecutiveDashboard';

// Admin Pages
import EmpresaPage from './components/pages/admin/EmpresaPage';
import WorkflowManagement from './components/pages/admin/WorkflowManagement';

// Finance Pages
import CuentasPage from './components/pages/finance/CuentasPage';
import PolizasPage from './components/pages/finance/PolizasPage';
import BancosPage from './components/pages/finance/BancosPage';
import BalanzaPage from './components/pages/finance/BalanzaPage';
import AsientosAutomaticosPage from './components/pages/finance/AsientosAutomaticosPage';
import BankIntegration from './components/pages/finance/BankIntegration';
import CollaborativeBudgeting from './components/pages/finance/CollaborativeBudgeting';
import AutoClassification from './components/pages/finance/AutoClassification';

// Production Page
import ProductionDashboard from './components/pages/production/ProductionDashboard';
import MRPManagement from './components/pages/production/MRPManagement';

// Sales Page
import SalesDashboard from './components/pages/sales/SalesDashboard';
import ClientLevelPricing from './components/pages/sales/ClientLevelPricing';
import AdvancePaymentOrders from './components/pages/sales/AdvancePaymentOrders';
import CreditNotes from './components/pages/sales/CreditNotes';

// Inventory Page
import InventoryDashboard from './components/pages/inventory/InventoryDashboard';
import TomaInventario from './components/pages/inventory/TomaInventario';
import ProductVariants from './components/pages/inventory/ProductVariants';
import QRScanner from './components/pages/inventory/QRScanner';

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
import CADAgents from './components/pages/cad/CADAgents';

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
import TransitInventory from './components/pages/logistics/TransitInventory';

// CRM Page
import CrmDashboard from './components/pages/crm/CrmDashboard';

// Project Management Page
import ProjectManagementDashboard from './components/pages/projectmanagement/ProjectManagementDashboard';

// Asset Management Page
import AssetManagementDashboard from './components/pages/assetmanagement/AssetManagementDashboard';

// Business Intelligence Pages
import BusinessIntelligenceDashboard from './components/pages/businessintelligence/BusinessIntelligenceDashboard';
import KPIMgmt from './components/pages/businessintelligence/KPIMgmt';
import PredictiveAnalysis from './components/pages/businessintelligence/PredictiveAnalysis';
import SensitivityAnalysis from './components/pages/businessintelligence/SensitivityAnalysis';
import DeviationAnalysis from './components/pages/businessintelligence/DeviationAnalysis';

// Reports Page
import ReportsDashboard from './components/pages/reports/ReportsDashboard';
import CustomReports from './components/pages/reports/CustomReports';

// Permissions Page
import PermissionsDashboard from './components/pages/permissions/PermissionsDashboard';

// Settings Page
import SystemSettings from './components/pages/settings/SystemSettings';
import ThemeSettings from './components/pages/settings/ThemeSettings';
import LanguageSettings from './components/pages/settings/LanguageSettings';

// AI Assistant Page
import AIAssistant from './components/pages/ai/AIAssistant';

// Printing Agents Page
import PrintingAgents from './components/pages/printing/PrintingAgents';

// Security Pages
import FraudDetection from './components/pages/security/FraudDetection';
import SecurityAudit from './components/pages/security/SecurityAudit';
import DataEncryption from './components/pages/security/DataEncryption';

// Maintenance Page
import MaintenancePlanning from './components/pages/maintenance/MaintenancePlanning';

// Document Management
import VersionControl from './components/pages/documents/VersionControl';
import ElectronicSignatures from './components/pages/documents/ElectronicSignatures';

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
        <Route path="executive-dashboard" element={<ExecutiveDashboard />} />
        
        {/* Admin */}
        <Route path="admin/empresa" element={<EmpresaPage />} />
        <Route path="admin/workflow-management" element={<WorkflowManagement />} />
        
        {/* Finance */}
        <Route path="finance/cuentas" element={<CuentasPage />} />
        <Route path="finance/polizas" element={<PolizasPage />} />
        <Route path="finance/bancos" element={<BancosPage />} />
        <Route path="finance/balanza" element={<BalanzaPage />} />
        <Route path="finance/asientos-automaticos" element={<AsientosAutomaticosPage />} />
        <Route path="finance/bank-integration" element={<BankIntegration />} />
        <Route path="finance/collaborative-budgeting" element={<CollaborativeBudgeting />} />
        <Route path="finance/auto-classification" element={<AutoClassification />} />
        
        {/* Production */}
        <Route path="production" element={<ProductionDashboard />} />
        <Route path="production/mrp-management" element={<MRPManagement />} />
        
        {/* Sales */}
        <Route path="sales" element={<SalesDashboard />} />
        <Route path="sales/client-level-pricing" element={<ClientLevelPricing />} />
        <Route path="sales/advance-payment-orders" element={<AdvancePaymentOrders />} />
        <Route path="sales/credit-notes" element={<CreditNotes />} />
        
        {/* Inventory */}
        <Route path="inventory" element={<InventoryDashboard />} />
        <Route path="inventory/toma-inventario" element={<TomaInventario />} />
        <Route path="inventory/product-variants" element={<ProductVariants />} />
        <Route path="inventory/qr-scanner" element={<QRScanner />} />
        
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
        <Route path="cad/agents" element={<CADAgents />} />
        
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
        <Route path="logistics/transit-inventory" element={<TransitInventory />} />
        
        {/* CRM */}
        <Route path="crm" element={<CrmDashboard />} />
        
        {/* Project Management */}
        <Route path="project-management" element={<ProjectManagementDashboard />} />
        
        {/* Asset Management */}
        <Route path="asset-management" element={<AssetManagementDashboard />} />
        
        {/* Business Intelligence */}
        <Route path="business-intelligence" element={<BusinessIntelligenceDashboard />} />
        <Route path="business-intelligence/kpi" element={<KPIMgmt />} />
        <Route path="business-intelligence/predictive-analysis" element={<PredictiveAnalysis />} />
        <Route path="business-intelligence/sensitivity-analysis" element={<SensitivityAnalysis />} />
        <Route path="business-intelligence/deviation-analysis" element={<DeviationAnalysis />} />
        
        {/* Reports */}
        <Route path="reports" element={<ReportsDashboard />} />
        <Route path="reports/custom-reports" element={<CustomReports />} />
        
        {/* AI Assistant */}
        <Route path="ai-assistant" element={<AIAssistant />} />
        
        {/* Printing Agents */}
        <Route path="printing-agents" element={<PrintingAgents />} />
        
        {/* Permissions */}
        <Route path="permissions" element={<PermissionsDashboard />} />
        
        {/* Settings */}
        <Route path="settings" element={<SystemSettings />} />
        <Route path="settings/theme" element={<ThemeSettings />} />
        <Route path="settings/language" element={<LanguageSettings />} />
        
        {/* Security */}
        <Route path="security/fraud-detection" element={<FraudDetection />} />
        <Route path="security/audit" element={<SecurityAudit />} />
        <Route path="security/data-encryption" element={<DataEncryption />} />
        
        {/* Maintenance */}
        <Route path="maintenance/planning" element={<MaintenancePlanning />} />
        
        {/* Document Management */}
        <Route path="documents/version-control" element={<VersionControl />} />
        <Route path="documents/electronic-signatures" element={<ElectronicSignatures />} />
      </Route>
      
      {/* Catch all */}
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
};

export default App;