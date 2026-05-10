import React from 'react';
import { Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { RootState } from '../store';

interface ProtectedRouteProps {
  children: React.ReactNode;
  allowedRoles?: string[];
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
  children, 
  allowedRoles = ['superuser'] 
}) => {
  const { isAuthenticated, user } = useSelector((state: RootState) => state.auth);

  // Check if user is authenticated and has the required role
  const hasRequiredRole = user && allowedRoles.includes(user.tipo_usuario || user.role);

  if (!isAuthenticated) {
    // Redirect to login if not authenticated
    return <Navigate to="/login" />;
  }

  if (!hasRequiredRole) {
    // Redirect to home if user doesn't have required role
    return <Navigate to="/" />;
  }

  // Render the protected component
  return <>{children}</>;
};

export default ProtectedRoute;