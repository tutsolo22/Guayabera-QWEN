import React from 'react';
import { Row, Col, Card, Statistic, Table, Typography, Tag, Spin } from 'antd';
import {
  BankOutlined,
  FileTextOutlined,
  WalletOutlined,
  SyncOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
} from '@ant-design/icons';
import { useGetCuentasQuery, useGetPolizasQuery, useGetBancosQuery, useGetAsientosEstadisticasQuery } from '../../services/financeApi';
import dayjs from 'dayjs';

const { Title } = Typography;

const DashboardPage: React.FC = () => {
  const { data: cuentas, isLoading: loadingCuentas } = useGetCuentasQuery();
  const { data: polizas, isLoading: loadingPolizas } = useGetPolizasQuery();
  const { data: bancos, isLoading: loadingBancos } = useGetBancosQuery();
    const { data: asientosStats, isLoading: loadingAsientos } = useGetAsientosEstadisticasQuery({});

  const totalCuentas = cuentas?.length || 0;
  const totalPolizas = polizas?.length || 0;
  const totalBancos = bancos?.length || 0;
  const asientosHoy = asientosStats?.last_24h || 0;

  const recentPolizas = polizas?.slice(0, 5) || [];

  const columns = [
    {
      title: 'Número',
      dataIndex: 'numero',
      key: 'numero',
      render: (num: number) => <strong>#{num}</strong>,
    },
    {
      title: 'Tipo',
      dataIndex: 'tipo',
      key: 'tipo',
      render: (tipo: string) => {
        const colors: any = { diario: 'blue', ingreso: 'green', egreso: 'orange' };
        return <Tag color={colors[tipo]}>{tipo.toUpperCase()}</Tag>;
      },
    },
    {
      title: 'Fecha',
      dataIndex: 'fecha',
      key: 'fecha',
      render: (fecha: string) => dayjs(fecha).format('DD/MM/YYYY'),
    },
    {
      title: 'Descripción',
      dataIndex: 'descripcion',
      key: 'descripcion',
      ellipsis: true,
    },
    {
      title: 'Estado',
      dataIndex: 'estado',
      key: 'estado',
      render: (estado: string) => {
        const colors: any = {
          borrador: 'default',
          revisada: 'processing',
          aprobada: 'success',
          cancelada: 'error',
        };
        return <Tag color={colors[estado]}>{estado.toUpperCase()}</Tag>;
      },
    },
    {
      title: 'Total',
      dataIndex: 'total_cargos',
      key: 'total_cargos',
      render: (total: number) => `$${total.toLocaleString('es-MX', { minimumFractionDigits: 2 })}`,
    },
  ];

  if (loadingCuentas || loadingPolizas || loadingBancos || loadingAsientos) {
    return (
      <div style={{ textAlign: 'center', padding: '100px 0' }}>
        <Spin size="large" tip="Cargando dashboard..." />
      </div>
    );
  }

  return (
    <div>
      <Title level={3} style={{ marginBottom: 24 }}>Dashboard General</Title>

      {/* Statistics Cards */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} lg={6}>
          <Card className="stat-card" hoverable>
            <Statistic
              title="Cuentas Contables"
              value={totalCuentas}
              prefix={<BankOutlined />}
              suffix={totalCuentas > 0 ? <ArrowUpOutlined style={{ color: '#52c41a' }} /> : null}
              valueStyle={{ color: '#1890ff' }}
            />
            <div className="stat-card-label">Catálogo SAT importado</div>
          </Card>
        </Col>

        <Col xs={24} sm={12} lg={6}>
          <Card className="stat-card" hoverable>
            <Statistic
              title="Pólizas Registradas"
              value={totalPolizas}
              prefix={<FileTextOutlined />}
              valueStyle={{ color: '#722ed1' }}
            />
            <div className="stat-card-label">Diario, ingreso y egreso</div>
          </Card>
        </Col>

        <Col xs={24} sm={12} lg={6}>
          <Card className="stat-card" hoverable>
            <Statistic
              title="Cuentas Bancarias"
              value={totalBancos}
              prefix={<WalletOutlined />}
              valueStyle={{ color: '#fa8c16' }}
            />
            <div className="stat-card-label">Bancos activos</div>
          </Card>
        </Col>

        <Col xs={24} sm={12} lg={6}>
          <Card className="stat-card" hoverable>
            <Statistic
              title="Asientos Hoy"
              value={asientosHoy}
              prefix={<SyncOutlined spin={asientosHoy > 0} />}
              valueStyle={{ color: asientosHoy > 0 ? '#52c41a' : '#666' }}
            />
            <div className="stat-card-label">Asientos automáticos (24h)</div>
          </Card>
        </Col>
      </Row>

      {/* Automatic Accounting Status */}
      {asientosStats && (
        <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
          <Col span={24}>
            <Card title="Estado de Asientos Automáticos" bordered={false}>
              <Row gutter={16}>
                <Col span={6}>
                  <Statistic
                    title="Procesados"
                    value={asientosStats.by_status?.procesado || 0}
                    valueStyle={{ color: '#52c41a' }}
                  />
                </Col>
                <Col span={6}>
                  <Statistic
                    title="Pendientes"
                    value={asientosStats.by_status?.pendiente || 0}
                    valueStyle={{ color: '#faad14' }}
                  />
                </Col>
                <Col span={6}>
                  <Statistic
                    title="Fallidos"
                    value={asientosStats.by_status?.fallido || 0}
                    valueStyle={{ color: '#ff4d4f' }}
                  />
                </Col>
                <Col span={6}>
                  <Statistic
                    title="Requieren Atención"
                    value={asientosStats.requires_intervention || 0}
                    valueStyle={{ color: '#ff4d4f' }}
                  />
                </Col>
              </Row>
            </Card>
          </Col>
        </Row>
      )}

      {/* Recent Policies Table */}
      <Card title="Pólizas Recientes" bordered={false}>
        <Table
          columns={columns}
          dataSource={recentPolizas}
          rowKey="id"
          pagination={false}
          locale={{ emptyText: 'No hay pólizas registradas' }}
        />
      </Card>
    </div>
  );
};

export default DashboardPage;
