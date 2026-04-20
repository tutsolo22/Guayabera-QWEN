import React, { useState } from 'react';
import { Table, DatePicker, Button, Typography, Card, Row, Col, Statistic, Tag } from 'antd';
import { CalculatorOutlined } from '@ant-design/icons';
import { useGetBalanzaComprobacionQuery } from '../../../services/financeApi';
import dayjs from 'dayjs';

const { Title } = Typography;
const { RangePicker } = DatePicker;

const BalanzaPage: React.FC = () => {
  const [dateRange, setDateRange] = useState<[dayjs.Dayjs, dayjs.Dayjs] | null>(null);

  const { data: balanza, isLoading } = useGetBalanzaComprobacionQuery(
    {
      fecha_desde: dateRange?.[0]?.format('YYYY-MM-DD') || dayjs().startOf('month').format('YYYY-MM-DD'),
      fecha_hasta: dateRange?.[1]?.format('YYYY-MM-DD') || dayjs().endOf('month').format('YYYY-MM-DD'),
    },
    { skip: !dateRange }
  );

  const columns = [
    { title: 'Cuenta', dataIndex: 'cuenta_codigo', key: 'cuenta_codigo', width: 150 },
    { title: 'Nombre', dataIndex: 'cuenta_nombre', key: 'cuenta_nombre', ellipsis: true },
    {
      title: 'Tipo',
      dataIndex: 'tipo',
      key: 'tipo',
      width: 100,
      render: (tipo: string) => <Tag>{tipo.toUpperCase()}</Tag>,
    },
    {
      title: 'Saldo Inicial',
      dataIndex: 'saldo_inicial',
      key: 'saldo_inicial',
      width: 150,
      render: (val: number) => `$${val.toFixed(2)}`,
    },
    {
      title: 'Cargos',
      dataIndex: 'cargos',
      key: 'cargos',
      width: 150,
      render: (val: number) => `$${val.toFixed(2)}`,
    },
    {
      title: 'Abonos',
      dataIndex: 'abonos',
      key: 'abonos',
      width: 150,
      render: (val: number) => `$${val.toFixed(2)}`,
    },
    {
      title: 'Saldo Final',
      dataIndex: 'saldo_final',
      key: 'saldo_final',
      width: 150,
      render: (val: number) => <strong>${val.toFixed(2)}</strong>,
    },
  ];

  return (
    <div>
      <div className="table-header">
        <Title level={3}>Balanza de Comprobación</Title>
        <RangePicker
          onChange={(dates) => setDateRange(dates as any)}
          defaultValue={[dayjs().startOf('month'), dayjs().endOf('month')]}
        />
      </div>

      {balanza && (
        <Row gutter={16} style={{ marginBottom: 24 }}>
          <Col span={8}>
            <Card>
              <Statistic title="Total Cargos" value={balanza.total_cargos} precision={2} prefix="$" />
            </Card>
          </Col>
          <Col span={8}>
            <Card>
              <Statistic title="Total Abonos" value={balanza.total_abonos} precision={2} prefix="$" />
            </Card>
          </Col>
          <Col span={8}>
            <Card>
              <Statistic
                title="Estado"
                value={balanza.esta_cuadrada ? '✅ Cuadrada' : '❌ No Cuadrada'}
                valueStyle={{ color: balanza.esta_cuadrada ? '#52c41a' : '#ff4d4f' }}
              />
            </Card>
          </Col>
        </Row>
      )}

      <Table
        columns={columns}
        dataSource={balanza?.lineas || []}
        rowKey="cuenta_id"
        loading={isLoading}
        pagination={false}
        scroll={{ x: 1200 }}
        summary={() => balanza && (
          <Table.Summary>
            <Table.Summary.Row>
              <Table.Summary.Cell index={0} colSpan={3}><strong>Totales</strong></Table.Summary.Cell>
              <Table.Summary.Cell index={3}><strong>${balanza.total_cargos.toFixed(2)}</strong></Table.Summary.Cell>
              <Table.Summary.Cell index={4}><strong>${balanza.total_abonos.toFixed(2)}</strong></Table.Summary.Cell>
              <Table.Summary.Cell index={5}></Table.Summary.Cell>
            </Table.Summary.Row>
          </Table.Summary>
        )}
      />
    </div>
  );
};

export default BalanzaPage;
