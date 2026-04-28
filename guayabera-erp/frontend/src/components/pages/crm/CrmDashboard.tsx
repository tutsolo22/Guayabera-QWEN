import React from 'react';
import { Card, Row, Col, Statistic, Button, Typography, Table, Tag, Alert } from 'antd';
import { 
  TeamOutlined, 
  PlusOutlined, 
  PhoneOutlined, 
  MailOutlined,
  UserAddOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;

const CrmDashboard: React.FC = () => {
  const clients = [
    { key: '1', id: 'CLI-001', nombre: 'Tienda Yucateca', tipo: 'Mayorista', contacto: 'José Pérez', telefono: '999-123-4567', estado: 'Activo', ultimoContacto: '2023-04-01' },
    { key: '2', id: 'CLI-002', nombre: 'Exportadora Maya', tipo: 'Distribuidor', contacto: 'María López', telefono: '999-234-5678', estado: 'Activo', ultimoContacto: '2023-04-02' },
    { key: '3', id: 'CLI-003', nombre: 'Modas Tradicionales', tipo: 'Detallista', contacto: 'Carlos Ramírez', telefono: '999-345-6789', estado: 'Inactivo', ultimoContacto: '2023-03-15' },
    { key: '4', id: 'CLI-004', nombre: 'Regalos Elegantes', tipo: 'Mayorista', contacto: 'Ana Gómez', telefono: '999-456-7890', estado: 'Activo', ultimoContacto: '2023-04-01' },
  ];

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { 
      title: 'Tipo', 
      dataIndex: 'tipo', 
      key: 'tipo',
      render: (tipo: string) => {
        let color = 'default';
        if (tipo === 'Mayorista') color = 'blue';
        if (tipo === 'Detallista') color = 'green';
        if (tipo === 'Distribuidor') color = 'orange';
        return <Tag color={color}>{tipo}</Tag>;
      }
    },
    { title: 'Contacto', dataIndex: 'contacto', key: 'contacto' },
    { title: 'Teléfono', dataIndex: 'telefono', key: 'telefono' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'Activo') color = 'green';
        if (estado === 'Inactivo') color = 'red';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { title: 'Último Contacto', dataIndex: 'ultimoContacto', key: 'ultimoContacto' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <>
          <Button type="link" icon={<PhoneOutlined />}>Llamar</Button>
          <Button type="link" icon={<MailOutlined />}>Email</Button>
          <Button type="link" icon={<UserAddOutlined />}>Relación</Button>
        </>
      ),
    },
  ];

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}>Módulo de CRM</Title>
          <Text>
            Gestión de relaciones con clientes y oportunidades comerciales
          </Text>
        </div>
        <Button type="primary" icon={<PlusOutlined />}>
          Nuevo Cliente
        </Button>
      </Row>
      
      <Alert
        message="Módulo en Desarrollo"
        description="Este módulo permitirá gestionar las relaciones con clientes, oportunidades de negocio y campañas de marketing."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
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
              title="Activos" 
              value={108} 
              prefix={<TeamOutlined />} 
              valueStyle={{ color: '#52c41a' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Oportunidades" 
              value={24} 
              prefix={<PlusOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Contactos Hoy" 
              value={8} 
              prefix={<PhoneOutlined />} 
              valueStyle={{ color: '#722ed1' }} 
            />
          </Card>
        </Col>
      </Row>

      <Card className="dashboard-card">
        <Table dataSource={clients} columns={columns} />
      </Card>
    </div>
  );
};

export default CrmDashboard;