import React from 'react';
import { Card, Row, Col, Statistic, Button, Typography, Table, Tag, Alert } from 'antd';
import { 
  CustomerServiceOutlined, 
  PlusOutlined, 
  MessageOutlined, 
  CheckSquareOutlined,
  ClockCircleOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;

const HelpdeskDashboard: React.FC = () => {
  const tickets = [
    { key: '1', id: 'TKT-001', titulo: 'Error en módulo de facturación', estado: 'Abierto', prioridad: 'Alta', solicitante: 'José Martínez', fecha: '2023-04-01' },
    { key: '2', id: 'TKT-002', titulo: 'Solicitud de nuevo reporte', estado: 'En Progreso', prioridad: 'Media', solicitante: 'Ana López', fecha: '2023-04-02' },
    { key: '3', id: 'TKT-003', titulo: 'Consulta sobre nómina', estado: 'Resuelto', prioridad: 'Baja', solicitante: 'Carlos Ramírez', fecha: '2023-03-28' },
    { key: '4', id: 'TKT-004', titulo: 'Problemas con login', estado: 'Cerrado', prioridad: 'Alta', solicitante: 'Luisa Gómez', fecha: '2023-04-01' },
  ];

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Título', dataIndex: 'titulo', key: 'titulo' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'Abierto') color = 'orange';
        if (estado === 'En Progreso') color = 'blue';
        if (estado === 'Resuelto') color = 'gold';
        if (estado === 'Cerrado') color = 'green';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { 
      title: 'Prioridad', 
      dataIndex: 'prioridad', 
      key: 'prioridad',
      render: (prioridad: string) => {
        let color = 'default';
        if (prioridad === 'Alta') color = 'red';
        if (prioridad === 'Media') color = 'orange';
        if (prioridad === 'Baja') color = 'green';
        return <Tag color={color}>{prioridad}</Tag>;
      }
    },
    { title: 'Solicitante', dataIndex: 'solicitante', key: 'solicitante' },
    { title: 'Fecha', dataIndex: 'fecha', key: 'fecha' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <>
          <Button type="link" icon={<MessageOutlined />}>Ver</Button>
          <Button type="link" icon={<CheckSquareOutlined />}>Resolver</Button>
        </>
      ),
    },
  ];

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}>Módulo de Helpdesk</Title>
          <Text>
            Sistema de soporte técnico y administración de tickets
          </Text>
        </div>
        <Button type="primary" icon={<PlusOutlined />}>
          Nuevo Ticket
        </Button>
      </Row>
      
      <Alert
        message="Módulo en Desarrollo"
        description="Este módulo permitirá gestionar tickets de soporte técnico y seguimiento de problemas."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Tickets Abiertos" 
              value={12} 
              prefix={<CustomerServiceOutlined />} 
              valueStyle={{ color: '#ff4d4f' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="En Progreso" 
              value={8} 
              prefix={<ClockCircleOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Resueltos Hoy" 
              value={5} 
              prefix={<CheckSquareOutlined />} 
              valueStyle={{ color: '#52c41a' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Total Tickets" 
              value={128} 
              prefix={<CustomerServiceOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
      </Row>

      <Card className="dashboard-card">
        <Table dataSource={tickets} columns={columns} />
      </Card>
    </div>
  );
};

export default HelpdeskDashboard;