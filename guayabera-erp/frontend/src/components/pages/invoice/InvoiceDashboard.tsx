import React from 'react';
import { Card, Row, Col, Statistic, Table, Button, Space, Typography, Tag } from 'antd';
import { PlusOutlined, FileTextOutlined, CreditCardOutlined, PrinterOutlined, CheckCircleOutlined } from '@ant-design/icons';

const { Title } = Typography;

const InvoiceDashboard: React.FC = () => {
  // Datos simulados para la tabla de facturas
  const invoicesData = [
    { key: '1', id: 'FAC-001', cliente: 'Tienda Yucateca', total: 15000, estado: 'Válida', fecha: '2023-04-01', uuid: 'abc123-456-def-789-ghi' },
    { key: '2', id: 'FAC-002', cliente: 'Exportadora Maya', total: 28500, estado: 'Cancelada', fecha: '2023-04-02', uuid: 'jkl098-765-mno-432-pqr' },
    { key: '3', id: 'FAC-003', cliente: 'Modas Tradicionales', total: 9750, estado: 'Válida', fecha: '2023-04-03', uuid: 'stu654-321-vwx-987-yz' },
    { key: '4', id: 'FAC-004', cliente: 'Regalos Elegantes', total: 12300, estado: 'Pendiente', fecha: '2023-04-04', uuid: 'abc111-222-def-333-ghi' },
  ];

  const columns = [
    { title: 'Folio Fiscal', dataIndex: 'id', key: 'id' },
    { title: 'Cliente', dataIndex: 'cliente', key: 'cliente' },
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
        if (estado === 'Válida') color = 'green';
        if (estado === 'Cancelada') color = 'red';
        if (estado === 'Pendiente') color = 'orange';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { title: 'Fecha', dataIndex: 'fecha', key: 'fecha' },
    { title: 'UUID', dataIndex: 'uuid', key: 'uuid', ellipsis: true },
    {
      title: 'Acciones',
      key: 'acciones',
      render: (_, record) => (
        <Space size="middle">
          <Button type="link" disabled={record.estado !== 'Válida'}>Timbrar</Button>
          <Button type="link" disabled={record.estado !== 'Válida'}>Cancelar</Button>
          <Button type="link">Imprimir</Button>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Title level={2}>Módulo de Facturación Electrónica</Title>
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Facturas Emitidas" 
              value={342} 
              prefix={<FileTextOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Facturas Válidas" 
              value={328} 
              prefix={<CheckCircleOutlined />} 
              valueStyle={{ color: '#3f8600' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Facturas Canceladas" 
              value={12} 
              prefix={<CreditCardOutlined />} 
              valueStyle={{ color: '#ff4d4f' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Ingresos Facturados" 
              value="$1.2M" 
              precision={2}
              prefix={<PrinterOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
      </Row>

      <Card 
        title="Facturas Recientes" 
        extra={<Button type="primary" icon={<PlusOutlined />}>Nueva Factura</Button>}
        className="dashboard-card"
      >
        <Table dataSource={invoicesData} columns={columns} />
      </Card>
    </div>
  );
};

export default InvoiceDashboard;