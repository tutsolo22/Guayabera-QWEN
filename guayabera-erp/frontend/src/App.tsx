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
      </Route>
      
      {/* Catch all */}
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
};

export default App;
