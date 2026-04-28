import React, { useState } from 'react';
import { Card, Row, Col, Table, Button, Space, Typography, Tag, Modal, Form, Input, Select, DatePicker, InputNumber, Tabs, Divider, message, Steps } from 'antd';
import { 
  ScanOutlined, 
  FileSearchOutlined, 
  CalculatorOutlined,
  CheckCircleOutlined,
  ExclamationCircleOutlined,
  PlusOutlined,
  UploadOutlined,
  ReloadOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { Option } = Select;
const { Step } = Steps;

interface ProductoToma {
  key: string;
  codigo: string;
  nombre: string;
  modelo: string;
  color: string;
  talla: string;
  cantidadSistema: number;
  cantidadFisica: number;
  diferencia: number;
}

interface MovimientoInventario {
  key: string;
  tipo: string;
  producto: string;
  cantidad: number;
  fecha: string;
  responsable: string;
  motivo: string;
}

const TomaInventario: React.FC = () => {
  const [tomaModalVisible, setTomaModalVisible] = useState(false);
  const [ajusteModalVisible, setAjusteModalVisible] = useState(false);
  const [movimientoModalVisible, setMovimientoModalVisible] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [form] = Form.useForm();
  
  // Datos simulados para productos en la toma
  const productosToma: ProductoToma[] = [
    { key: '1', codigo: 'PROD-001', nombre: 'Camisa Guayabera Azul', modelo: 'Guayabera', color: 'Azul Marino', talla: 'M', cantidadSistema: 25, cantidadFisica: 23, diferencia: -2 },
    { key: '2', codigo: 'PROD-002', nombre: 'Pantalón Jeans Negro', modelo: 'Jeans', color: 'Negro', talla: '32', cantidadSistema: 15, cantidadFisica: 17, diferencia: 2 },
    { key: '3', codigo: 'PROD-003', nombre: 'Blusa Seda Rosa', modelo: 'Blusa', color: 'Rosado', talla: 'S', cantidadSistema: 8, cantidadFisica: 5, diferencia: -3 },
    { key: '4', codigo: 'PROD-004', nombre: 'Vestido Verano Estampado', modelo: 'Vestido', color: 'Multicolor', talla: 'L', cantidadSistema: 12, cantidadFisica: 12, diferencia: 0 },
  ];

  const movimientosData: MovimientoInventario[] = [
    { key: '1', tipo: 'ajuste_negativo', producto: 'Camisa Guayabera Azul', cantidad: 2, fecha: '2023-04-15', responsable: 'Carlos Ramírez', motivo: 'Diferencia en conteo físico' },
    { key: '2', tipo: 'ajuste_positivo', producto: 'Pantalón Jeans Negro', cantidad: 2, fecha: '2023-04-15', responsable: 'Carlos Ramírez', motivo: 'Diferencia en conteo físico' },
    { key: '3', tipo: 'entrada_ajuste', producto: 'Vestido Verano Estampado', cantidad: 5, fecha: '2023-04-14', responsable: 'Ana Gómez', motivo: 'Recepción de mercancía faltante' },
  ];

  const columnasProductos = [
    { title: 'Código', dataIndex: 'codigo', key: 'codigo' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Modelo', dataIndex: 'modelo', key: 'modelo' },
    { title: 'Color', dataIndex: 'color', key: 'color' },
    { title: 'Talla', dataIndex: 'talla', key: 'talla' },
    { 
      title: 'Cant. Sistema', 
      dataIndex: 'cantidadSistema', 
      key: 'cantidadSistema',
      render: (cantidad: number) => <Tag color="blue">{cantidad}</Tag>
    },
    { 
      title: 'Cant. Física', 
      dataIndex: 'cantidadFisica', 
      key: 'cantidadFisica',
      render: (cantidad: number) => <Tag color="green">{cantidad}</Tag>
    },
    { 
      title: 'Diferencia', 
      dataIndex: 'diferencia', 
      key: 'diferencia',
      render: (diferencia: number) => (
        <Tag color={diferencia === 0 ? 'success' : diferencia > 0 ? 'warning' : 'error'}>
          {diferencia > 0 ? '+' : ''}{diferencia}
        </Tag>
      )
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link">Detalles</Button>
        </Space>
      ),
    },
  ];

  const columnasMovimientos = [
    { title: 'Tipo', dataIndex: 'tipo', key: 'tipo' },
    { title: 'Producto', dataIndex: 'producto', key: 'producto' },
    { title: 'Cantidad', dataIndex: 'cantidad', key: 'cantidad' },
    { title: 'Fecha', dataIndex: 'fecha', key: 'fecha' },
    { title: 'Responsable', dataIndex: 'responsable', key: 'responsable' },
    { title: 'Motivo', dataIndex: 'motivo', key: 'motivo' },
  ];

  const steps = [
    {
      title: 'Crear Toma',
      icon: <FileSearchOutlined />,
    },
    {
      title: 'Registrar Productos',
      icon: <ScanOutlined />,
    },
    {
      title: 'Comparar Inventario',
      icon: <CalculatorOutlined />,
    },
    {
      title: 'Aplicar Ajustes',
      icon: <CheckCircleOutlined />,
    },
  ];

  const handleIniciarToma = () => {
    setCurrentStep(0);
    setTomaModalVisible(true);
  };

  const handleAgregarProducto = () => {
    message.info('Funcionalidad de escaneo no implementada en esta demo');
  };

  const handleCompararInventario = () => {
    message.success('Comparación de inventario completada');
    setCurrentStep(2);
  };

  const handleAjustarInventario = () => {
    setAjusteModalVisible(true);
  };

  const handleRealizarAjuste = async () => {
    try {
      // Simular ajuste
      message.success('Ajuste de inventario realizado exitosamente');
      setAjusteModalVisible(false);
      setCurrentStep(3);
    } catch (error) {
      message.error('Error al realizar el ajuste de inventario');
    }
  };

  const handleCrearMovimiento = () => {
    setMovimientoModalVisible(true);
  };

  const handleGuardarMovimiento = async () => {
    try {
      const values = await form.validateFields();
      message.success('Movimiento de inventario registrado exitosamente');
      setMovimientoModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al registrar movimiento:', error);
      message.error('Error al registrar el movimiento');
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}>Toma de Inventario</Title>
          <Text>
            Proceso de conteo físico de productos en almacén y comparación con sistema
          </Text>
        </div>
        <Space>
          <Button type="primary" icon={<FileSearchOutlined />} onClick={handleIniciarToma}>
            Nueva Toma
          </Button>
          <Button icon={<ReloadOutlined />} onClick={() => setCurrentStep(0)}>
            Reiniciar Proceso
          </Button>
        </Space>
      </Row>

      <Steps current={currentStep} items={steps} style={{ marginBottom: 24 }} />

      <Card className="dashboard-card">
        <Tabs 
          defaultActiveKey="1" 
          items={[
            {
              label: 'Productos Escaneados',
              key: '1',
              children: (
                <>
                  <Row gutter={16} style={{ marginBottom: 16 }}>
                    <Col span={18}>
                      <Input 
                        placeholder="Escanear código de barras o ingresar manualmente" 
                        addonAfter={
                          <Button icon={<ScanOutlined />} onClick={handleAgregarProducto}>
                            Escanear
                          </Button>
                        } 
                      />
                    </Col>
                    <Col span={6}>
                      <Button 
                        type="primary" 
                        icon={<ExclamationCircleOutlined />}
                        onClick={handleCompararInventario}
                        disabled={currentStep < 1}
                      >
                        Comparar Inventario
                      </Button>
                    </Col>
                  </Row>
                  
                  <Table 
                    dataSource={productosToma} 
                    columns={columnasProductos} 
                    pagination={{ pageSize: 10 }}
                  />
                </>
              ),
            },
            {
              label: 'Diferencias Encontradas',
              key: '2',
              children: (
                <>
                  <Row justify="end" style={{ marginBottom: 16 }}>
                    <Space>
                      <Button 
                        type="primary" 
                        icon={<CheckCircleOutlined />}
                        onClick={handleAjustarInventario}
                        disabled={currentStep < 2}
                      >
                        Realizar Ajuste Automático
                      </Button>
                    </Space>
                  </Row>
                  
                  <Table 
                    dataSource={productosToma.filter(p => p.diferencia !== 0)} 
                    columns={columnasProductos} 
                    pagination={{ pageSize: 10 }}
                  />
                </>
              ),
            },
            {
              label: 'Movimientos de Inventario',
              key: '3',
              children: (
                <>
                  <Row justify="end" style={{ marginBottom: 16 }}>
                    <Button 
                      type="primary" 
                      icon={<PlusOutlined />}
                      onClick={handleCrearMovimiento}
                    >
                      Nuevo Movimiento
                    </Button>
                  </Row>
                  
                  <Table 
                    dataSource={movimientosData} 
                    columns={columnasMovimientos} 
                    pagination={{ pageSize: 10 }}
                  />
                </>
              ),
            },
          ]} 
        />
      </Card>

      <Modal
        title="Nueva Toma de Inventario"
        open={tomaModalVisible}
        onCancel={() => {
          setTomaModalVisible(false);
          setCurrentStep(0);
        }}
        footer={null}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={(values) => {
            message.success('Toma de inventario creada exitosamente');
            setTomaModalVisible(false);
            setCurrentStep(1);
          }}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="almacen" label="Almacén" rules={[{ required: true, message: 'Seleccione un almacén' }]}>
                <Select placeholder="Seleccione almacén">
                  <Option value="principal">Almacén Principal</Option>
                  <Option value="secundario">Almacén Secundario</Option>
                  <Option value="produccion">Almacén de Producción</Option>
                  <Option value="pv">Punto de Venta</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="responsable" label="Responsable" rules={[{ required: true, message: 'Seleccione un responsable' }]}>
                <Select placeholder="Seleccione responsable">
                  <Option value="carlos">Carlos Ramírez</Option>
                  <Option value="ana">Ana Gómez</Option>
                  <Option value="luis">Luis Fernández</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="folio" label="Folio">
            <Input placeholder="Folio se generará automáticamente" disabled />
          </Form.Item>
          
          <Form.Item name="comentarios" label="Comentarios">
            <Input.TextArea placeholder="Comentarios adicionales sobre la toma de inventario" rows={3} />
          </Form.Item>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setTomaModalVisible(false);
                setCurrentStep(0);
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>
                Iniciar Toma
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>

      <Modal
        title="Realizar Ajuste Automático"
        open={ajusteModalVisible}
        onCancel={() => setAjusteModalVisible(false)}
        footer={null}
        width={600}
      >
        <div style={{ textAlign: 'center', padding: '20px 0' }}>
          <ExclamationCircleOutlined style={{ fontSize: '48px', color: '#faad14', marginBottom: '16px' }} />
          <Title level={4}>¿Confirmar ajuste automático?</Title>
          <Text>
            Se aplicarán los ajustes necesarios para igualar las cantidades físicas con las del sistema.
            ¿Desea continuar?
          </Text>
        </div>
        
        <Divider />
        
        <Row justify="end">
          <Space>
            <Button onClick={() => setAjusteModalVisible(false)}>
              Cancelar
            </Button>
            <Button type="primary" onClick={handleRealizarAjuste} icon={<CheckCircleOutlined />}>
              Confirmar Ajuste
            </Button>
          </Space>
        </Row>
      </Modal>

      <Modal
        title="Registrar Movimiento de Inventario"
        open={movimientoModalVisible}
        onCancel={() => {
          setMovimientoModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={700}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleGuardarMovimiento}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="tipo" label="Tipo de Movimiento" rules={[{ required: true, message: 'Seleccione el tipo de movimiento' }]}>
                <Select placeholder="Seleccione tipo de movimiento">
                  <Option value="ajuste_positivo">Entrada por Ajuste de Inventario</Option>
                  <Option value="ajuste_negativo">Salida por Ajuste de Inventario</Option>
                  <Option value="otro_entrada">Entrada por Otros Movimientos</Option>
                  <Option value="otro_salida">Salida por Otros Movimientos</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="producto" label="Producto" rules={[{ required: true, message: 'Seleccione un producto' }]}>
                <Select placeholder="Seleccione producto">
                  <Option value="camisa">Camisa Guayabera Azul</Option>
                  <Option value="pantalon">Pantalón Jeans Negro</Option>
                  <Option value="blusa">Blusa Seda Rosa</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="cantidad" label="Cantidad" rules={[{ required: true, message: 'Ingrese la cantidad' }]}>
                <InputNumber min={1} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="responsable" label="Responsable" rules={[{ required: true, message: 'Seleccione responsable' }]}>
                <Select placeholder="Seleccione responsable">
                  <Option value="carlos">Carlos Ramírez</Option>
                  <Option value="ana">Ana Gómez</Option>
                  <Option value="luis">Luis Fernández</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="motivo" label="Motivo del Movimiento" rules={[{ required: true, message: 'Ingrese el motivo' }]}>
            <Input.TextArea placeholder="Descripción del motivo del movimiento" rows={3} />
          </Form.Item>
          
          <Form.Item name="referencia" label="Referencia (Opcional)">
            <Input placeholder="Número de documento o referencia externa" />
          </Form.Item>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setMovimientoModalVisible(false);
                form.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<UploadOutlined />}>
                Registrar Movimiento
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default TomaInventario;