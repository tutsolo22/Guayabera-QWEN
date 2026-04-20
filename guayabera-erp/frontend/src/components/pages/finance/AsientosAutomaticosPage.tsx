puedesimport React from 'react';
import { Table, Typography, Tag, Card, Row, Col, Statistic, Spin } from 'antd';
import { SyncOutlined, CheckCircleOutlined, CloseCircleOutlined, ClockCircleOutlined } from '@ant-design/icons';
import { useGetAsientosAutomaticosQuery, useGetAsientosEstadisticasQuery } from '../../../services/financeApi';
import dayjs from 'dayjs';

const { Title } = Typography;

const AsientosAutomaticosPage: React.FC = () => {
  const { data: asientos, isLoading } = useGetAsientosAutomaticosQuery();
  const { data: stats, isLoading: loadingStats } = useGetAsientosEstadisticasQuery({});

  const columns = [
    { title: 'Módulo', dataIndex: 'modulo_origen', key: 'modulo_origen', width: 120 },
    { title: 'Entidad', dataIndex: 'entidad_origen', key: 'entidad_origen', width: 150 },
    { title: 'Referencia', dataIndex: 'referencia', key: 'referencia', width: 150 },
    {
      title: 'Estado',
      dataIndex: 'estado',
      key: 'estado',
      width: 150,
      render: (estado: string) => {
        const config: any = {
          procesado: { color: 'success', icon: <CheckCircleOutlined />, text: 'PROCESADO' },
          pendiente: { color: 'processing', icon: <ClockCircleOutlined />, text: 'PENDIENTE' },
          fallido: { color: 'error', icon: <CloseCircleOutlined />, text: 'FALLIDO' },
          requiere_intervencion: { color: 'warning', icon: <CloseCircleOutlined />, text: 'REQUIERE ATENCIÓN' },
        };
        const { color, icon, text } = config[estado] || config.pendiente;
        return <Tag color={color} icon={icon}>{text}</Tag>;
      },
    },
    {
      title: 'Fecha Creación',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (fecha: string) => dayjs(fecha).format('DD/MM/YYYY HH:mm'),
    },
    {
      title: 'Fecha Proceso',
      dataIndex: 'fecha_procesado',
      key: 'fecha_procesado',
      render: (fecha: string) => fecha ? dayjs(fecha).format('DD/MM/YYYY HH:mm') : '-',
    },
  ];

  if (loadingStats) {
    return <Spin size="large" />;
  }

  return (
    <div>
      <Title level={3}>
        <SyncOutlined spin /> Asientos Automáticos
      </Title>

      {stats && (
        <Row gutter={16} style={{ marginBottom: 24 }}>
          <Col span={6}>
            <Card>
              <Statistic
                title="Procesados"
                value={stats.by_status?.procesado || 0}
                valueStyle={{ color: '#52c41a' }}
                prefix={<CheckCircleOutlined />}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="Pendientes"
                value={stats.by_status?.pendiente || 0}
                valueStyle={{ color: '#faad14' }}
                prefix={<ClockCircleOutlined />}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="Fallidos"
                value={stats.by_status?.fallido || 0}
                valueStyle={{ color: '#ff4d4f' }}
                prefix={<CloseCircleOutlined />}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="Últimas 24h"
                value={stats.last_24h || 0}
                prefix={<SyncOutlined />}
              />
            </Card>
          </Col>
        </Row>
      )}

      <Table
        columns={columns}
        dataSource={asientos || []}
        rowKey="id"
        loading={isLoading}
        pagination={{ pageSize: 20 }}
      />
    </div>
  );
};

export default AsientosAutomaticosPage;
