import React, { useState } from 'react';
import { Card, Row, Col, Statistic, Table, Button, Space, Typography, Tag, Modal, Form, Input, Select, DatePicker, message } from 'antd';
import { 
  PlusOutlined, 
  ShoppingCartOutlined, 
  FileTextOutlined, 
  ShopOutlined, 
  UserOutlined, 
  CheckCircleOutlined, 
  CloseCircleOutlined,
  EditOutlined,
  DeleteOutlined,
  SearchOutlined
} from '@ant-design/icons';

const { Title } = Typography;
const { Option } = Select;
const { RangePicker } = DatePicker;

const PurchasesDashboard: React.FC = () => {
  const [purchases, setPurchases] = useState<any[]>([
    { 
      key: '1', 
      id: 'COMP-001', 
      proveedor: 'Proveedor Textil Sureño', 
      solicitante: 'Carlos Ramírez', 
      total: 45000, 
      estado: 'Autorizada', 
      fecha_solicitud: '2023-04-01',
      fecha_entrega: '2023-04-10',
      prioridad: 'Alta'
    },
    { 
      key: '2', 
      id: 'COMP-002', 
      proveedor: 'Distribuidora Maya', 
      solicitante: 'Ana López', 
      total: 28500, 
      estado: 'Pendiente', 
      fecha_solicitud: '2023-04-02',
      fecha_entrega: '2023-04-15',
      prioridad: 'Media'
    },
    { 
      key: '3', 
      id: 'COMP-003', 
      proveedor: 'Importaciones del Norte', 
      solicitante: 'José Martínez', 
      total: 32000, 
      estado: 'Rechazada', 
      fecha_solicitud: '2023-04-01',
      fecha_entrega: '2023-04-12',
      prioridad: 'Baja'
    },
    { 
      key: '4', 
      id: 'COMP-004', 
      proveedor: 'Comercial Textil Yucateca', 
      solicitante: 'Luisa Gómez', 
      total: 18750, 
      estado: 'Entregada', 
      fecha_solicitud: '2023-03-28',
      fecha_entrega: '2023-04-05',
      prioridad: 'Alta'
    },
  ]);
  
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [currentPurchase, setCurrentPurchase] = useState<any>(null);
  const [form] = Form.useForm();

  const columns = [
    { title: 'ID Compra', dataIndex: 'id', key: 'id' },
    { title: 'Proveedor', dataIndex: 'proveedor', key: 'proveedor' },
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
        if (estado === 'Autorizada') color = 'blue';
        if (estado === 'Pendiente') color = 'orange';
        if (estado === 'Rechazada') color = 'red';
        if (estado === 'Entregada') color = 'green';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { title: 'Fecha Solicitud', dataIndex: 'fecha_solicitud', key: 'fecha_solicitud' },
    { title: 'Fecha Entrega', dataIndex: 'fecha_entrega', key: 'fecha_entrega' },
    { 
      title: 'Prioridad', 
      dataIndex: 'prioridad', 
      key: 'prioridad',
      render: (prioridad: string) => {
        let color = 'default';
        if (prioridad === 'Alta') color = 'red';
        if (prioridad === 'Media') color = 'orange';
        if (prioridad === 'Baja') color = 'green';
        return <Tag color={color}>{prioridad}</Tag>;
      }
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: (_, record) => (
        <Space size="middle">
          <Button 
            type="link" 
            icon={<SearchOutlined />}
          >
            Ver Detalles
          </Button>
          <Button 
            type="link" 
            icon={<EditOutlined />}
            disabled={record.estado !== 'Pendiente'}
          >
            Editar
          </Button>
          <Button 
            type="link" 
            danger
            icon={<DeleteOutlined />}
            disabled={record.estado !== 'Pendiente'}
          >
            Eliminar
          </Button>
        </Space>
      ),
    },
  ];

  const handleNewPurchase = () => {
    setCurrentPurchase(null);
    form.resetFields();
    setIsModalVisible(true);
  };

  const handleSave = () => {
    form.validateFields().then(values => {
      // En una implementación real, aquí se haría la llamada al API
      message.success('Compra creada exitosamente');
      setIsModalVisible(false);
      form.resetFields();
      setCurrentPurchase(null);
    });
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <Title level={2}>Módulo de Compras</Title>
        <Button 
          type="primary" 
          icon={<PlusOutlined />} 
          onClick={handleNewPurchase}
        >
          Nueva Compra
        </Button>
      </Row>
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Total Compras" 
              value={purchases.length} 
              prefix={<ShoppingCartOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Pendientes" 
              value={purchases.filter(p => p.estado === 'Pendiente').length} 
              prefix={<FileTextOutlined />} 
              valueStyle={{ color: '#fa8c16' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Autorizadas" 
              value={purchases.filter(p => p.estado === 'Autorizada').length} 
              prefix={<CheckCircleOutlined />} 
              valueStyle={{ color: '#52c41a' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Valor Total" 
              value="$124.25K" 
              prefix={<FileTextOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
      </Row>

      <Card className="dashboard-card">
        <Table 
          dataSource={purchases} 
          columns={columns} 
          pagination={{ pageSize: 10 }}
          scroll={{ x: 1200 }}
        />
      </Card>

      <Modal
        title="Nueva Solicitud de Compra"
        open={isModalVisible}
        onOk={handleSave}
        onCancel={() => {
          setIsModalVisible(false);
          form.resetFields();
          setCurrentPurchase(null);
        }}
        okText="Guardar"
        cancelText="Cancelar"
        width={800}
      >
        <Form
          form={form}
          layout="vertical"
          name="purchase_form"
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="proveedor"
                label="Proveedor"
                rules={[{ required: true, message: 'Por favor seleccione un proveedor' }]}
              >
                <Select placeholder="Seleccione un proveedor">
                  <Option value="Proveedor Textil Sureño">Proveedor Textil Sureño</Option>
                  <Option value="Distribuidora Maya">Distribuidora Maya</Option>
                  <Option value="Importaciones del Norte">Importaciones del Norte</Option>
                  <Option value="Comercial Textil Yucateca">Comercial Textil Yucateca</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="solicitante"
                label="Solicitante"
                rules={[{ required: true, message: 'Por favor seleccione al solicitante' }]}
              >
                <Select placeholder="Seleccione al solicitante">
                  <Option value="Carlos Ramírez">Carlos Ramírez</Option>
                  <Option value="Ana López">Ana López</Option>
                  <Option value="José Martínez">José Martínez</Option>
                  <Option value="Luisa Gómez">Luisa Gómez</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="fecha_solicitud"
                label="Fecha de Solicitud"
                rules={[{ required: true, message: 'Por favor seleccione la fecha' }]}
              >
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="fecha_entrega"
                label="Fecha de Entrega Esperada"
                rules={[{ required: true, message: 'Por favor seleccione la fecha' }]}
              >
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item
            name="descripcion"
            label="Descripción de la Compra"
            rules={[{ required: true, message: 'Por favor ingrese la descripción' }]}
          >
            <Input.TextArea rows={4} placeholder="Detalle los artículos o servicios a comprar..." />
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="monto"
                label="Monto Estimado"
                rules={[
                  { required: true, message: 'Por favor ingrese el monto' },
                  { pattern: /^\d+(\.\d{1,2})?$/, message: 'Ingrese un monto válido' }
                ]}
              >
                <Input prefix="$" placeholder="0.00" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="prioridad"
                label="Prioridad"
                rules={[{ required: true, message: 'Por favor seleccione la prioridad' }]}
              >
                <Select placeholder="Seleccione la prioridad">
                  <Option value="Baja">Baja</Option>
                  <Option value="Media">Media</Option>
                  <Option value="Alta">Alta</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default PurchasesDashboard;