import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, InputNumber, Divider } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  BarChartOutlined,
  TrophyOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { Option } = Select;

const KPIMgmt: React.FC = () => {
  const [kpiModalVisible, setKpiModalVisible] = useState(false);
  const [form] = Form.useForm();
  
  // Datos simulados para KPIs
  const kpiData = [
    { id: '1', nombre: 'Ventas Totales', departamento: 'Ventas', responsable: 'Juan Pérez', formula: 'SUM(ventas.total)', unidad: 'MXN', frecuencia: 'diaria', meta: 1500000, umbral: 1000000 },
    { id: '2', nombre: 'Clientes Nuevos', departamento: 'Ventas', responsable: 'María López', formula: 'COUNT(clientes.nuevo)', unidad: 'personas', frecuencia: 'mensual', meta: 150, umbral: 100 },
    { id: '3', nombre: 'Margen de Ganancia', departamento: 'Finanzas', responsable: 'Carlos Gómez', formula: '(ventas.total - costos.total) / ventas.total', unidad: '%', frecuencia: 'diaria', meta: 30, umbral: 20 },
    { id: '4', nombre: 'Tiempo Promedio de Entrega', departamento: 'Logística', responsable: 'Ana Martínez', formula: 'AVG(ordenes.tiempo_entrega)', unidad: 'días', frecuencia: 'diaria', meta: 2.5, umbral: 5 },
  ];

  const columnasKPI = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Departamento', dataIndex: 'departamento', key: 'departamento' },
    { title: 'Responsable', dataIndex: 'responsable', key: 'responsable' },
    { title: 'Unidad', dataIndex: 'unidad', key: 'unidad' },
    { title: 'Frecuencia', dataIndex: 'frecuencia', key: 'frecuencia' },
    { 
      title: 'Meta', 
      dataIndex: 'meta', 
      key: 'meta',
      render: (meta: number, record: any) => `${meta}${record.unidad === '%' ? '%' : ''}`
    },
    { 
      title: 'Umbral', 
      dataIndex: 'umbral', 
      key: 'umbral',
      render: (umbral: number, record: any) => `${umbral}${record.unidad === '%' ? '%' : ''}`
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

  const handleCrearKPI = () => {
    setKpiModalVisible(true);
  };

  const handleGuardarKPI = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      setKpiModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear KPI:', error);
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><TrophyOutlined /> Gestión de KPIs</Title>
          <Text>
            Configuración y monitoreo de indicadores clave de desempeño
          </Text>
        </div>
        <Space>
          <Button icon={<PlusOutlined />} onClick={handleCrearKPI}>
            Nuevo KPI
          </Button>
        </Space>
      </Row>

      <Card className="dashboard-card">
        <Table 
          dataSource={kpiData} 
          columns={columnasKPI} 
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Modal
        title="Crear Nuevo KPI"
        open={kpiModalVisible}
        onCancel={() => {
          setKpiModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={700}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleGuardarKPI}
        >
          <Form.Item name="nombre" label="Nombre del KPI" rules={[{ required: true, message: 'Ingrese el nombre del KPI' }]}>
            <Input placeholder="Ej: Ventas Totales Mensuales" />
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="departamento" label="Departamento" rules={[{ required: true, message: 'Seleccione el departamento' }]}>
                <Select placeholder="Seleccione el departamento">
                  <Option value="ventas">Ventas</Option>
                  <Option value="produccion">Producción</Option>
                  <Option value="finanzas">Finanzas</Option>
                  <Option value="rh">Recursos Humanos</Option>
                  <Option value="logistica">Logística</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="responsable" label="Responsable" rules={[{ required: true, message: 'Seleccione el responsable' }]}>
                <Select placeholder="Seleccione el responsable">
                  <Option value="juan">Juan Pérez</Option>
                  <Option value="maria">María López</Option>
                  <Option value="carlos">Carlos Gómez</Option>
                  <Option value="ana">Ana Martínez</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="formula" label="Fórmula de Cálculo" rules={[{ required: true, message: 'Ingrese la fórmula de cálculo' }]}>
            <Input.TextArea 
              placeholder="Ej: SUM(ventas.total) o AVG(ordenes.tiempo_entrega)" 
              rows={4} 
            />
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="unidad" label="Unidad de Medida" rules={[{ required: true, message: 'Ingrese la unidad de medida' }]}>
                <Select placeholder="Seleccione la unidad">
                  <Option value="MXN">$ MXN</Option>
                  <Option value="USD">$ USD</Option>
                  <Option value="unidades">Unidades</Option>
                  <Option value="porcentaje">%</Option>
                  <Option value="dias">Días</Option>
                  <Option value="horas">Horas</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="frecuencia" label="Frecuencia de Cálculo" rules={[{ required: true, message: 'Seleccione la frecuencia' }]}>
                <Select placeholder="Seleccione la frecuencia">
                  <Option value="diaria">Diaria</Option>
                  <Option value="semanal">Semanal</Option>
                  <Option value="mensual">Mensual</Option>
                  <Option value="trimestral">Trimestral</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="meta" label="Valor Meta" rules={[{ required: true, message: 'Ingrese el valor meta' }]}>
                <InputNumber 
                  placeholder="Ej: 1500000"
                  style={{ width: '100%' }}
                />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="umbral" label="Umbral de Alerta" rules={[{ required: true, message: 'Ingrese el umbral de alerta' }]}>
                <InputNumber 
                  placeholder="Ej: 1000000"
                  style={{ width: '100%' }}
                />
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="descripcion" label="Descripción">
            <Input.TextArea placeholder="Descripción del KPI y su propósito" rows={3} />
          </Form.Item>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setKpiModalVisible(false);
                form.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>
                Crear KPI
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default KPIMgmt;