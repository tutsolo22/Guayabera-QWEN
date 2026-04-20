import React, { useState } from 'react';
import { Table, Button, Modal, Form, Input, message, Typography, Statistic, Row, Col, Card } from 'antd';
import { PlusOutlined, WalletOutlined } from '@ant-design/icons';
import { useGetBancosQuery, useCreateBancoMutation } from '../../../services/financeApi';

const { Title } = Typography;

const BancosPage: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [form] = Form.useForm();
  const { data: bancos, isLoading } = useGetBancosQuery();
  const [createBanco] = useCreateBancoMutation();

  const handleCreate = async (values: any) => {
    try {
      await createBanco(values).unwrap();
      message.success('Banco creado exitosamente');
      setModalVisible(false);
      form.resetFields();
    } catch (error: any) {
      message.error('Error creando banco');
    }
  };

  const totalSaldo = bancos?.reduce((sum, b) => sum + b.saldo_actual, 0) || 0;

  const columns = [
    { title: 'Banco', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Cuenta', dataIndex: 'cuenta', key: 'cuenta' },
    { title: 'CLABE', dataIndex: 'clabe', key: 'clabe' },
    { title: 'Moneda', dataIndex: 'moneda', key: 'moneda', width: 100 },
    {
      title: 'Saldo',
      dataIndex: 'saldo_actual',
      key: 'saldo_actual',
      render: (saldo: number) => `$${saldo.toLocaleString('es-MX', { minimumFractionDigits: 2 })}`,
    },
  ];

  return (
    <div>
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={8}>
          <Card>
            <Statistic
              title="Total Bancos"
              value={bancos?.length || 0}
              prefix={<WalletOutlined />}
            />
          </Card>
        </Col>
        <Col span={16}>
          <Card>
            <Statistic
              title="Saldo Total en Bancos"
              value={totalSaldo}
              precision={2}
              prefix="$"
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
      </Row>

      <div className="table-header">
        <Title level={3}>Cuentas Bancarias</Title>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => setModalVisible(true)}>
          Nuevo Banco
        </Button>
      </div>

      <Table columns={columns} dataSource={bancos || []} rowKey="id" loading={isLoading} />

      <Modal
        title="Nuevo Banco"
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
      >
        <Form form={form} layout="vertical" onFinish={handleCreate}>
          <Form.Item name="nombre" label="Nombre" rules={[{ required: true }]}>
            <Input placeholder="Ej: BBVA" />
          </Form.Item>
          <Form.Item name="cuenta" label="Número de Cuenta" rules={[{ required: true }]}>
            <Input placeholder="1234567890" />
          </Form.Item>
          <Form.Item name="clabe" label="CLABE">
            <Input placeholder="123456789012345678" maxLength={18} />
          </Form.Item>
          <Form.Item name="saldo_actual" label="Saldo Inicial">
            <Input type="number" placeholder="0.00" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" block>Crear Banco</Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default BancosPage;
