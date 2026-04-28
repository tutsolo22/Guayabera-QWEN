import React from 'react';
import { Card, Row, Col, Statistic, Table, Button, Space, Typography, Tag } from 'antd';
import { PlusOutlined, FileTextOutlined, UserOutlined, CalendarOutlined, CreditCardOutlined } from '@ant-design/icons';

const { Title } = Typography;

const PayrollDashboard: React.FC = () => {
  // Datos simulados para la tabla de recibos de nómina
  const payrollData = [
    { key: '1', id: 'NOM-001', empleado: 'Juan Pérez', periodo: 'Marzo 2023', total: 15000, estado: 'Pagado', fecha: '2023-04-01' },
    { key: '2', id: 'NOM-002', empleado: 'María López', periodo: 'Marzo 2023', total: 18500, estado: 'Pendiente', fecha: '2023-04-02' },
    { key: '3', id: 'NOM-003', empleado: 'Carlos Ramírez', periodo: 'Marzo 2023', total: 12300, estado: 'Pagado', fecha: '2023-04-01' },
    { key: '4', id: 'NOM-004', empleado: 'Ana Gutiérrez', periodo: 'Marzo 2023', total: 22500, estado: 'Pagado', fecha: '2023-04-01' },
  ];

  const columns = [
    { title: 'ID Nómina', dataIndex: 'id', key: 'id' },
    { title: 'Empleado', dataIndex: 'empleado', key: 'empleado' },
    { title: 'Periodo', dataIndex: 'periodo', key: 'periodo' },
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
        if (estado === 'Pagado') color = 'green';
        if (estado === 'Pendiente') color = 'orange';
        if (estado === 'Cancelado') color = 'red';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { title: 'Fecha', dataIndex: 'fecha', key: 'fecha' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: (_, record) => (
        <Space size="middle">
          <Button type="link">Ver Detalle</Button>
          <Button type="link">Imprimir</Button>
          <Button type="link" disabled={record.estado !== 'Pendiente'}>Procesar</Button>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Title level={2}>Módulo de Nómina Electrónica</Title>
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Empleados" 
              value={42} 
              prefix={<UserOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Nóminas Procesadas" 
              value={126} 
              prefix={<FileTextOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Nóminas Pendientes" 
              value={8} 
              prefix={<CalendarOutlined />} 
              valueStyle={{ color: '#ff4d4f' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Total Pagado" 
              value="$524K" 
              precision={2}
              prefix={<CreditCardOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
      </Row>

      <Card 
        title="Nóminas Recientes" 
        extra={<Button type="primary" icon={<PlusOutlined />}>Nueva Nómina</Button>}
        className="dashboard-card"
      >
        <Table dataSource={payrollData} columns={columns} />
      </Card>
    </div>
  );
};

export default PayrollDashboard;