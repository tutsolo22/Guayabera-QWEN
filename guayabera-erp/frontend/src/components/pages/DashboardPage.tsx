import React from 'react';
import { Card, Row, Col, Statistic, Button, Space, Typography, Tooltip } from 'antd';
import { 
  ArrowUpOutlined, 
  ArrowDownOutlined, 
  DollarCircleOutlined, 
  ShoppingCartOutlined, 
  TeamOutlined, 
  AppstoreOutlined,
  ToolOutlined,
  ShoppingOutlined,
  StockOutlined,
  UsergroupAddOutlined,
  AccountBookOutlined,
  SettingOutlined,
  ShopOutlined,
  TransactionOutlined,
  FileProtectOutlined,
  DesktopOutlined,
  ProfileOutlined,
  CustomerServiceOutlined,
  FileSyncOutlined,
  NotificationOutlined,
  SafetyCertificateOutlined,
  CarOutlined,
  TeamOutlined as TeamOutlined2,
  ProjectOutlined,
  ApartmentOutlined,
  BarChartOutlined,
  PieChartOutlined,
  LockOutlined,
  ToolOutlined
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';

const { Title } = Typography;

const DashboardPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div>
      <Title level={2}>Panel de Control</Title>
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Ventas Hoy" 
              value={12} 
              prefix={<ShoppingCartOutlined />} 
              valueStyle={{ color: '#3f8600' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Ingresos Hoy" 
              value="$42,500" 
              precision={2}
              prefix={<DollarCircleOutlined />} 
              valueStyle={{ color: '#3f8600' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Clientes" 
              value={124} 
              prefix={<TeamOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Pedidos Pendientes" 
              value={8} 
              prefix={<ArrowDownOutlined />} 
              valueStyle={{ color: '#cf1322' }} 
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col span={24}>
          <Title level={3}>Módulos del Sistema</Title>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <AccountBookOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/finance/cuentas')}>Catálogo de Cuentas</Button>,
              <Button type="link" onClick={() => navigate('/finance/polizas')}>Pólizas</Button>
            ]}
          >
            <Card.Meta
              title="Contabilidad"
              description="Gestión de cuentas, pólizas y asientos contables"
            />
          </Card>
        </Col>
        
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <ToolOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/production')}>Órdenes de Producción</Button>
            ]}
          >
            <Card.Meta
              title="Producción"
              description="Gestión de órdenes de producción y control de calidad"
            />
          </Card>
        </Col>
        
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <ShoppingOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/sales')}>Ventas</Button>
            ]}
          >
            <Card.Meta
              title="Ventas"
              description="Gestión de clientes, pedidos y cotizaciones"
            />
          </Card>
        </Col>
        
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <StockOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/inventory')}>Inventario</Button>
            ]}
          >
            <Card.Meta
              title="Inventario"
              description="Gestión de productos y niveles de stock"
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16} style={{ marginTop: 16 }}>
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <UsergroupAddOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/hr')}>Empleados</Button>
            ]}
          >
            <Card.Meta
              title="Recursos Humanos"
              description="Gestión de empleados y nóminas"
            />
          </Card>
        </Col>
        
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <ShopOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/supply-chain')}>Proveedores</Button>,
              <Button type="link" onClick={() => navigate('/supply-chain')}>Órdenes Compra</Button>
            ]}
          >
            <Card.Meta
              title="Cadena de Suministro"
              description="Gestión de proveedores y compras"
            />
          </Card>
        </Col>
        
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <ShoppingCartOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/purchases')}>Solicitudes</Button>,
              <Button type="link" onClick={() => navigate('/purchases')}>Ordenes Compra</Button>
            ]}
          >
            <Card.Meta
              title="Compras"
              description="Gestión de solicitudes y órdenes de compra"
            />
          </Card>
        </Col>
        
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <TransactionOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/invoice')}>Facturas</Button>
            ]}
          >
            <Card.Meta
              title="Facturación Electrónica"
              description="Emisión y manejo de CFDI"
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16} style={{ marginTop: 16 }}>
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <FileProtectOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/payroll')}>Nóminas</Button>
            ]}
          >
            <Card.Meta
              title="Nómina Electrónica"
              description="Gestión de recibos y percepciones/deducciones"
            />
          </Card>
        </Col>
        
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <DesktopOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/agents')}>Gestionar Agentes</Button>
            ]}
          >
            <Card.Meta
              title="Agentes Locales"
              description="Gestión de agentes para tareas locales"
            />
          </Card>
        </Col>
        
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <ProfileOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/size-chart')}>Gráficos</Button>,
              <Button type="link" onClick={() => navigate('/size-chart')}>Tallas</Button>
            ]}
          >
            <Card.Meta
              title="Gráficos de Talla"
              description="Tablas de medidas y tallas"
            />
          </Card>
        </Col>
        
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <DesktopOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/cad')}>Diseños</Button>,
              <Button type="link" onClick={() => navigate('/cad')}>Modelos 3D</Button>
            ]}
          >
            <Card.Meta
              title="Diseño CAD"
              description="Diseño técnico y modelos 3D"
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16} style={{ marginTop: 16 }}>
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #a6c0fe 0%, #f68084 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <SafetyCertificateOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/quality-control')}>Inspecciones</Button>,
              <Button type="link" onClick={() => navigate('/quality-control')}>Reportes</Button>
            ]}
          >
            <Card.Meta
              title="Control de Calidad"
              description="Inspecciones y estándares de calidad"
            />
          </Card>
        </Col>
        
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <CarOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/logistics')}>Envíos</Button>,
              <Button type="link" onClick={() => navigate('/logistics')}>Rutas</Button>
            ]}
          >
            <Card.Meta
              title="Logística"
              description="Gestión de envíos y transporte"
            />
          </Card>
        </Col>
        
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <TeamOutlined2 style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/crm')}>Clientes</Button>,
              <Button type="link" onClick={() => navigate('/crm')}>Oportunidades</Button>
            ]}
          >
            <Card.Meta
              title="CRM"
              description="Relación con clientes"
            />
          </Card>
        </Col>
        
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <ProjectOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/project-management')}>Proyectos</Button>,
              <Button type="link" onClick={() => navigate('/project-management')}>Tareas</Button>
            ]}
          >
            <Card.Meta
              title="Gestión de Proyectos"
              description="Planificación y seguimiento"
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16} style={{ marginTop: 16 }}>
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <ApartmentOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/asset-management')}>Activos</Button>,
              <Button type="link" onClick={() => navigate('/asset-management')}>Mantenimiento</Button>
            ]}
          >
            <Card.Meta
              title="Gestión de Activos"
              description="Inventario de activos fijos"
            />
          </Card>
        </Col>
        
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <BarChartOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/business-intelligence')}>Reportes</Button>,
              <Button type="link" onClick={() => navigate('/business-intelligence')}>KPIs</Button>
            ]}
          >
            <Card.Meta
              title="Inteligencia de Negocios"
              description="Análisis y toma de decisiones"
            />
          </Card>
        </Col>
        
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <FileSyncOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/requisitions')}>Solicitudes</Button>,
              <Button type="link" onClick={() => navigate('/requisitions')}>Aprobaciones</Button>
            ]}
          >
            <Card.Meta
              title="Requisiciones"
              description="Solicitudes internas y aprobaciones"
            />
          </Card>
        </Col>
        
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <CustomerServiceOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/helpdesk')}>Tickets</Button>,
              <Button type="link" onClick={() => navigate('/helpdesk')}>Soporte</Button>
            ]}
          >
            <Card.Meta
              title="Helpdesk"
              description="Soporte técnico y atención"
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16} style={{ marginTop: 16 }}>
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <NotificationOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/notifications')}>Alertas</Button>,
              <Button type="link" onClick={() => navigate('/notifications')}>Mensajes</Button>
            ]}
          >
            <Card.Meta
              title="Notificaciones"
              description="Centro de mensajes y alertas"
            />
          </Card>
        </Col>
        
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #da22ff 0%, #9733ee 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <PieChartOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/reports')}>Generar Reporte</Button>,
              <Button type="link" onClick={() => navigate('/reports')}>Ver Históricos</Button>
            ]}
          >
            <Card.Meta
              title="Sistema de Reportes"
              description="Generación y gestión de reportes para todos los módulos"
            />
          </Card>
        </Col>
        
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #d299c2 0%, #fef9d7 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <LockOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/permissions')}>Gestionar Permisos</Button>,
              <Button type="link" onClick={() => navigate('/permissions')}>Asignar Roles</Button>
            ]}
          >
            <Card.Meta
              title="Gestión de Permisos"
              description="Roles, permisos y asignación a usuarios"
            />
          </Card>
        </Col>
        
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <SettingOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/settings')}>Configuración</Button>
            ]}
          >
            <Card.Meta
              title="Configuración"
              description="Configuración del sistema y temas"
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default DashboardPage;