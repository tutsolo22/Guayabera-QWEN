import React from 'react';
import { Card, Row, Col, Statistic, Button, Typography, Table, Tag, Alert } from 'antd';
import { 
  SafetyCertificateOutlined, 
  PlusOutlined, 
  CheckSquareOutlined, 
  IssuesCloseOutlined,
  PercentageOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;

const QualityControlDashboard: React.FC = () => {
  const inspections = [
    { key: '1', id: 'QC-001', producto: 'Camisa Lino Azul Marino', lote: 'LOT-2023-001', cantidad: 500, resultado: 'Aprobado', responsable: 'Ana López', fecha: '2023-04-01' },
    { key: '2', id: 'QC-002', producto: 'Vestido Seda Rosa', lote: 'LOT-2023-002', cantidad: 300, resultado: 'Rechazado', responsable: 'Carlos Ramírez', fecha: '2023-04-02' },
    { key: '3', id: 'QC-003', producto: 'Pantalón Mezclilla Negra', lote: 'LOT-2023-003', cantidad: 750, resultado: 'Pendiente', responsable: 'José Martínez', fecha: '2023-04-03' },
    { key: '4', id: 'QC-004', producto: 'Blusa Algodón Blanca', lote: 'LOT-2023-004', cantidad: 400, resultado: 'Aprobado', responsable: 'Luisa Gómez', fecha: '2023-04-01' },
  ];

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Producto', dataIndex: 'producto', key: 'producto' },
    { title: 'Lote', dataIndex: 'lote', key: 'lote' },
    { title: 'Cantidad', dataIndex: 'cantidad', key: 'cantidad' },
    { 
      title: 'Resultado', 
      dataIndex: 'resultado', 
      key: 'resultado',
      render: (resultado: string) => {
        let color = 'default';
        if (resultado === 'Aprobado') color = 'green';
        if (resultado === 'Rechazado') color = 'red';
        if (resultado === 'Pendiente') color = 'orange';
        return <Tag color={color}>{resultado}</Tag>;
      }
    },
    { title: 'Responsable', dataIndex: 'responsable', key: 'responsable' },
    { title: 'Fecha', dataIndex: 'fecha', key: 'fecha' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <>
          <Button type="link" icon={<CheckSquareOutlined />}>Ver Informe</Button>
          <Button type="link" icon={<IssuesCloseOutlined />}>Editar</Button>
        </>
      ),
    },
  ];

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}>Módulo de Control de Calidad</Title>
          <Text>
            Gestión de inspecciones y controles de calidad en producción
          </Text>
        </div>
        <Button type="primary" icon={<PlusOutlined />}>
          Nueva Inspección
        </Button>
      </Row>
      
      <Alert
        message="Módulo en Desarrollo"
        description="Este módulo permitirá gestionar los procesos de control de calidad y registrar inspecciones de productos."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Inspecciones" 
              value={124} 
              prefix={<SafetyCertificateOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Aprobadas" 
              value={98} 
              prefix={<CheckSquareOutlined />} 
              valueStyle={{ color: '#52c41a' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Rechazadas" 
              value={18} 
              prefix={<IssuesCloseOutlined />} 
              valueStyle={{ color: '#ff4d4f' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Eficacia" 
              value="85.2%" 
              prefix={<PercentageOutlined />} 
              valueStyle={{ color: '#52c41a' }} 
            />
          </Card>
        </Col>
      </Row>

      <Card className="dashboard-card">
        <Table dataSource={inspections} columns={columns} />
      </Card>
    </div>
  );
};

export default QualityControlDashboard;