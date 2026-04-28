import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, Tabs, Divider, Tag, DatePicker, InputNumber, Statistic } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  SafetyCertificateOutlined,
  BarChartOutlined,
  PercentageOutlined,
  FileTextOutlined,
  CheckCircleOutlined
} from '@ant-design/icons';
import { Column, ColumnConfig } from '@ant-design/plots';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;
const { RangePicker } = DatePicker;

const QualityControlDashboard: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [activeTab, setActiveTab] = useState('nonconformities');
  const [form] = Form.useForm();
  
  // Datos simulados para no conformidades
  const nonconformityData = [
    { id: '1', descripcion: 'Defecto en costura', causa: 'Mala técnica de cosido', responsable: 'Operario 1', fecha: '2023-04-15', estado: 'abierto', criticidad: 'alta' },
    { id: '2', descripcion: 'Color diferente al especificado', causa: 'Error en mezcla de tintes', responsable: 'Operario 2', fecha: '2023-04-14', estado: 'cerrado', criticidad: 'media' },
    { id: '3', descripcion: 'Medida incorrecta', causa: 'Error de corte', responsable: 'Operario 3', fecha: '2023-04-13', estado: 'en_proceso', criticidad: 'alta' },
    { id: '4', descripcion: 'Botón flojo', causa: 'Punto débil', responsable: 'Operario 1', fecha: '2023-04-12', estado: 'cerrado', criticidad: 'baja' },
    { id: '5', descripcion: 'Mancha de aceite', causa: 'Mantenimiento deficiente', responsable: 'Mantenimiento', fecha: '2023-04-11', estado: 'abierto', criticidad: 'alta' },
  ];

  // Datos para el análisis de Pareto
  const paretoData = [
    { problema: 'Defecto en costura', frecuencia: 35, porcentaje: 35, acumulado: 35 },
    { problema: 'Medida incorrecta', frecuencia: 25, porcentaje: 25, acumulado: 60 },
    { problema: 'Color diferente', frecuencia: 15, porcentaje: 15, acumulado: 75 },
    { problema: 'Botón flojo', frecuencia: 10, porcentaje: 10, acumulado: 85 },
    { problema: 'Mancha de aceite', frecuencia: 8, porcentaje: 8, acumulado: 93 },
    { problema: 'Falta de etiqueta', frecuencia: 5, porcentaje: 5, acumulado: 98 },
    { problema: 'Otro', frecuencia: 2, porcentaje: 2, acumulado: 100 },
  ];

  // Configuración del gráfico de Pareto
  const paretoConfig: ColumnConfig = {
    data: paretoData,
    xField: 'problema',
    yField: 'frecuencia',
    color: ({ problema }) => {
      // Colores diferentes para cada barra
      const colors = ['#1890FF', '#2FC25B', '#FACC14', '#F04864', '#8543E0', '#7ED321', '#50E3C2'];
      const index = paretoData.findIndex(item => item.problema === problema);
      return colors[index % colors.length];
    },
    columnWidthRatio: 0.8,
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
    annotations: [
      {
        type: 'line',
        start: ['min', 'dataMax'],
        end: ['max', 'dataMax'],
        style: {
          stroke: '#F04864',
          lineWidth: 2,
          lineDash: [2, 2],
        },
      },
    ],
    interactions: [
      {
        type: 'element-highlight-by-color',
      },
      {
        type: 'element-link',
      },
    ],
  };

  const columnasNoConformidades = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Descripción', dataIndex: 'descripcion', key: 'descripcion' },
    { title: 'Causa Raíz', dataIndex: 'causa', key: 'causa' },
    { title: 'Responsable', dataIndex: 'responsable', key: 'responsable' },
    { title: 'Fecha', dataIndex: 'fecha', key: 'fecha' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'abierto') color = 'orange';
        if (estado === 'en_proceso') color = 'blue';
        if (estado === 'cerrado') color = 'green';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { 
      title: 'Criticidad', 
      dataIndex: 'criticidad', 
      key: 'criticidad',
      render: (criticidad: string) => {
        let color = 'default';
        if (criticidad === 'baja') color = 'green';
        if (criticidad === 'media') color = 'blue';
        if (criticidad === 'alta') color = 'red';
        return <Tag color={color}>{criticidad}</Tag>;
      }
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

  const handleCrearNoConformidad = () => {
    setModalVisible(true);
  };

  const handleGuardarNoConformidad = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear no conformidad:', error);
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><SafetyCertificateOutlined /> Control de Calidad</Title>
          <Text>
            Gestión de calidad total: Análisis de Pareto, gráficos de control y seguimiento de no conformidades
          </Text>
        </div>
        <Space>
          <Button icon={<PlusOutlined />} onClick={handleCrearNoConformidad}>
            Nueva No Conformidad
          </Button>
        </Space>
      </Row>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="No Conformidades"
              value={24}
              prefix={<FileTextOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Correctivas"
              value={18}
              prefix={<CheckCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Preventivas"
              value={32}
              prefix={<PercentageOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Eficacia (%)"
              value={87.5}
              precision={2}
              prefix={<BarChartOutlined />}
              suffix="%"
            />
          </Card>
        </Col>
      </Row>

      <Tabs defaultActiveKey="nonconformities" onChange={setActiveTab}>
        <TabPane tab="No Conformidades" key="nonconformities">
          <Card className="dashboard-card">
            <Table 
              dataSource={nonconformityData} 
              columns={columnasNoConformidades} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Análisis de Pareto" key="pareto">
          <Card className="dashboard-card">
            <div style={{ height: 400 }}>
              <Column {...paretoConfig} />
            </div>
            <div style={{ marginTop: 24 }}>
              <Text strong>El análisis de Pareto muestra que el 80% de los defectos provienen del 20% de las causas:</Text>
              <ul>
                <li>Defecto en costura (35% del total)</li>
                <li>Medida incorrecta (25% del total)</li>
                <li>Color diferente (15% del total)</li>
              </ul>
              <Text strong>Acciones recomendadas:</Text>
              <ul>
                <li>Capacitar al personal en técnicas de cosido</li>
                <li>Mejorar el proceso de corte con plantillas precisas</li>
                <li>Implementar control de calidad en la etapa de tintura</li>
              </ul>
            </div>
          </Card>
        </TabPane>
        
        <TabPane tab="Gráficos de Control" key="controlCharts">
          <Card title="Gráfico de Control de Calidad" className="dashboard-card">
            <div style={{ height: 400, display: 'flex', alignItems: 'center', justifyContent: 'center', border: '1px solid #f0f0f0', borderRadius: '4px' }}>
              <Text type="secondary">Visualización de gráficos de control de calidad</Text>
            </div>
            <div style={{ marginTop: 24 }}>
              <Text strong>Límites de control:</Text>
              <ul>
                <li>LCS (Límite de Control Superior): 98%</li>
                <li>LC (Línea Central): 95%</li>
                <li>LCI (Límite de Control Inferior): 92%</li>
              </ul>
              <Text strong>Actualmente:</Text>
              <ul>
                <li>Tasa de defectos: 4.2%</li>
                <li>Nivel de calidad: 95.8%</li>
                <li>Estado: Dentro de límites aceptables</li>
              </ul>
            </div>
          </Card>
        </TabPane>
      </Tabs>

      <Modal
        title="Registrar Nueva No Conformidad"
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
          onFinish={handleGuardarNoConformidad}
        >
          <Form.Item name="descripcion" label="Descripción del Problema" rules={[{ required: true, message: 'Ingrese la descripción del problema' }]}>
            <TextArea placeholder="Describa detalladamente el problema encontrado" rows={4} />
          </Form.Item>
          
          <Form.Item name="causa_raiz" label="Causa Raíz" rules={[{ required: true, message: 'Ingrese la causa raíz del problema' }]}>
            <TextArea placeholder="Describa la causa raíz del problema" rows={3} />
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="responsable" label="Responsable del Área" rules={[{ required: true, message: 'Seleccione el responsable' }]}>
                <Select placeholder="Seleccione el responsable">
                  <Option value="operario1">Operario 1</Option>
                  <Option value="operario2">Operario 2</Option>
                  <Option value="operario3">Operario 3</Option>
                  <Option value="supervisor">Supervisor de Calidad</Option>
                  <Option value="mantenimiento">Personal de Mantenimiento</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="criticidad" label="Criticidad" rules={[{ required: true, message: 'Seleccione la criticidad' }]}>
                <Select placeholder="Seleccione la criticidad">
                  <Option value="baja">Baja</Option>
                  <Option value="media">Media</Option>
                  <Option value="alta">Alta</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="fecha" label="Fecha de Detección" rules={[{ required: true, message: 'Seleccione la fecha de detección' }]}>
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>
          
          <Form.Item name="area" label="Área Afectada" rules={[{ required: true, message: 'Seleccione el área afectada' }]}>
            <Select placeholder="Seleccione el área afectada">
              <Option value="corte">Corte</Option>
              <Option value="confeccion">Confección</Option>
              <Option value="terminado">Terminado</Option>
              <Option value="empaque">Empaque</Option>
              <Option value="almacen">Almacén</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="acciones_inmediatas" label="Acciones Inmediatas">
            <TextArea placeholder="Describa las acciones inmediatas tomadas" rows={3} />
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
                Registrar No Conformidad
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default QualityControlDashboard;