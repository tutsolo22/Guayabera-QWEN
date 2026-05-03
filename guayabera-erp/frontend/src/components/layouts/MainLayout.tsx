import React, { useState } from 'react';
import { Layout, Menu, theme, Dropdown, Space } from 'antd';
import type { MenuProps } from 'antd';
import {
  DesktopOutlined,
  PieChartOutlined,
  TeamOutlined,
  UserOutlined,
  ShoppingCartOutlined,
  AppstoreOutlined,
  FileTextOutlined,
  BankOutlined,
  ToolOutlined,
  SafetyCertificateOutlined,
  HistoryOutlined,
  QrcodeOutlined,
  FileProtectOutlined,
  MessageOutlined,
  SettingOutlined,
  LogoutOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  DollarCircleOutlined
} from '@ant-design/icons';
import { useDispatch, useSelector } from 'react-redux';
import { logout } from '../../store/features/auth/authSlice';
import { RootState } from '../../store';
import { Link, useNavigate } from 'react-router-dom';

const { Header, Sider, Content } = Layout;

interface MenuItem {
  key: string;
  label: React.ReactNode;
  icon?: React.ReactNode;
  children?: MenuItem[];
  onClick?: () => void;
}

const MainLayout: React.FC = () => {
  const [collapsed, setCollapsed] = useState(false);
  const {
    token: { colorBgContainer },
  } = theme.useToken();
  
  const dispatch = useDispatch();
  const user = useSelector((state: RootState) => state.auth.user);
  const navigate = useNavigate();

  // Menú superior para usuario
  const userMenuItems: MenuProps['items'] = [
    {
      key: 'profile',
      label: 'Mi Perfil',
      icon: <UserOutlined />,
    },
    {
      key: 'settings',
      label: 'Configuración',
      icon: <SettingOutlined />,
      children: [
        {
          key: 'theme',
          label: <Link to="/theme-settings">Temas</Link>,
          icon: <DesktopOutlined />,
        },
        {
          key: 'system',
          label: <Link to="/system-settings">Sistema</Link>,
          icon: <SettingOutlined />,
        },
        {
          key: 'language',
          label: <Link to="/language-settings">Idioma</Link>,
          icon: <MessageOutlined />,
        },
      ],
    },
    {
      type: 'divider',
    },
    {
      key: 'logout',
      label: 'Cerrar Sesión',
      icon: <LogoutOutlined />,
      danger: true,
      onClick: () => {
        dispatch(logout());
        navigate('/login');
      },
    },
  ];

  // Menú lateral
  const menuItems: MenuItem[] = [
    {
      key: 'dashboard',
      label: <Link to="/">Inicio</Link>,
      icon: <PieChartOutlined />,
    },
    {
      key: 'executive',
      label: <Link to="/executive-dashboard">Dashboard Ejecutivo</Link>,
      icon: <PieChartOutlined />,
    },
    {
      key: 'production',
      label: 'Producción',
      icon: <AppstoreOutlined />,
      children: [
        {
          key: 'production-dashboard',
          label: <Link to="/production">Panel de Producción</Link>,
        },
        {
          key: 'mrp-management',
          label: <Link to="/mrp-management">MRP</Link>,
        },
        {
          key: 'maintenance-planning',
          label: <Link to="/maintenance-planning">Mantenimiento</Link>,
        },
      ],
    },
    {
      key: 'sales',
      label: 'Ventas',
      icon: <ShoppingCartOutlined />,
      children: [
        {
          key: 'sales-dashboard',
          label: <Link to="/sales">Panel de Ventas</Link>,
        },
        {
          key: 'sales-configuration',
          label: <Link to="/sales-configuration">Configuración de Ventas</Link>,
        },
        {
          key: 'client-level-pricing',
          label: <Link to="/client-level-pricing">Precios por Nivel</Link>,
        },
        {
          key: 'advance-payment-orders',
          label: <Link to="/advance-payment-orders">Pedidos con Anticipo</Link>,
        },
        {
          key: 'credit-notes',
          label: <Link to="/credit-notes">Notas de Crédito</Link>,
        },
      ],
    },
    {
      key: 'inventory',
      label: 'Inventario',
      icon: <AppstoreOutlined />,
      children: [
        {
          key: 'inventory-dashboard',
          label: <Link to="/inventory">Panel de Inventario</Link>,
        },
        {
          key: 'product-variants',
          label: <Link to="/product-variants">Variantes de Productos</Link>,
        },
        {
          key: 'qr-scanner',
          label: <Link to="/qr-scanner">Escáner QR</Link>,
        },
        {
          key: 'inventory-count',
          label: <Link to="/inventory-count">Toma de Inventario</Link>,
        },
      ],
    },
    {
      key: 'hr',
      label: 'Recursos Humanos',
      icon: <TeamOutlined />,
      children: [
        {
          key: 'hr-dashboard',
          label: <Link to="/hr">Panel de RH</Link>,
        },
        {
          key: 'hr-new-features',
          label: <Link to="/hr-new-features">Nuevas Funciones</Link>,
        },
        {
          key: 'payroll',
          label: <Link to="/payroll">Nómina</Link>,
        },
      ],
    },
    {
      key: 'finance',
      label: 'Finanzas',
      icon: <BankOutlined />,
      children: [
        {
          key: 'advanced-accounting',
          label: <Link to="/advanced-accounting">Contabilidad Avanzada</Link>,
        },
        {
          key: 'bank-integration',
          label: <Link to="/bank-integration">Integración Bancaria</Link>,
        },
        {
          key: 'collaborative-budgeting',
          label: <Link to="/collaborative-budgeting">Presupuestación</Link>,
        },
        {
          key: 'auto-classification',
          label: <Link to="/auto-classification">Clasificación Automática</Link>,
        },
      ],
    },
    {
      key: 'supply-chain',
      label: 'Cadena de Suministro',
      icon: <AppstoreOutlined />,
      children: [
        {
          key: 'supply-chain-dashboard',
          label: <Link to="/supply-chain">Panel SCM</Link>,
        },
        {
          key: 'purchases',
          label: <Link to="/purchases">Compras</Link>,
        },
        {
          key: 'logistics',
          label: <Link to="/logistics">Logística</Link>,
        },
        {
          key: 'transit-inventory',
          label: <Link to="/transit-inventory">Inventario en Tránsito</Link>,
        },
      ],
    },
    {
      key: 'quality',
      label: 'Calidad',
      icon: <SafetyCertificateOutlined />,
      children: [
        {
          key: 'quality-control',
          label: <Link to="/quality-control">Control de Calidad</Link>,
        },
        {
          key: 'helpdesk',
          label: <Link to="/helpdesk">Soporte Técnico</Link>,
        },
      ],
    },
    {
      key: 'business-intelligence',
      label: 'Inteligencia de Negocios',
      icon: <PieChartOutlined />,
      children: [
        {
          key: 'bi-dashboard',
          label: <Link to="/business-intelligence">Panel BI</Link>,
        },
        {
          key: 'custom-reports',
          label: <Link to="/custom-reports">Reportes Personalizados</Link>,
        },
        {
          key: 'kpi-management',
          label: <Link to="/kpi-management">Gestión de KPIs</Link>,
        },
        {
          key: 'predictive-analysis',
          label: <Link to="/predictive-analysis">Análisis Predictivo</Link>,
        },
        {
          key: 'sensitivity-analysis',
          label: <Link to="/sensitivity-analysis">Análisis de Sensibilidad</Link>,
        },
        {
          key: 'deviation-analysis',
          label: <Link to="/deviation-analysis">Análisis de Desviaciones</Link>,
        },
      ],
    },
    {
      key: 'projects',
      label: 'Proyectos',
      icon: <FileTextOutlined />,
      children: [
        {
          key: 'project-management',
          label: <Link to="/project-management">Gestión de Proyectos</Link>,
        },
        {
          key: 'requisitions',
          label: <Link to="/requisitions">Requisiciones</Link>,
        },
      ],
    },
    {
      key: 'assets',
      label: 'Activos',
      icon: <ToolOutlined />,
      children: [
        {
          key: 'asset-management',
          label: <Link to="/asset-management">Gestión de Activos</Link>,
        },
        {
          key: 'maintenance-planning',
          label: <Link to="/maintenance-planning">Mantenimiento</Link>,
        },
      ],
    },
    {
      key: 'crm',
      label: 'CRM',
      icon: <TeamOutlined />,
      children: [
        {
          key: 'crm-dashboard',
          label: <Link to="/crm">Panel CRM</Link>,
        },
        {
          key: 'agents',
          label: <Link to="/agents">Agentes</Link>,
        },
      ],
    },
    {
      key: 'design',
      label: 'Diseño',
      icon: <AppstoreOutlined />,
      children: [
        {
          key: 'cad',
          label: <Link to="/cad">Diseño Asistido</Link>,
        },
        {
          key: 'size-chart',
          label: <Link to="/size-chart">Tablas de Tallas</Link>,
        },
        {
          key: 'printing-agents',
          label: <Link to="/printing-agents">Agentes de Impresión</Link>,
        },
        {
          key: 'cad-agents',
          label: <Link to="/cad-agents">Agentes de Diseño</Link>,
        },
      ],
    },
    {
      key: 'admin',
      label: 'Administración',
      icon: <UserOutlined />,
      children: [
        {
          key: 'empresa',
          label: <Link to="/admin/empresa">Empresa</Link>,
        },
        {
          key: 'permissions',
          label: <Link to="/permissions">Permisos</Link>,
        },
        {
          key: 'notifications',
          label: <Link to="/notifications">Notificaciones</Link>,
        },
        {
          key: 'workflow-management',
          label: <Link to="/workflow-management">Flujos de Trabajo</Link>,
        },
        {
          key: 'version-control',
          label: <Link to="/version-control">Control de Versiones</Link>,
        },
      ],
    },
    {
      key: 'security',
      label: 'Seguridad',
      icon: <SafetyCertificateOutlined />,
      children: [
        {
          key: 'security-audit',
          label: <Link to="/security-audit">Auditoría</Link>,
        },
        {
          key: 'fraud-detection',
          label: <Link to="/fraud-detection">Detección de Fraudes</Link>,
        },
        {
          key: 'data-encryption',
          label: <Link to="/data-encryption">Encriptación</Link>,
        },
        {
          key: 'electronic-signatures',
          label: <Link to="/electronic-signatures">Firmas Electrónicas</Link>,
        },
      ],
    },
    {
      key: 'ai',
      label: 'IA',
      icon: <DesktopOutlined />,
      children: [
        {
          key: 'ai-assistant',
          label: <Link to="/ai-assistant">Asistente de IA</Link>,
        },
      ],
    },
  ];

  const onClickMenu = (item: any) => {
    console.log('Clicked menu item:', item.key);
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider 
        collapsible 
        collapsed={collapsed} 
        onCollapse={(value) => setCollapsed(value)}
        style={{ background: colorBgContainer }}
      >
        <div className="demo-logo-vertical" />
        <Menu
          theme="light"
          defaultSelectedKeys={[window.location.pathname.split('/')[1] || 'dashboard']}
          mode="inline"
          items={menuItems}
          onClick={onClickMenu}
        />
      </Sider>
      <Layout>
        <Header style={{ padding: 0, background: colorBgContainer }}>
          <div style={{ float: 'right', paddingRight: 20 }}>
            <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
              <Space style={{ cursor: 'pointer' }}>
                <UserOutlined />
                <span>{user?.nombre || 'Usuario'}</span>
              </Space>
            </Dropdown>
          </div>
          <div style={{ float: 'left', paddingLeft: 20, paddingTop: 10 }}>
            {React.createElement(collapsed ? MenuUnfoldOutlined : MenuFoldOutlined, {
              className: 'trigger',
              onClick: () => setCollapsed(!collapsed),
            })}
          </div>
        </Header>
        <Content style={{ margin: '24px 16px 0', overflow: 'initial' }}>
          <div style={{ padding: 24, minHeight: 360, background: colorBgContainer }}>
            <Outlet />
          </div>
        </Content>
      </Layout>
    </Layout>
  );
};

export default MainLayout;