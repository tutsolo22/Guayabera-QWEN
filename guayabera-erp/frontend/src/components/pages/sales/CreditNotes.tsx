import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, Tabs, Divider, Tag, DatePicker, InputNumber, Statistic } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  FileTextOutlined,
  PercentageOutlined,
  FileProtectOutlined,
  CheckCircleOutlined,
  SwapOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

const CreditNotes: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [activeTab, setActiveTab] = useState('notes');
  const [form] = Form.useForm();
  
  // Datos simulados para notas de crédito
  const noteData = [
    { id: '1', folio: 'NC-2023-001', cliente: 'Moda S.A.', factura_relacionada: 'FAC-2023-050', fecha: '2023-04-10', total: 12500, motivo: 'Devolución', estado: 'emitida' },
    { id: '2', folio: 'NC-2023-002', cliente: 'Tendencias SA', factura_relacionada: 'FAC-2023-055', fecha: '2023-04-12', total: 8200, motivo: 'Cancelación', estado: 'procesada' },
    { id: '3', folio: 'NC-2023-003', cliente: 'Distribuciones XYZ', factura_relacionada: 'FAC-2023-060', fecha: '2023-04-15', total: 15600, motivo: 'Devolución', estado: 'pendiente' },
    { id: '4', folio: 'NC-2023-004', cliente: 'Ropa al Por Mayor', factura_relacionada: 'FAC-2023-065', fecha: '2023-04-18', total: 6500, motivo: 'Error Facturación', estado: 'emitida' },
  ];

  // Datos simulados para devoluciones
  const returnData = [
    { id: '1', folio: 'DEV-2023-001', cliente: 'Moda S.A.', factura_relacionada: 'FAC-2023-050', productos: '5 camisas', fecha: '2023-04-08', estado: 'autorizada' },
    { id: '2', folio: 'DEV-2023-002', cliente: 'Tendencias SA', factura_relacionada: 'FAC-2023-055', productos: '3 pantalones', fecha: '2023-04-10', estado: 'procesada' },
  ];

  const columnasNotas = [
    { title: 'Folio', dataIndex: 'folio', key: 'folio' },
    { title: 'Cliente', dataIndex: 'cliente', key: 'cliente' },
    { title: 'Factura Relacionada', dataIndex: 'factura_relacionada', key: 'factura_relacionada' },
    { title: 'Fecha', dataIndex: 'fecha', key: 'fecha' },
    { 
      title: 'Total', 
      dataIndex: 'total', 
      key: 'total',
      render: (total: number) => `$${total.toLocaleString()}`
    },
    { 
      title: 'Motivo', 
      dataIndex: 'motivo', 
      key: 'motivo',
      render: (motivo: string) => {
        let color = 'default';
        if (motivo === 'Devolución') color = 'orange';
        if (motivo === 'Cancelación') color = 'red';
        if (motivo === 'Error Facturación') color = 'blue';
        return <Tag color={color}>{motivo}</Tag>;
      }
    },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'pendiente') color = 'orange';
        if (estado === 'emitida') color = 'blue';
        if (estado === 'procesada') color = 'green';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link" icon={<EditOutlined />}>Editar</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Eliminar</Button>
          <Button type="link" icon={<FileTextOutlined />}>Imprimir</Button>
        </Space>
      ),
    },
  ];

  const columnasDevoluciones = [
    { title: 'Folio', dataIndex: 'folio', key: 'folio' },
    { title: 'Cliente', dataIndex: 'cliente', key: 'cliente' },
    { title: 'Factura Relacionada', dataIndex: 'factura_relacionada', key: 'factura_relacionada' },
    { title: 'Productos', dataIndex: 'productos', key: 'productos' },
    { title: 'Fecha', dataIndex: 'fecha', key: 'fecha' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'pendiente') color = 'orange';
        if (estado === 'autorizada') color = 'blue';
        if (estado === 'procesada') color = 'green';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link" icon={<EditOutlined />}>Editar</Button>
          <Button type="link" icon={<SwapOutlined />}>Generar Nota</Button>
        </Space>
      ),
    },
  ];

  const handleCrearNota = () => {
    setModalVisible(true);
  };

  const handleGuardarNota = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear nota de crédito:', error);
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><FileProtectOutlined /> Notas de Crédito Automáticas</Title>
          <Text>
            Generación automática de notas de crédito por devoluciones o cancelaciones
          </Text>
        </div>
        <Space>
          <Button icon={<PlusOutlined />} onClick={handleCrearNota}>
            Nueva Nota de Crédito
          </Button>
        </Space>
      </Row>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Notas Emitidas"
              value={42}
              prefix={<FileTextOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total Devuelto"
              value={285600}
              precision={2}
              prefix={<SwapOutlined />}
              suffix="MXN"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Autenticación SAT"
              value={100}
              precision={0}
              prefix={<CheckCircleOutlined />}
              suffix="%"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Procesadas"
              value={38}
              prefix={<FileProtectOutlined />}
            />
          </Card>
        </Col>
      </Row>

      <Tabs defaultActiveKey="notes" onChange={setActiveTab}>
        <TabPane tab="Notas de Crédito" key="notes">
          <Card className="dashboard-card">
            <Table 
              dataSource={noteData} 
              columns={columnasNotas} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Devoluciones Autorizadas" key="returns">
          <Card className="dashboard-card">
            <Table 
              dataSource={returnData} 
              columns={columnasDevoluciones} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
      </Tabs>

      <Modal
        title="Crear Nueva Nota de Crédito"
        open={modalVisible}
        onCancel={() => {
          setModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={800}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleGuardarNota}
        >
          <Form.Item name="folio" label="Folio de la Nota" rules={[{ required: true, message: 'Ingrese el folio de la nota' }]}>
            <Input placeholder="Ej: NC-2023-001" />
          </Form.Item>
          
          <Form.Item name="cliente" label="Cliente" rules={[{ required: true, message: 'Seleccione el cliente' }]}>
            <Select placeholder="Seleccione el cliente">
              <Option value="moda_sa">Moda S.A.</Option>
              <Option value="tendencias_sa">Tendencias SA</Option>
              <Option value="distribuciones_xyz">Distribuciones XYZ</Option>
              <Option value="ropa_al_por_mayor">Ropa al Por Mayor</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="factura_relacionada" label="Factura Relacionada" rules={[{ required: true, message: 'Seleccione la factura relacionada' }]}>
            <Select placeholder="Seleccione la factura relacionada">
              <Option value="fac-2023-050">FAC-2023-050 - Moda S.A.</Option>
              <Option value="fac-2023-055">FAC-2023-055 - Tendencias SA</Option>
              <Option value="fac-2023-060">FAC-2023-060 - Distribuciones XYZ</Option>
              <Option value="fac-2023-065">FAC-2023-065 - Ropa al Por Mayor</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="motivo" label="Motivo de la Nota" rules={[{ required: true, message: 'Seleccione el motivo de la nota' }]}>
            <Select placeholder="Seleccione el motivo de la nota">
              <Option value="devolucion">Devolución de Mercancía</Option>
              <Option value="cancelacion">Cancelación de Factura</Option>
              <Option value="error_facturacion">Error en Facturación</Option>
              <Option value="descuento">Aplicación de Descuento</Option>
              <Option value="otros">Otros</Option>
            </Select>
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="fecha" label="Fecha de Emisión" rules={[{ required: true, message: 'Seleccione la fecha de emisión' }]}>
                <Input type="date" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="total" label="Total de la Nota" rules={[{ required: true, message: 'Ingrese el total de la nota' }]}>
                <InputNumber 
                  placeholder="Total de la nota de crédito"
                  style={{ width: '100%' }}
                  formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                  parser={value => value!.replace(/\$\s?|(,*)/g, '')}
                />
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="productos" label="Productos a Devolver">
            <Select 
              mode="multiple" 
              placeholder="Seleccione los productos a devolver"
              allowClear
            >
              <Option value="camisa_casual">Camisa Casual</Option>
              <Option value="pantalon_jeans">Pantalón Jeans</Option>
              <Option value="vestido_fiesta">Vestido de Fiesta</Option>
              <Option value="chaqueta_formal">Chaqueta Formal</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="observaciones" label="Observaciones">
            <TextArea placeholder="Observaciones adicionales sobre la nota de crédito" rows={4} />
          </Form.Item>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setModalVisible(false);
                form.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>
                Crear Nota de Crédito
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default CreditNotes;