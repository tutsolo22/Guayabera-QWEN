import React from 'react';
import { Card, Row, Col, Statistic, Button, Typography, Table, Tag, Alert } from 'antd';
import { 
  BarChartOutlined, 
  FundOutlined, 
  RiseOutlined, 
  FallOutlined,
  DotChartOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;

const BusinessIntelligenceDashboard: React.FC = () => {
  const kpis = [
    { key: '1', nombre: 'Ventas Mensuales', valor: '$1,245,670', variacion: '+12.5%', periodo: 'Mes Actual', objetivo: '$1,200,000', estado: 'superado' },
    { key: '2', nombre: 'Margen de Ganancia', valor: '32.4%', variacion: '-2.3%', periodo: 'Mes Actual', objetivo: '35%', estado: 'pendiente' },
    { key: '3', nombre: 'Clientes Activos', valor: '1,248', variacion: '+8.2%', periodo: 'Mes Actual', objetivo: '1,200', estado: 'superado' },
    { key: '4', nombre: 'Satisfacción Cliente', valor: '92%', variacion: '+3.1%', periodo: 'Mes Actual', objetivo: '90%', estado: 'superado' },
  ];

  const columns = [
    { title: 'Indicador', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Valor Actual', dataIndex: 'valor', key: 'valor' },
    { 
      title: 'Variación', 
      dataIndex: 'variacion', 
      key: 'variacion',
      render: (variacion: string) => (
        <span style={{ color: variacion.startsWith('+') ? '#3f8600' : '#cf1322' }}>
          {variacion.startsWith('+') ? <RiseOutlined /> : <FallOutlined />} {variacion}
        </span>
      )
    },
    { title: 'Período', dataIndex: 'periodo', key: 'periodo' },
    { title: 'Objetivo', dataIndex: 'objetivo', key: 'objetivo' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'superado') color = 'green';
        if (estado === 'pendiente') color = 'orange';
        return <Tag color={color}>{estado === 'superado' ? 'Objetivo Superado' : 'En Progreso'}</Tag>;
      }
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <>
          <Button type="link" icon={<BarChartOutlined />}>Gráfica</Button>
          <Button type="link" icon={<DotChartOutlined />}>Detalle</Button>
        </>
      ),
    },
  ];

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}>Módulo de Inteligencia de Negocios</Title>
          <Text>
            Análisis de datos y toma de decisiones estratégicas
          </Text>
        </div>
        <Button type="primary" icon={<FundOutlined />}>
          Nuevo Reporte
        </Button>
      </Row>
      
      <Alert
        message="Módulo en Desarrollo"
        description="Este módulo permitirá analizar datos empresariales y generar reportes estratégicos para la toma de decisiones."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Reportes Activos" 
              value={24} 
              prefix={<BarChartOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="KPIs Monitoreados" 
              value={48} 
              prefix={<DotChartOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Alertas Activas" 
              value={3} 
              prefix={<BarChartOutlined />} 
              valueStyle={{ color: '#fa8c16' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Datos Procesados" 
              value="2.4M+" 
              prefix={<FundOutlined />} 
              valueStyle={{ color: '#52c41a' }} 
            />
          </Card>
        </Col>
      </Row>

      <Card className="dashboard-card">
        <Table dataSource={kpis} columns={columns} />
      </Card>
    </div>
  );
};

export default BusinessIntelligenceDashboard;