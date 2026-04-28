import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, Tabs, Divider, Tag, Slider, Statistic, Progress } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  BarChartOutlined,
  PercentageOutlined,
  RiseOutlined,
  FallOutlined,
  FundOutlined
} from '@ant-design/icons';
import { Column, ColumnConfig } from '@ant-design/plots';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

const SensitivityAnalysis: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [activeTab, setActiveTab] = useState('scenarios');
  const [form] = Form.useForm();
  
  // Datos simulados para escenarios
  const scenarioData = [
    { id: '1', nombre: 'Escenario Optimista', descripcion: 'Aumento del 15% en ventas', resultado: 2500000, variacion: '+15%', estado: 'activo' },
    { id: '2', nombre: 'Escenario Base', descripcion: 'Proyección normal', resultado: 2100000, variacion: '0%', estado: 'activo' },
    { id: '3', nombre: 'Escenario Pesimista', descripcion: 'Disminución del 10% en ventas', resultado: 1850000, variacion: '-10%', estado: 'activo' },
    { id: '4', nombre: 'Escenario Inflación', descripcion: 'Aumento de costos por inflación', resultado: 1950000, variacion: '-7%', estado: 'activo' },
  ];

  // Datos simulados para variables
  const variableData = [
    { id: '1', nombre: 'Precio de Venta', descripcion: 'Impacto en ventas por cambio en precio', rango_min: -15, rango_max: 15, impacto: 'alto', estado: 'activo' },
    { id: '2', nombre: 'Costo de Producción', descripcion: 'Impacto en utilidades por cambio en costos', rango_min: -10, rango_max: 20, impacto: 'muy_alto', estado: 'activo' },
    { id: '3', nombre: 'Tasa de Interés', descripcion: 'Impacto en flujo de efectivo', rango_min: -2, rango_max: 3, impacto: 'medio', estado: 'activo' },
    { id: '4', nombre: 'Tipo de Cambio', descripcion: 'Impacto en costos de importación', rango_min: -5, rango_max: 8, impacto: 'medio', estado: 'inactivo' },
  ];

  // Datos para gráfico de sensibilidad
  const sensitivityData = [
    { variable: 'Precio Venta', impacto: 15.2, color: '#1890FF' },
    { variable: 'Costo Prod', impacto: -12.8, color: '#F04864' },
    { variable: 'Vol. Ventas', impacto: 10.5, color: '#2FC25B' },
    { variable: 'Tasa Int', impacto: -3.2, color: '#FACC14' },
    { variable: 'Inflación', impacto: -5.7, color: '#8543E0' },
  ];

  const columnasEscenarios = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Descripción', dataIndex: 'descripcion', key: 'descripcion' },
    { 
      title: 'Resultado', 
      dataIndex: 'resultado', 
      key: 'resultado',
      render: (resultado: number) => `$${resultado.toLocaleString()}`
    },
    { 
      title: 'Variación', 
      dataIndex: 'variacion', 
      key: 'variacion',
      render: (variacion: string) => {
        const isPositive = variacion.startsWith('+');
        return (
          <Text type={isPositive ? 'success' : 'danger'}>
            {isPositive ? <RiseOutlined /> : <FallOutlined />} {variacion}
          </Text>
        );
      }
    },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => (
        <Tag color={estado === 'activo' ? 'green' : 'default'}>
          {estado}
        </Tag>
      )
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link" icon={<EditOutlined />}>Editar</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Eliminar</Button>
        </Space>
      ),
    },
  ];

  const columnasVariables = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Descripción', dataIndex: 'descripcion', key: 'descripcion' },
    { 
      title: 'Rango Min (%)', 
      dataIndex: 'rango_min', 
      key: 'rango_min',
      render: (rango_min: number) => `${rango_min}%`
    },
    { 
      title: 'Rango Max (%)', 
      dataIndex: 'rango_max', 
      key: 'rango_max',
      render: (rango_max: number) => `${rango_max}%`
    },
    { 
      title: 'Impacto', 
      dataIndex: 'impacto', 
      key: 'impacto',
      render: (impacto: string) => {
        let color = 'default';
        if (impacto === 'muy_alto') color = 'red';
        if (impacto === 'alto') color = 'orange';
        if (impacto === 'medio') color = 'blue';
        if (impacto === 'bajo') color = 'green';
        return <Tag color={color}>{impacto}</Tag>;
      }
    },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => (
        <Tag color={estado === 'activo' ? 'green' : 'default'}>
          {estado}
        </Tag>
      )
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link" icon={<EditOutlined />}>Editar</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Eliminar</Button>
        </Space>
      ),
    },
  ];

  // Configuración del gráfico de sensibilidad
  const sensitivityConfig: ColumnConfig = {
    data: sensitivityData,
    xField: 'variable',
    yField: 'impacto',
    color: ({ variable }) => {
      const item = sensitivityData.find(d => d.variable === variable);
      return item?.color || '#1890FF';
    },
    columnWidthRatio: 0.6,
    label: {
      position: 'top',
      style: {
        fill: '#FFFFFF',
        opacity: 0.6,
      },
    },
    yAxis: {
      nice: true,
    },
    interactions: [
      {
        type: 'element-highlight-by-color',
      },
      {
        type: 'element-link',
      },
    ],
  };

  const handleCrearEscenario = () => {
    setModalVisible(true);
  };

  const handleGuardarEscenario = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear escenario:', error);
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><BarChartOutlined /> Análisis de Sensibilidad</Title>
          <Text>
            Evaluación del impacto de cambios en variables clave sobre los resultados financieros
          </Text>
        </div>
        <Space>
          <Button icon={<PlusOutlined />} onClick={handleCrearEscenario}>
            Nuevo Escenario
          </Button>
        </Space>
      </Row>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Escenarios Activos"
              value={4}
              prefix={<FundOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Variables Críticas"
              value={3}
              prefix={<BarChartOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Mayor Impacto"
              value="-12.8"
              precision={1}
              prefix={<FallOutlined />}
              suffix="%"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Mejor Escenario"
              value={2500000}
              precision={0}
              prefix={<RiseOutlined />}
              formatter={(value) => `$${value}`}
            />
          </Card>
        </Col>
      </Row>

      <Tabs defaultActiveKey="sensitivity" onChange={setActiveTab}>
        <TabPane tab="Análisis de Sensibilidad" key="sensitivity">
          <Card className="dashboard-card">
            <div style={{ height: 400 }}>
              <Column {...sensitivityConfig} />
            </div>
            <div style={{ marginTop: 24 }}>
              <Text strong>Interpretación:</Text>
              <ul>
                <li>El costo de producción tiene el mayor impacto negativo (-12.8%)</li>
                <li>El precio de venta tiene el mayor impacto positivo (15.2%)</li>
                <li>Se recomienda enfocarse en la optimización de costos y estrategias de precios</li>
              </ul>
            </div>
          </Card>
        </TabPane>
        
        <TabPane tab="Escenarios" key="scenarios">
          <Card className="dashboard-card">
            <Table 
              dataSource={scenarioData} 
              columns={columnasEscenarios} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Variables Clave" key="variables">
          <Card className="dashboard-card">
            <Table 
              dataSource={variableData} 
              columns={columnasVariables} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
      </Tabs>

      <Modal
        title="Crear Nuevo Escenario"
        open={modalVisible}
        onCancel={() => {
          setModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={700}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleGuardarEscenario}
        >
          <Form.Item name="nombre" label="Nombre del Escenario" rules={[{ required: true, message: 'Ingrese el nombre del escenario' }]}>
            <Input placeholder="Ej: Escenario Optimista" />
          </Form.Item>
          
          <Form.Item name="descripcion" label="Descripción">
            <TextArea placeholder="Descripción del escenario y supuestos considerados" rows={4} />
          </Form.Item>
          
          <Form.Item name="variables_impactadas" label="Variables Impactadas">
            <Select 
              mode="multiple" 
              placeholder="Seleccione las variables impactadas"
              allowClear
            >
              <Option value="precio_venta">Precio de Venta</Option>
              <Option value="costo_prod">Costo de Producción</Option>
              <Option value="vol_ventas">Volumen de Ventas</Option>
              <Option value="tasa_int">Tasa de Interés</Option>
              <Option value="inflacion">Tasa de Inflación</Option>
            </Select>
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="variacion_resultado" label="Variación Esperada en Resultado (%)">
                <Slider 
                  min={-50} 
                  max={50} 
                  tooltip={{ formatter: (value) => `${value}%` }}
                  marks={{ -50: '-50%', -25: '-25%', 0: '0%', 25: '25%', 50: '50%' }}
                />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="variacion_valor" label="Valor de Variación (%)" initialValue={0}>
                <InputNumber 
                  min={-50} 
                  max={50} 
                  formatter={value => `${value}%`}
                  parser={value => value!.replace('%', '')}
                  style={{ width: '100%' }}
                />
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="resultado_estimado" label="Resultado Estimado">
            <InputNumber 
              placeholder="Resultado financiero estimado"
              style={{ width: '100%' }}
              formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
              parser={value => value!.replace(/\$\s?|(,*)/g, '')}
            />
          </Form.Item>
          
          <Form.Item name="estado" label="Estado" valuePropName="checked">
            <Select placeholder="Seleccione el estado">
              <Option value="activo">Activo</Option>
              <Option value="inactivo">Inactivo</Option>
            </Select>
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
                Crear Escenario
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default SensitivityAnalysis;