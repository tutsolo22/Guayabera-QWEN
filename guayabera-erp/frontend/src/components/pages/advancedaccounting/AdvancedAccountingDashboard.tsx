import React from 'react';
import { Card, Row, Col, Statistic, Button, Typography, Table, Tag, Alert } from 'antd';
import { 
  CalculatorOutlined, 
  LineChartOutlined, 
  BarChartOutlined, 
  AreaChartOutlined,
  FundProjectionScreenOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;

const AdvancedAccountingDashboard: React.FC = () => {
  const reports = [
    { key: '1', id: 'REP-001', nombre: 'Estado de Resultados', tipo: 'Financiero', periodicidad: 'Mensual', responsable: 'Ana López', status: 'Programado' },
    { key: '2', id: 'REP-002', nombre: 'Análisis de Costos', tipo: 'Costos', periodicidad: 'Semanal', responsable: 'Carlos Ramírez', status: 'Ejecutándose' },
    { key: '3', id: 'REP-003', nombre: 'Flujo de Efectivo', tipo: 'Financiero', periodicidad: 'Diario', responsable: 'José Martínez', status: 'Completado' },
    { key: '4', id: 'REP-004', nombre: 'Margen de Utilidad', tipo: 'Analítico', periodicidad: 'Mensual', responsable: 'Luisa Gómez', status: 'Pendiente' },
  ];

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Tipo', dataIndex: 'tipo', key: 'tipo' },
    { title: 'Periodicidad', dataIndex: 'periodicidad', key: 'periodicidad' },
    { title: 'Responsable', dataIndex: 'responsable', key: 'responsable' },
    { 
      title: 'Status', 
      dataIndex: 'status', 
      key: 'status',
      render: (status: string) => {
        let color = 'default';
        if (status === 'Completado') color = 'green';
        if (status === 'Ejecutándose') color = 'blue';
        if (status === 'Programado') color = 'orange';
        if (status === 'Pendiente') color = 'gray';
        return <Tag color={color}>{status}</Tag>;
      }
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <>
          <Button type="link" icon={<BarChartOutlined />}>Ver</Button>
          <Button type="link" icon={<FundProjectionScreenOutlined />}>Programar</Button>
        </>
      ),
    },
  ];

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}>Módulo de Contabilidad Avanzada</Title>
          <Text>
            Reportes financieros, análisis de costos y proyecciones contables
          </Text>
        </div>
        <Button type="primary" icon={<LineChartOutlined />}>
          Nuevo Reporte
        </Button>
      </Row>
      
      <Alert
        message="Módulo en Desarrollo"
        description="Este módulo permitirá generar reportes financieros avanzados, análisis de costos y proyecciones contables."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Reportes" 
              value={24} 
              prefix={<CalculatorOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Automatizados" 
              value={18} 
              prefix={<AreaChartOutlined />} 
              valueStyle={{ color: '#52c41a' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Este Mes" 
              value={12} 
              prefix={<LineChartOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Programados" 
              value={6} 
              prefix={<FundProjectionScreenOutlined />} 
              valueStyle={{ color: '#722ed1' }} 
            />
          </Card>
        </Col>
      </Row>

      <Card className="dashboard-card">
        <Table dataSource={reports} columns={columns} />
      </Card>
    </div>
  );
};

export default AdvancedAccountingDashboard;