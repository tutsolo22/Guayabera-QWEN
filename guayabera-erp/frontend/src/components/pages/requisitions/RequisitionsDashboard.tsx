import React from 'react';
import { Card, Row, Col, Statistic, Button, Typography, Table, Tag, Alert } from 'antd';
import { 
  FileSyncOutlined, 
  PlusOutlined, 
  SearchOutlined, 
  CheckCircleOutlined,
  CloseCircleOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;

const RequisitionsDashboard: React.FC = () => {
  const requisitions = [
    { key: '1', id: 'REQ-001', descripcion: 'Material para producción de verano', departamento: 'Producción', solicitante: 'Carlos Ramírez', total: 15000, estado: 'Aprobado', fecha: '2023-04-01' },
    { key: '2', id: 'REQ-002', descripcion: 'Equipos de cómputo nuevos', departamento: 'TI', solicitante: 'Ana López', total: 45000, estado: 'Pendiente', fecha: '2023-04-02' },
    { key: '3', id: 'REQ-003', descripcion: 'Suministros de oficina', departamento: 'Administración', solicitante: 'José Martínez', total: 8500, estado: 'Rechazado', fecha: '2023-03-28' },
    { key: '4', id: 'REQ-004', descripcion: 'Maquinaria industrial', departamento: 'Producción', solicitante: 'Luisa Gómez', total: 125000, estado: 'Aprobado', fecha: '2023-04-01' },
  ];

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Descripción', dataIndex: 'descripcion', key: 'descripcion' },
    { title: 'Departamento', dataIndex: 'departamento', key: 'departamento' },
    { title: 'Solicitante', dataIndex: 'solicitante', key: 'solicitante' },
    { 
      title: 'Total', 
      dataIndex: 'total', 
      key: 'total',
      render: (total: number) => `$${total.toLocaleString()}`
    },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'Aprobado') color = 'green';
        if (estado === 'Pendiente') color = 'orange';
        if (estado === 'Rechazado') color = 'red';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { title: 'Fecha', dataIndex: 'fecha', key: 'fecha' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <>
          <Button type="link" icon={<SearchOutlined />}>Ver</Button>
          <Button type="link" icon={<CheckCircleOutlined />}>Aprobar</Button>
        </>
      ),
    },
  ];

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}>Módulo de Requisiciones</Title>
          <Text>
            Gestión de solicitudes internas de materiales y servicios
          </Text>
        </div>
        <Button type="primary" icon={<PlusOutlined />}>
          Nueva Requisición
        </Button>
      </Row>
      
      <Alert
        message="Módulo en Desarrollo"
        description="Este módulo permitirá gestionar solicitudes internas de materiales y servicios con flujo de aprobación."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Requisiciones" 
              value={86} 
              prefix={<FileSyncOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Pendientes" 
              value={15} 
              prefix={<SearchOutlined />} 
              valueStyle={{ color: '#fa8c16' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Aprobadas" 
              value={62} 
              prefix={<CheckCircleOutlined />} 
              valueStyle={{ color: '#52c41a' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Rechazadas" 
              value={9} 
              prefix={<CloseCircleOutlined />} 
              valueStyle={{ color: '#ff4d4f' }} 
            />
          </Card>
        </Col>
      </Row>

      <Card className="dashboard-card">
        <Table dataSource={requisitions} columns={columns} />
      </Card>
    </div>
  );
};

export default RequisitionsDashboard;