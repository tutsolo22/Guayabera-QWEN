import React from 'react';
import { Card, Row, Col, Statistic, Button, Space, Typography } from 'antd';
import { 
  UserOutlined, 
  TeamOutlined, 
  DollarOutlined, 
  ShoppingCartOutlined, 
  StockOutlined, 
  FileTextOutlined, 
  SettingOutlined,
  UsergroupAddOutlined,
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
  ProjectOutlined,
  ApartmentOutlined,
  BarChartOutlined,
  PieChartOutlined,
  LockOutlined,
  ToolOutlined,
  RiseOutlined,
  RobotOutlined,
  PrinterOutlined,
  TrophyOutlined,
  ThunderboltOutlined
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';

const { Title } = Typography;

const DashboardPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div>
      <Title level={2}>Panel de Control</Title>
      <Typography.Paragraph>
        Bienvenido al sistema ERP Guayabera. Accede a los diferentes módulos del sistema.
      </Typography.Paragraph>

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
                <UsergroupAddOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/hr')}>Ir a RH</Button>
            ]}
          >
            <Card.Meta
              title="Recursos Humanos"
              description="Gestión de empleados, nóminas y asistencias"
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
              <Button type="link" onClick={() => navigate('/production')}>Ir a Producción</Button>
            ]}
          >
            <Card.Meta
              title="Producción"
              description="Órdenes de producción y control de calidad"
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
                <ShoppingCartOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/sales')}>Ir a Ventas</Button>
            ]}
          >
            <Card.Meta
              title="Ventas"
              description="Clientes, pedidos y cotizaciones"
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
              <Button type="link" onClick={() => navigate('/inventory')}>Ir a Inventario</Button>
            ]}
          >
            <Card.Meta
              title="Inventario"
              description="Control de productos y niveles de stock"
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
                <FileTextOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/finance')}>Ir a Contabilidad</Button>
            ]}
          >
            <Card.Meta
              title="Contabilidad"
              description="Catálogo de cuentas y pólizas"
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
              <Button type="link" onClick={() => navigate('/supply-chain')}>Ir a Cadena de Suministro</Button>
            ]}
          >
            <Card.Meta
              title="Cadena de Suministro"
              description="Proveedores y órdenes de compra"
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
                <TransactionOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/invoice')}>Ir a Facturación</Button>
            ]}
          >
            <Card.Meta
              title="Facturación Electrónica"
              description="Emisión y manejo de CFDI"
            />
          </Card>
        </Col>
        
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
                <FileProtectOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/payroll')}>Ir a Nómina</Button>
            ]}
          >
            <Card.Meta
              title="Nómina Electrónica"
              description="Gestión de recibos y percepciones/deducciones"
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
                background: 'linear-gradient(135deg, #da22ff 0%, #9733ee 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <BarChartOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/reports')}>Generar Reporte</Button>,
              <Button type="link" onClick={() => navigate('/reports/custom-reports')}>Reportes Personalizados</Button>
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
                <RiseOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/executive-dashboard')}>Ver Dashboard</Button>,
              <Button type="link" onClick={() => navigate('/executive-dashboard')}>Indicadores Clave</Button>
            ]}
          >
            <Card.Meta
              title="Dashboard Ejecutivo"
              description="Visión general del desempeño empresarial con KPIs y métricas clave"
            />
          </Card>
        </Col>
        
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #5ee7df 0%, #b490ca 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <RobotOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/ai-assistant')}>Asistente IA</Button>,
              <Button type="link" onClick={() => navigate('/ai-assistant')}>Ayuda Inteligente</Button>
            ]}
          >
            <Card.Meta
              title="Asistente de IA"
              description="Tu asistente virtual para resolver dudas y guiar en el uso del sistema ERP"
            />
          </Card>
        </Col>
        
        <Col span={6}>
          <Card 
            hoverable
            cover={
              <div style={{ 
                height: 120, 
                background: 'linear-gradient(135deg, #5a6268 0%, #868e96 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <PrinterOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/printing-agents')}>Gestionar Agentes</Button>,
              <Button type="link" onClick={() => navigate('/printing-agents')}>Impresión Distribuida</Button>
            ]}
          >
            <Card.Meta
              title="Agentes de Impresión"
              description="Gestión de agentes de impresión locales y en red para reducir la carga del servidor"
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
                background: 'linear-gradient(135deg, #00c9ff 0%, #92fe9d 100%)', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center' 
              }}>
                <TrophyOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/business-intelligence/kpi')}>Gestionar KPIs</Button>,
              <Button type="link" onClick={() => navigate('/business-intelligence/kpi')}>Monitorear Indicadores</Button>
            ]}
          >
            <Card.Meta
              title="Gestión de KPIs"
              description="Configuración y monitoreo de indicadores clave de desempeño"
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
                <ThunderboltOutlined style={{ fontSize: '48px', color: 'white' }} />
              </div>
            }
            actions={[
              <Button type="link" onClick={() => navigate('/business-intelligence/predictive-analysis')}>Modelos Predictivos</Button>,
              <Button type="link" onClick={() => navigate('/business-intelligence/predictive-analysis')}>Análisis Avanzado</Button>
            ]}
          >
            <Card.Meta
              title="Análisis Predictivo"
              description="Modelos predictivos para anticipar tendencias y comportamientos"
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default DashboardPage;