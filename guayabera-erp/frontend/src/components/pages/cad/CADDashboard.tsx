import React from 'react';
import { Card, Row, Col, Statistic, Button, Typography, Alert } from 'antd';
import { 
  DesktopOutlined, 
  EyeOutlined, 
  DownloadOutlined, 
  UploadOutlined 
} from '@ant-design/icons';

const { Title, Text } = Typography;

const CADDashboard: React.FC = () => {
  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}>Módulo de Diseño CAD</Title>
          <Text>
            Gestión de diseños técnicos y modelos 3D para prendas de vestir
          </Text>
        </div>
      </Row>
      
      <Alert
        message="Módulo en Desarrollo"
        description="Este módulo se conectará con agentes locales para realizar operaciones de CAD intensivas en la máquina del cliente."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Diseños" 
              value={128} 
              prefix={<EyeOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Modelos 3D" 
              value={86} 
              prefix={<DesktopOutlined />} 
              valueStyle={{ color: '#52c41a' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Patrones" 
              value={245} 
              prefix={<EyeOutlined />} 
              valueStyle={{ color: '#722ed1' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Clientes" 
              value={32} 
              prefix={<DownloadOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
      </Row>

      <Card className="dashboard-card">
        <Title level={4}>Funcionalidades Disponibles</Title>
        <Row gutter={16}>
          <Col span={8}>
            <Card 
              hoverable
              style={{ textAlign: 'center' }}
              cover={<div style={{ height: 120, background: '#f0f2f5', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <DesktopOutlined style={{ fontSize: '48px', color: '#1890ff' }} />
              </div>}
            >
              <Title level={5}>Visualizador CAD</Title>
              <Text type="secondary">Visualización de modelos 3D</Text>
            </Card>
          </Col>
          <Col span={8}>
            <Card 
              hoverable
              style={{ textAlign: 'center' }}
              cover={<div style={{ height: 120, background: '#f0f2f5', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <UploadOutlined style={{ fontSize: '48px', color: '#52c41a' }} />
              </div>}
            >
              <Title level={5}>Carga de Modelos</Title>
              <Text type="secondary">Importar diseños CAD</Text>
            </Card>
          </Col>
          <Col span={8}>
            <Card 
              hoverable
              style={{ textAlign: 'center' }}
              cover={<div style={{ height: 120, background: '#f0f2f5', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <DownloadOutlined style={{ fontSize: '48px', color: '#fa8c16' }} />
              </div>}
            >
              <Title level={5}>Exportar Diseños</Title>
              <Text type="secondary">Descargar archivos CAD</Text>
            </Card>
          </Col>
        </Row>
      </Card>
    </div>
  );
};

export default CADDashboard;