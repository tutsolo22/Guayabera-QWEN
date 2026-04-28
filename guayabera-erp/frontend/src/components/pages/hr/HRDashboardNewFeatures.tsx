import React, { useState } from 'react';
import { Card, Row, Col, Table, Button, Space, Typography, Tag, Modal, Form, Input, Select, DatePicker, InputNumber, Tabs, Divider, message, Steps } from 'antd';
import { 
  CalendarOutlined, 
  FileTextOutlined, 
  MedicineBoxOutlined,
  LaptopOutlined,
  BellOutlined,
  PlusOutlined,
  MailOutlined,
  TeamOutlined,
  UserOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { Option } = Select;
const { Step } = Steps;

interface Anuncio {
  key: string;
  titulo: string;
  contenido: string;
  tipo: string;
  fechaPublicacion: string;
  autor: string;
}

interface Vacacion {
  key: string;
  periodo: string;
  diasSolicitados: number;
  estado: string;
  fechaSolicitud: string;
}

interface Incapacidad {
  key: string;
  tipo: string;
  periodo: string;
  estado: string;
  fechaRegistro: string;
}

interface SolicitudEquipo {
  key: string;
  tipoEquipo: string;
  estadoEquipo: string;
  empleadoAsignado: string;
  departamento: string;
  estado: string;
  fechaSolicitud: string;
}

const HRDashboardNewFeatures: React.FC = () => {
  const [anuncioModalVisible, setAnuncioModalVisible] = useState(false);
  const [vacacionModalVisible, setVacacionModalVisible] = useState(false);
  const [incapacidadModalVisible, setIncapacidadModalVisible] = useState(false);
  const [solicitudEquipoModalVisible, setSolicitudEquipoModalVisible] = useState(false);
  const [currentTab, setCurrentTab] = useState('anuncios');
  const [form] = Form.useForm();
  
  // Datos simulados para anuncios
  const anunciosData: Anuncio[] = [
    { key: '1', titulo: 'Capacitación en Seguridad Laboral', contenido: 'Se llevará a cabo el próximo viernes...', tipo: 'capacitacion', fechaPublicacion: '2023-04-10', autor: 'María López' },
    { key: '2', titulo: 'Nueva Política de Vacaciones', contenido: 'Se ha actualizado la política de...', tipo: 'noticia', fechaPublicacion: '2023-04-08', autor: 'Carlos Ramírez' },
    { key: '3', titulo: 'Evento Corporativo', contenido: 'Invitación al evento anual...', tipo: 'evento', fechaPublicacion: '2023-04-05', autor: 'Ana Gómez' },
  ];

  // Datos simulados para vacaciones
  const vacacionesData: Vacacion[] = [
    { key: '1', periodo: '2023-06-01 a 2023-06-10', diasSolicitados: 10, estado: 'aprobado', fechaSolicitud: '2023-04-01' },
    { key: '2', periodo: '2023-07-15 a 2023-07-25', diasSolicitados: 11, estado: 'pendiente', fechaSolicitud: '2023-04-10' },
    { key: '3', periodo: '2023-08-01 a 2023-08-05', diasSolicitados: 5, estado: 'rechazado', fechaSolicitud: '2023-03-20' },
  ];

  // Datos simulados para incapacidades
  const incapacidadesData: Incapacidad[] = [
    { key: '1', tipo: 'Enfermedad general', periodo: '2023-04-01 a 2023-04-07', estado: 'aprobado', fechaRegistro: '2023-03-30' },
    { key: '2', tipo: 'Accidente trabajo', periodo: '2023-04-10 a 2023-04-20', estado: 'registrado', fechaRegistro: '2023-04-09' },
  ];

  // Datos simulados para solicitudes de equipo
  const solicitudesEquipoData: SolicitudEquipo[] = [
    { key: '1', tipoEquipo: 'Laptop', estadoEquipo: 'nuevo', empleadoAsignado: 'Juan Pérez', departamento: 'TI', estado: 'aprobado', fechaSolicitud: '2023-04-05' },
    { key: '2', tipoEquipo: 'Monitor', estadoEquipo: 'heredado', empleadoAsignado: 'María González', departamento: 'Contabilidad', estado: 'pendiente', fechaSolicitud: '2023-04-10' },
  ];

  const columnasAnuncios = [
    { title: 'Título', dataIndex: 'titulo', key: 'titulo' },
    { title: 'Tipo', dataIndex: 'tipo', key: 'tipo' },
    { title: 'Fecha Publicación', dataIndex: 'fechaPublicacion', key: 'fechaPublicacion' },
    { title: 'Autor', dataIndex: 'autor', key: 'autor' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link">Ver</Button>
        </Space>
      ),
    },
  ];

  const columnasVacaciones = [
    { title: 'Periodo', dataIndex: 'periodo', key: 'periodo' },
    { title: 'Días Solicitados', dataIndex: 'diasSolicitados', key: 'diasSolicitados' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'aprobado') color = 'green';
        if (estado === 'pendiente') color = 'orange';
        if (estado === 'rechazado') color = 'red';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { title: 'Fecha Solicitud', dataIndex: 'fechaSolicitud', key: 'fechaSolicitud' },
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

  const columnasIncapacidades = [
    { title: 'Tipo', dataIndex: 'tipo', key: 'tipo' },
    { title: 'Periodo', dataIndex: 'periodo', key: 'periodo' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'aprobado') color = 'green';
        if (estado === 'registrado') color = 'orange';
        if (estado === 'rechazado') color = 'red';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { title: 'Fecha Registro', dataIndex: 'fechaRegistro', key: 'fechaRegistro' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link">Subir Documento</Button>
        </Space>
      ),
    },
  ];

  const columnasSolicitudesEquipo = [
    { title: 'Tipo Equipo', dataIndex: 'tipoEquipo', key: 'tipoEquipo' },
    { title: 'Estado Equipo', dataIndex: 'estadoEquipo', key: 'estadoEquipo' },
    { title: 'Empleado Asignado', dataIndex: 'empleadoAsignado', key: 'empleadoAsignado' },
    { title: 'Departamento', dataIndex: 'departamento', key: 'departamento' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'aprobado') color = 'green';
        if (estado === 'pendiente') color = 'orange';
        if (estado === 'rechazado') color = 'red';
        if (estado === 'entregado') color = 'blue';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { title: 'Fecha Solicitud', dataIndex: 'fechaSolicitud', key: 'fechaSolicitud' },
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

  const handleCrearAnuncio = () => {
    setAnuncioModalVisible(true);
  };

  const handleSolicitarVacacion = () => {
    setVacacionModalVisible(true);
  };

  const handleRegistrarIncapacidad = () => {
    setIncapacidadModalVisible(true);
  };

  const handleSolicitarEquipo = () => {
    setSolicitudEquipoModalVisible(true);
  };

  const handleGuardarAnuncio = async () => {
    try {
      const values = await form.validateFields();
      message.success('Anuncio creado exitosamente');
      setAnuncioModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear anuncio:', error);
      message.error('Error al crear el anuncio');
    }
  };

  const handleGuardarVacacion = async () => {
    try {
      const values = await form.validateFields();
      message.success('Solicitud de vacaciones enviada exitosamente');
      setVacacionModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al solicitar vacaciones:', error);
      message.error('Error al solicitar vacaciones');
    }
  };

  const handleGuardarIncapacidad = async () => {
    try {
      const values = await form.validateFields();
      message.success('Incapacidad registrada exitosamente');
      setIncapacidadModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al registrar incapacidad:', error);
      message.error('Error al registrar incapacidad');
    }
  };

  const handleGuardarSolicitudEquipo = async () => {
    try {
      const values = await form.validateFields();
      message.success('Solicitud de equipo enviada exitosamente');
      setSolicitudEquipoModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al solicitar equipo:', error);
      message.error('Error al solicitar equipo');
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}>Recursos Humanos - Funcionalidades Adicionales</Title>
          <Text>
            Tablón de anuncios, vacaciones, incapacidades y solicitudes de equipo
          </Text>
        </div>
        <Space>
          {currentTab === 'anuncios' && (
            <Button type="primary" icon={<BellOutlined />} onClick={handleCrearAnuncio}>
              Nuevo Anuncio
            </Button>
          )}
          {currentTab === 'vacaciones' && (
            <Button type="primary" icon={<CalendarOutlined />} onClick={handleSolicitarVacacion}>
              Solicitar Vacaciones
            </Button>
          )}
          {currentTab === 'incapacidades' && (
            <Button type="primary" icon={<MedicineBoxOutlined />} onClick={handleRegistrarIncapacidad}>
              Registrar Incapacidad
            </Button>
          )}
          {currentTab === 'solicitudes-equipo' && (
            <Button type="primary" icon={<LaptopOutlined />} onClick={handleSolicitarEquipo}>
              Solicitar Equipo
            </Button>
          )}
        </Space>
      </Row>

      <Card className="dashboard-card">
        <Tabs 
          defaultActiveKey="anuncios" 
          onChange={setCurrentTab}
          items={[
            {
              label: 'Tablón de Anuncios',
              key: 'anuncios',
              children: (
                <Table 
                  dataSource={anunciosData} 
                  columns={columnasAnuncios} 
                  pagination={{ pageSize: 10 }}
                />
              ),
            },
            {
              label: 'Mis Vacaciones',
              key: 'vacaciones',
              children: (
                <Table 
                  dataSource={vacacionesData} 
                  columns={columnasVacaciones} 
                  pagination={{ pageSize: 10 }}
                />
              ),
            },
            {
              label: 'Incapacidades',
              key: 'incapacidades',
              children: (
                <Table 
                  dataSource={incapacidadesData} 
                  columns={columnasIncapacidades} 
                  pagination={{ pageSize: 10 }}
                />
              ),
            },
            {
              label: 'Solicitudes de Equipo',
              key: 'solicitudes-equipo',
              children: (
                <Table 
                  dataSource={solicitudesEquipoData} 
                  columns={columnasSolicitudesEquipo} 
                  pagination={{ pageSize: 10 }}
                />
              ),
            },
          ]} 
        />
      </Card>

      <Modal
        title="Crear Nuevo Anuncio"
        open={anuncioModalVisible}
        onCancel={() => {
          setAnuncioModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={700}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleGuardarAnuncio}
        >
          <Form.Item name="titulo" label="Título" rules={[{ required: true, message: 'Ingrese el título del anuncio' }]}>
            <Input placeholder="Título del anuncio" />
          </Form.Item>
          
          <Form.Item name="tipo" label="Tipo de Anuncio" rules={[{ required: true, message: 'Seleccione el tipo de anuncio' }]}>
            <Select placeholder="Seleccione el tipo">
              <Option value="noticia">Noticia</Option>
              <Option value="capacitacion">Capacitación</Option>
              <Option value="evento">Evento</Option>
              <Option value="otro">Otro</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="contenido" label="Contenido" rules={[{ required: true, message: 'Ingrese el contenido del anuncio' }]}>
            <Input.TextArea placeholder="Contenido del anuncio" rows={5} />
          </Form.Item>
          
          <Form.Item name="publico" label="Visibilidad" initialValue={true}>
            <Select>
              <Option value={true}>Público</Option>
              <Option value={false}>Solo para ciertos roles</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="fechaExpiracion" label="Fecha de Expiración (Opcional)">
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setAnuncioModalVisible(false);
                form.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>
                Crear Anuncio
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>

      <Modal
        title="Solicitar Vacaciones"
        open={vacacionModalVisible}
        onCancel={() => {
          setVacacionModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleGuardarVacacion}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="fechaInicio" label="Fecha Inicio" rules={[{ required: true, message: 'Seleccione la fecha de inicio' }]}>
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="fechaFin" label="Fecha Fin" rules={[{ required: true, message: 'Seleccione la fecha de fin' }]}>
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="diasSolicitados" label="Días Solicitados" rules={[{ required: true, message: 'Ingrese los días solicitados' }]}>
                <InputNumber min={1} max={30} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="comentarios" label="Comentarios (Opcional)">
            <Input.TextArea placeholder="Comentarios adicionales" rows={3} />
          </Form.Item>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setVacacionModalVisible(false);
                form.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<CalendarOutlined />}>
                Solicitar Vacaciones
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>

      <Modal
        title="Registrar Incapacidad"
        open={incapacidadModalVisible}
        onCancel={() => {
          setIncapacidadModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleGuardarIncapacidad}
        >
          <Form.Item name="tipoIncapacidad" label="Tipo de Incapacidad" rules={[{ required: true, message: 'Seleccione el tipo de incapacidad' }]}>
            <Select placeholder="Seleccione el tipo">
              <Option value="enfermedad_general">Enfermedad General</Option>
              <Option value="accidente_trabajo">Accidente de Trabajo</Option>
              <Option value="riesgo_pregnancy">Riesgo de Embarazo</Option>
              <Option value="maternidad">Maternidad</Option>
              <Option value="paternidad">Paternidad</Option>
            </Select>
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="fechaInicio" label="Fecha Inicio" rules={[{ required: true, message: 'Seleccione la fecha de inicio' }]}>
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="fechaFin" label="Fecha Fin (Opcional)">
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="documentoSoporte" label="Documento de Soporte (Opcional)">
            <Input placeholder="Ruta o enlace al documento digital" />
          </Form.Item>
          
          <Form.Item name="comentarios" label="Comentarios (Opcional)">
            <Input.TextArea placeholder="Comentarios adicionales" rows={3} />
          </Form.Item>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setIncapacidadModalVisible(false);
                form.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<MedicineBoxOutlined />}>
                Registrar Incapacidad
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>

      <Modal
        title="Solicitar Equipo de Cómputo"
        open={solicitudEquipoModalVisible}
        onCancel={() => {
          setSolicitudEquipoModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={700}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleGuardarSolicitudEquipo}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="tipoEquipo" label="Tipo de Equipo" rules={[{ required: true, message: 'Ingrese el tipo de equipo' }]}>
                <Input placeholder="Ej: Laptop, Monitor, Teclado" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="estadoEquipo" label="Estado del Equipo" rules={[{ required: true, message: 'Seleccione el estado del equipo' }]}>
                <Select>
                  <Option value="nuevo">Nuevo</Option>
                  <Option value="heredado">Heredado</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="descripcionEquipo" label="Descripción del Equipo (Opcional)">
            <Input.TextArea placeholder="Características del equipo solicitado" rows={2} />
          </Form.Item>
          
          <Form.Item name="necesitaCorreo" label="¿Necesita Cuenta de Correo?" valuePropName="checked">
            <Select>
              <Option value={true}>Sí</Option>
              <Option value={false}>No</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="tipoCorreo" label="Tipo de Correo">
            <Select>
              <Option value="nuevo">Nuevo</Option>
              <Option value="heredado">Heredado</Option>
            </Select>
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="departamentoDestino" label="Departamento Destino" rules={[{ required: true, message: 'Seleccione el departamento' }]}>
                <Select placeholder="Seleccione el departamento">
                  <Option value="ti">TI</Option>
                  <Option value="contabilidad">Contabilidad</Option>
                  <Option value="ventas">Ventas</Option>
                  <Option value="rh">Recursos Humanos</Option>
                  <Option value="produccion">Producción</Option>
                  <Option value="logistica">Logística</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="jefeDepartamento" label="Jefe de Departamento" rules={[{ required: true, message: 'Seleccione el jefe de departamento' }]}>
                <Select placeholder="Seleccione el jefe">
                  <Option value="maria">María López</Option>
                  <Option value="carlos">Carlos Ramírez</Option>
                  <Option value="ana">Ana Gómez</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="empleadoAsignadoNombre" label="Nombre del Empleado Asignado" rules={[{ required: true, message: 'Ingrese el nombre del empleado asignado' }]}>
            <Input placeholder="Nombre completo del empleado" />
          </Form.Item>
          
          <Form.Item name="carpetasCompartidas" label="¿Necesita Carpetas Compartidas?" valuePropName="checked">
            <Select>
              <Option value={true}>Sí</Option>
              <Option value={false}>No</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="descripcionCarpetas" label="Descripción de Carpetas (Opcional)">
            <Input.TextArea placeholder="Listado de carpetas compartidas necesarias" rows={2} />
          </Form.Item>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setSolicitudEquipoModalVisible(false);
                form.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<LaptopOutlined />}>
                Solicitar Equipo
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default HRDashboardNewFeatures;