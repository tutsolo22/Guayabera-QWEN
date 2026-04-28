import React from 'react';
import { Card, Row, Col, Statistic, Button, Typography, Table, Tag, Alert } from 'antd';
import { 
  CarOutlined, 
  PlusOutlined, 
  ShopOutlined, 
  ContainerOutlined,
  CarryOutOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;

const LogisticsDashboard: React.FC = () => {
  const shipments = [
    { key: '1', id: 'ENV-001', destino: 'Ciudad de México', tipo: 'Local', peso: '150 kg', estado: 'En Tránsito', fechaEnvio: '2023-04-01', fechaEntrega: '2023-04-03' },
    { key: '2', id: 'ENV-002', destino: 'Monterrey', tipo: 'Nacional', peso: '320 kg', estado: 'Entregado', fechaEnvio: '2023-03-28', fechaEntrega: '2023-03-30' },
    { key: '3', id: 'ENV-003', destino: 'Guadalajara', tipo: 'Nacional', peso: '85 kg', estado: 'Preparando', fechaEnvio: '2023-04-02', fechaEntrega: '2023-04-05' },
    { key: '4', id: 'ENV-004', destino: 'Mérida', tipo: 'Local', peso: '210 kg', estado: 'En Ruta', fechaEnvio: '2023-04-01', fechaEntrega: '2023-04-02' },
  ];

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Destino', dataIndex: 'destino', key: 'destino' },
    { title: 'Tipo', dataIndex: 'tipo', key: 'tipo' },
    { title: 'Peso', dataIndex: 'peso', key: 'peso' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'Entregado') color = 'green';
        if (estado === 'En Tránsito' || estado === 'En Ruta') color = 'blue';
        if (estado === 'Preparando') color = 'orange';
        if (estado === 'Retrasado') color = 'red';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { title: 'Fecha Envío', dataIndex: 'fechaEnvio', key: 'fechaEnvio' },
    { title: 'Fecha Entrega', dataIndex: 'fechaEntrega', key: 'fechaEntrega' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <>
          <Button type="link" icon={<CarryOutOutlined />}>Rastrear</Button>
          <Button type="link" icon={<ContainerOutlined />}>Detalles</Button>
        </>
      ),
    },
  ];

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}>Módulo de Logística</Title>
          <Text>
            Gestión de envíos, transporte y distribución de mercancías
          </Text>
        </div>
        <Button type="primary" icon={<PlusOutlined />}>
          Nuevo Envío
        </Button>
      </Row>
      
      <Alert
        message="Módulo en Desarrollo"
        description="Este módulo permitirá gestionar la logística de envíos y distribución de productos."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Envíos" 
              value={128} 
              prefix={<CarOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="En Tránsito" 
              value={24} 
              prefix={<CarryOutOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Entregados" 
              value={98} 
              prefix={<ShopOutlined />} 
              valueStyle={{ color: '#52c41a' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Retrasados" 
              value={6} 
              prefix={<ContainerOutlined />} 
              valueStyle={{ color: '#ff4d4f' }} 
            />
          </Card>
        </Col>
      </Row>

      <Card className="dashboard-card">
        <Table dataSource={shipments} columns={columns} />
      </Card>
    </div>
  );
};

export default LogisticsDashboard;