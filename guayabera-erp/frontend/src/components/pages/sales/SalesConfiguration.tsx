import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Form, 
  Input, 
  Button, 
  Switch, 
  Slider, 
  Tabs, 
  Row, 
  Col, 
  Table, 
  Modal, 
  notification,
  Typography,
  Space,
  Popconfirm,
  Select,
  DatePicker
} from 'antd';
import { 
  DollarCircleOutlined, 
  PercentageOutlined, 
  GiftOutlined, 
  TagsOutlined,
  PlusOutlined,
  EditOutlined,
  DeleteOutlined
} from '@ant-design/icons';
import moment from 'moment';

const { Title, Text } = Typography;
const { TabPane } = Tabs;
const { RangePicker } = DatePicker;

interface SalesConfiguration {
  id?: number;
  company_id: number;
  price_update_approval_required: boolean;
  allow_manual_discounts: boolean;
  max_discount_percentage: number;
  enable_promotions: boolean;
  promotion_approval_required: boolean;
  enable_customer_loyalty: boolean;
  loyalty_points_per_currency: number;
  points_to_currency_ratio: number;
  require_sales_order_approval: boolean;
  allow_backorders: boolean;
  default_sales_terms?: string;
  default_tax_rate: number;
}

interface DiscountRule {
  id?: number;
  name: string;
  description?: string;
  company_id: number;
  discount_type: string;
  discount_value: number;
  min_quantity: number;
  min_amount: number;
  applies_to_all_products: boolean;
  start_date?: string;
  end_date?: string;
  is_active: boolean;
  priority: number;
}

interface LoyaltyProgram {
  id?: number;
  name: string;
  description?: string;
  company_id: number;
  earning_method: string;
  points_calculation: string;
  earning_rate: number;
  redemption_rate: number;
  minimum_points_for_redemption: number;
  points_expire: boolean;
  points_expiry_months: number;
  is_active: boolean;
  is_default: boolean;
}

interface PriceList {
  id?: number;
  name: string;
  description?: string;
  company_id: number;
  currency: string;
  is_active: boolean;
  is_default: boolean;
  valid_from?: string;
  valid_until?: string;
}

const SalesConfiguration: React.FC = () => {
  const [configForm] = Form.useForm();
  const [discountRuleForm] = Form.useForm();
  const [loyaltyProgramForm] = Form.useForm();
  const [priceListForm] = Form.useForm();
  
  const [salesConfig, setSalesConfig] = useState<SalesConfiguration>({
    company_id: 1,
    price_update_approval_required: false,
    allow_manual_discounts: true,
    max_discount_percentage: 10,
    enable_promotions: true,
    promotion_approval_required: true,
    enable_customer_loyalty: true,
    loyalty_points_per_currency: 1,
    points_to_currency_ratio: 0.01,
    require_sales_order_approval: true,
    allow_backorders: true,
    default_sales_terms: '',
    default_tax_rate: 16,
  });
  
  const [discountRules, setDiscountRules] = useState<DiscountRule[]>([
    {
      id: 1,
      name: 'Descuento por volumen',
      description: 'Descuento para compras mayores a 1000 unidades',
      company_id: 1,
      discount_type: 'percentage',
      discount_value: 5,
      min_quantity: 100,
      min_amount: 1000,
      applies_to_all_products: true,
      is_active: true,
      priority: 1,
    }
  ]);
  
  const [loyaltyPrograms, setLoyaltyPrograms] = useState<LoyaltyProgram[]>([
    {
      id: 1,
      name: 'Programa de Lealtad Básico',
      description: 'Programa de puntos básico para clientes',
      company_id: 1,
      earning_method: 'spending',
      points_calculation: 'percentage',
      earning_rate: 1,
      redemption_rate: 0.01,
      minimum_points_for_redemption: 100,
      points_expire: true,
      points_expiry_months: 12,
      is_active: true,
      is_default: true,
    }
  ]);
  
  const [priceLists, setPriceLists] = useState<PriceList[]>([
    {
      id: 1,
      name: 'Lista de Precios General',
      description: 'Lista de precios estándar para todos los clientes',
      company_id: 1,
      currency: 'MXN',
      is_active: true,
      is_default: true,
      valid_from: moment().toISOString(),
    }
  ]);
  
  const [editingRule, setEditingRule] = useState<DiscountRule | null>(null);
  const [editingProgram, setEditingProgram] = useState<LoyaltyProgram | null>(null);
  const [editingPriceList, setEditingPriceList] = useState<PriceList | null>(null);
  const [ruleModalVisible, setRuleModalVisible] = useState(false);
  const [programModalVisible, setProgramModalVisible] = useState(false);
  const [priceListModalVisible, setPriceListModalVisible] = useState(false);

  // Simular carga de datos
  useEffect(() => {
    // Aquí iría la llamada a la API para cargar la configuración
  }, []);

  const handleSaveConfig = async (values: SalesConfiguration) => {
    try {
      // Simular llamada a la API
      setSalesConfig(values);
      notification.success({
        message: 'Configuración guardada',
        description: 'La configuración de ventas se ha actualizado correctamente.',
      });
    } catch (error) {
      notification.error({
        message: 'Error',
        description: 'Hubo un problema al guardar la configuración.',
      });
    }
  };

  const handleAddDiscountRule = () => {
    setEditingRule(null);
    discountRuleForm.resetFields();
    setRuleModalVisible(true);
  };

  const handleEditDiscountRule = (rule: DiscountRule) => {
    setEditingRule(rule);
    discountRuleForm.setFieldsValue({
      ...rule,
      validity_period: rule.start_date && rule.end_date ? 
        [moment(rule.start_date), moment(rule.end_date)] : undefined
    });
    setRuleModalVisible(true);
  };

  const handleSaveDiscountRule = async (values: any) => {
    try {
      // Convertir el rango de fechas
      if (values.validity_period) {
        values.start_date = values.validity_period[0]?.toISOString();
        values.end_date = values.validity_period[1]?.toISOString();
        delete values.validity_period;
      }

      if (editingRule) {
        // Actualizar regla existente
        const updatedRules = discountRules.map(rule => 
          rule.id === editingRule.id ? { ...editingRule, ...values } : rule
        );
        setDiscountRules(updatedRules);
      } else {
        // Agregar nueva regla
        const newRule = {
          ...values,
          id: discountRules.length + 1,
        };
        setDiscountRules([...discountRules, newRule]);
      }

      notification.success({
        message: 'Regla de descuento guardada',
        description: 'La regla de descuento se ha guardado correctamente.',
      });

      setRuleModalVisible(false);
    } catch (error) {
      notification.error({
        message: 'Error',
        description: 'Hubo un problema al guardar la regla de descuento.',
      });
    }
  };

  const handleDeleteDiscountRule = (id: number) => {
    setDiscountRules(discountRules.filter(rule => rule.id !== id));
    notification.success({
      message: 'Regla eliminada',
      description: 'La regla de descuento se ha eliminado correctamente.',
    });
  };

  const handleAddLoyaltyProgram = () => {
    setEditingProgram(null);
    loyaltyProgramForm.resetFields();
    setProgramModalVisible(true);
  };

  const handleEditLoyaltyProgram = (program: LoyaltyProgram) => {
    setEditingProgram(program);
    loyaltyProgramForm.setFieldsValue(program);
    setProgramModalVisible(true);
  };

  const handleSaveLoyaltyProgram = async (values: LoyaltyProgram) => {
    try {
      if (editingProgram) {
        // Actualizar programa existente
        const updatedPrograms = loyaltyPrograms.map(program => 
          program.id === editingProgram.id ? { ...editingProgram, ...values } : program
        );
        setLoyaltyPrograms(updatedPrograms);
      } else {
        // Agregar nuevo programa
        const newProgram = {
          ...values,
          id: loyaltyPrograms.length + 1,
        };
        setLoyaltyPrograms([...loyaltyPrograms, newProgram]);
      }

      notification.success({
        message: 'Programa de lealtad guardado',
        description: 'El programa de lealtad se ha guardado correctamente.',
      });

      setProgramModalVisible(false);
    } catch (error) {
      notification.error({
        message: 'Error',
        description: 'Hubo un problema al guardar el programa de lealtad.',
      });
    }
  };

  const handleDeleteLoyaltyProgram = (id: number) => {
    setLoyaltyPrograms(loyaltyPrograms.filter(program => program.id !== id));
    notification.success({
      message: 'Programa eliminado',
      description: 'El programa de lealtad se ha eliminado correctamente.',
    });
  };

  const handleAddPriceList = () => {
    setEditingPriceList(null);
    priceListForm.resetFields();
    setPriceListModalVisible(true);
  };

  const handleEditPriceList = (priceList: PriceList) => {
    setEditingPriceList(priceList);
    priceListForm.setFieldsValue({
      ...priceList,
      validity_period: priceList.valid_from && priceList.valid_until ? 
        [moment(priceList.valid_from), moment(priceList.valid_until)] : undefined
    });
    setPriceListModalVisible(true);
  };

  const handleSavePriceList = async (values: any) => {
    try {
      // Convertir el rango de fechas
      if (values.validity_period) {
        values.valid_from = values.validity_period[0]?.toISOString();
        values.valid_until = values.validity_period[1]?.toISOString();
        delete values.validity_period;
      }

      if (editingPriceList) {
        // Actualizar lista existente
        const updatedLists = priceLists.map(list => 
          list.id === editingPriceList.id ? { ...editingPriceList, ...values } : list
        );
        setPriceLists(updatedLists);
      } else {
        // Agregar nueva lista
        const newList = {
          ...values,
          id: priceLists.length + 1,
        };
        setPriceLists([...priceLists, newList]);
      }

      notification.success({
        message: 'Lista de precios guardada',
        description: 'La lista de precios se ha guardado correctamente.',
      });

      setPriceListModalVisible(false);
    } catch (error) {
      notification.error({
        message: 'Error',
        description: 'Hubo un problema al guardar la lista de precios.',
      });
    }
  };

  const handleDeletePriceList = (id: number) => {
    setPriceLists(priceLists.filter(list => list.id !== id));
    notification.success({
      message: 'Lista eliminada',
      description: 'La lista de precios se ha eliminada correctamente.',
    });
  };

  // Columnas para la tabla de reglas de descuento
  const discountRuleColumns = [
    {
      title: 'Nombre',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Tipo',
      dataIndex: 'discount_type',
      key: 'discount_type',
      render: (text: string) => text === 'percentage' ? 'Porcentaje' : 'Monto fijo',
    },
    {
      title: 'Valor',
      dataIndex: 'discount_value',
      key: 'discount_value',
      render: (value: number, record: DiscountRule) => 
        record.discount_type === 'percentage' ? `${value}%` : `$${value}`,
    },
    {
      title: 'Cantidad Mínima',
      dataIndex: 'min_quantity',
      key: 'min_quantity',
    },
    {
      title: 'Monto Mínimo',
      dataIndex: 'min_amount',
      key: 'min_amount',
      render: (value: number) => `$${value}`,
    },
    {
      title: 'Activa',
      dataIndex: 'is_active',
      key: 'is_active',
      render: (active: boolean) => active ? 'Sí' : 'No',
    },
    {
      title: 'Acciones',
      key: 'actions',
      render: (_: any, record: DiscountRule) => (
        <Space>
          <Button 
            icon={<EditOutlined />} 
            size="small" 
            onClick={() => handleEditDiscountRule(record)}
          />
          <Popconfirm 
            title="¿Eliminar regla de descuento?" 
            onConfirm={() => handleDeleteDiscountRule(record.id!)}
          >
            <Button icon={<DeleteOutlined />} size="small" danger />
          </Popconfirm>
        </Space>
      ),
    },
  ];

  // Columnas para la tabla de programas de lealtad
  const loyaltyProgramColumns = [
    {
      title: 'Nombre',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Método de acumulación',
      dataIndex: 'earning_method',
      key: 'earning_method',
      render: (method: string) => {
        switch(method) {
          case 'spending': return 'Por compra';
          case 'visits': return 'Por visitas';
          case 'purchases': return 'Por compras';
          default: return method;
        }
      },
    },
    {
      title: 'Tasa de acumulación',
      dataIndex: 'earning_rate',
      key: 'earning_rate',
      render: (rate: number) => `${rate} pts/unidad`,
    },
    {
      title: 'Tasa de canje',
      dataIndex: 'redemption_rate',
      key: 'redemption_rate',
      render: (rate: number) => `$${rate}/pto`,
    },
    {
      title: 'Predeterminado',
      dataIndex: 'is_default',
      key: 'is_default',
      render: (isDefault: boolean) => isDefault ? 'Sí' : 'No',
    },
    {
      title: 'Activo',
      dataIndex: 'is_active',
      key: 'is_active',
      render: (active: boolean) => active ? 'Sí' : 'No',
    },
    {
      title: 'Acciones',
      key: 'actions',
      render: (_: any, record: LoyaltyProgram) => (
        <Space>
          <Button 
            icon={<EditOutlined />} 
            size="small" 
            onClick={() => handleEditLoyaltyProgram(record)}
          />
          <Popconfirm 
            title="¿Eliminar programa de lealtad?" 
            onConfirm={() => handleDeleteLoyaltyProgram(record.id!)}
          >
            <Button icon={<DeleteOutlined />} size="small" danger />
          </Popconfirm>
        </Space>
      ),
    },
  ];

  // Columnas para la tabla de listas de precios
  const priceListColumns = [
    {
      title: 'Nombre',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Moneda',
      dataIndex: 'currency',
      key: 'currency',
    },
    {
      title: 'Válida desde',
      dataIndex: 'valid_from',
      key: 'valid_from',
      render: (date: string) => date ? moment(date).format('DD/MM/YYYY') : 'No especificado',
    },
    {
      title: 'Válida hasta',
      dataIndex: 'valid_until',
      key: 'valid_until',
      render: (date: string) => date ? moment(date).format('DD/MM/YYYY') : 'No especificado',
    },
    {
      title: 'Predeterminada',
      dataIndex: 'is_default',
      key: 'is_default',
      render: (isDefault: boolean) => isDefault ? 'Sí' : 'No',
    },
    {
      title: 'Activa',
      dataIndex: 'is_active',
      key: 'is_active',
      render: (active: boolean) => active ? 'Sí' : 'No',
    },
    {
      title: 'Acciones',
      key: 'actions',
      render: (_: any, record: PriceList) => (
        <Space>
          <Button 
            icon={<EditOutlined />} 
            size="small" 
            onClick={() => handleEditPriceList(record)}
          />
          <Popconfirm 
            title="¿Eliminar lista de precios?" 
            onConfirm={() => handleDeletePriceList(record.id!)}
          >
            <Button icon={<DeleteOutlined />} size="small" danger />
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <Title level={2}>
          <DollarCircleOutlined /> Configuración de Ventas
        </Title>
        <Text type="secondary">
          Gestiona las configuraciones de precios, descuentos, promociones y lealtad
        </Text>
      </Row>

      <Tabs defaultActiveKey="general" destroyInactiveTabPane>
        {/* Pestaña de configuración general */}
        <TabPane tab="Configuración General" key="general">
          <Card title="Configuración General de Ventas">
            <Form
              form={configForm}
              layout="vertical"
              initialValues={salesConfig}
              onFinish={handleSaveConfig}
            >
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item 
                    name="price_update_approval_required" 
                    label="Requiere aprobación para actualización de precios" 
                    valuePropName="checked"
                  >
                    <Switch />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item 
                    name="allow_manual_discounts" 
                    label="Permitir descuentos manuales" 
                    valuePropName="checked"
                  >
                    <Switch />
                  </Form.Item>
                </Col>
              </Row>

              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item 
                    name="max_discount_percentage" 
                    label="Porcentaje máximo de descuento (%)"
                    rules={[{ required: true, message: 'Por favor ingrese el porcentaje máximo' }]}
                  >
                    <Slider min={0} max={100} step={0.1} tooltip={{ formatter: (value) => `${value}%` }} />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item 
                    name="default_tax_rate" 
                    label="Tasa de impuesto predeterminada (%)"
                    rules={[{ required: true, message: 'Por favor ingrese la tasa de impuesto' }]}
                  >
                    <Slider min={0} max={100} step={0.1} tooltip={{ formatter: (value) => `${value}%` }} />
                  </Form.Item>
                </Col>
              </Row>

              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item 
                    name="enable_promotions" 
                    label="Habilitar promociones" 
                    valuePropName="checked"
                  >
                    <Switch />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item 
                    name="promotion_approval_required" 
                    label="Requiere aprobación para promociones" 
                    valuePropName="checked"
                  >
                    <Switch />
                  </Form.Item>
                </Col>
              </Row>

              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item 
                    name="enable_customer_loyalty" 
                    label="Habilitar programa de lealtad" 
                    valuePropName="checked"
                  >
                    <Switch />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item 
                    name="require_sales_order_approval" 
                    label="Requiere aprobación de órdenes de venta" 
                    valuePropName="checked"
                  >
                    <Switch />
                  </Form.Item>
                </Col>
              </Row>

              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item 
                    name="allow_backorders" 
                    label="Permitir pedidos pendientes" 
                    valuePropName="checked"
                  >
                    <Switch />
                  </Form.Item>
                </Col>
              </Row>

              <Form.Item name="default_sales_terms" label="Términos de venta predeterminados">
                <Input.TextArea rows={4} placeholder="Términos y condiciones predeterminados para las ventas" />
              </Form.Item>

              <Form.Item>
                <Button type="primary" htmlType="submit" icon={<TagsOutlined />}>
                  Guardar Configuración General
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </TabPane>

        {/* Pestaña de reglas de descuento */}
        <TabPane tab="Reglas de Descuento" key="discounts">
          <Card 
            title="Reglas de Descuento"
            extra={
              <Button 
                type="primary" 
                icon={<PlusOutlined />} 
                onClick={handleAddDiscountRule}
              >
                Agregar Regla
              </Button>
            }
          >
            <Table 
              dataSource={discountRules} 
              columns={discountRuleColumns} 
              rowKey="id"
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>

        {/* Pestaña de programas de lealtad */}
        <TabPane tab="Programas de Lealtad" key="loyalty">
          <Card 
            title="Programas de Lealtad"
            extra={
              <Button 
                type="primary" 
                icon={<GiftOutlined />} 
                onClick={handleAddLoyaltyProgram}
              >
                Agregar Programa
              </Button>
            }
          >
            <Table 
              dataSource={loyaltyPrograms} 
              columns={loyaltyProgramColumns} 
              rowKey="id"
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>

        {/* Pestaña de listas de precios */}
        <TabPane tab="Listas de Precios" key="prices">
          <Card 
            title="Listas de Precios"
            extra={
              <Button 
                type="primary" 
                icon={<PercentageOutlined />} 
                onClick={handleAddPriceList}
              >
                Agregar Lista
              </Button>
            }
          >
            <Table 
              dataSource={priceLists} 
              columns={priceListColumns} 
              rowKey="id"
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
      </Tabs>

      {/* Modal para edición/creación de regla de descuento */}
      <Modal
        title={editingRule ? "Editar Regla de Descuento" : "Crear Nueva Regla de Descuento"}
        open={ruleModalVisible}
        onCancel={() => setRuleModalVisible(false)}
        footer={null}
        width={600}
      >
        <Form
          form={discountRuleForm}
          layout="vertical"
          onFinish={handleSaveDiscountRule}
        >
          <Form.Item 
            name="name" 
            label="Nombre de la regla"
            rules={[{ required: true, message: 'Por favor ingrese el nombre' }]}
          >
            <Input placeholder="Ej: Descuento por volumen" />
          </Form.Item>

          <Form.Item name="description" label="Descripción">
            <Input.TextArea rows={3} placeholder="Descripción de la regla de descuento" />
          </Form.Item>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item 
                name="discount_type" 
                label="Tipo de descuento"
                initialValue="percentage"
              >
                <Select>
                  <Select.Option value="percentage">Porcentaje</Select.Option>
                  <Select.Option value="fixed_amount">Monto fijo</Select.Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item 
                name="discount_value" 
                label="Valor del descuento"
                rules={[{ required: true, message: 'Por favor ingrese el valor' }]}
              >
                <Input type="number" placeholder="Ej: 10" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item 
                name="min_quantity" 
                label="Cantidad mínima"
                initialValue={1}
              >
                <Input type="number" placeholder="Ej: 100" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item 
                name="min_amount" 
                label="Monto mínimo"
                initialValue={0}
              >
                <Input type="number" placeholder="Ej: 1000" />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item 
            name="applies_to_all_products" 
            label="Aplica a todos los productos" 
            valuePropName="checked"
            initialValue={false}
          >
            <Switch />
          </Form.Item>

          <Form.Item 
            name="validity_period" 
            label="Periodo de validez"
          >
            <RangePicker style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item 
            name="is_active" 
            label="Activa" 
            valuePropName="checked"
            initialValue={true}
          >
            <Switch />
          </Form.Item>

          <Form.Item 
            name="priority" 
            label="Prioridad (mayor número = mayor prioridad)"
            initialValue={1}
          >
            <Input type="number" placeholder="Ej: 1" />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" block>
              {editingRule ? "Actualizar Regla" : "Crear Regla"}
            </Button>
          </Form.Item>
        </Form>
      </Modal>

      {/* Modal para edición/creación de programa de lealtad */}
      <Modal
        title={editingProgram ? "Editar Programa de Lealtad" : "Crear Nuevo Programa de Lealtad"}
        open={programModalVisible}
        onCancel={() => setProgramModalVisible(false)}
        footer={null}
        width={600}
      >
        <Form
          form={loyaltyProgramForm}
          layout="vertical"
          onFinish={handleSaveLoyaltyProgram}
        >
          <Form.Item 
            name="name" 
            label="Nombre del programa"
            rules={[{ required: true, message: 'Por favor ingrese el nombre' }]}
          >
            <Input placeholder="Ej: Club de Beneficios" />
          </Form.Item>

          <Form.Item name="description" label="Descripción">
            <Input.TextArea rows={3} placeholder="Descripción del programa de lealtad" />
          </Form.Item>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item 
                name="earning_method" 
                label="Método de acumulación"
                initialValue="spending"
              >
                <Select>
                  <Select.Option value="spending">Por compra</Select.Option>
                  <Select.Option value="visits">Por visitas</Select.Option>
                  <Select.Option value="purchases">Por compras</Select.Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item 
                name="points_calculation" 
                label="Cálculo de puntos"
                initialValue="percentage"
              >
                <Select>
                  <Select.Option value="percentage">Porcentaje</Select.Option>
                  <Select.Option value="fixed_amount">Monto fijo</Select.Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item 
                name="earning_rate" 
                label="Tasa de acumulación (puntos por unidad)"
                rules={[{ required: true, message: 'Por favor ingrese la tasa' }]}
              >
                <Input type="number" placeholder="Ej: 1" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item 
                name="redemption_rate" 
                label="Tasa de canje (valor de cada punto)"
                rules={[{ required: true, message: 'Por favor ingrese la tasa' }]}
              >
                <Input type="number" placeholder="Ej: 0.01" />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item 
            name="minimum_points_for_redemption" 
            label="Mínimo de puntos para canje"
            initialValue={100}
          >
            <Input type="number" placeholder="Ej: 100" />
          </Form.Item>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item 
                name="points_expire" 
                label="Los puntos expiran" 
                valuePropName="checked"
                initialValue={false}
              >
                <Switch />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item 
                name="points_expiry_months" 
                label="Meses de expiración"
                dependencies={['points_expire']}
              >
                <Input 
                  type="number" 
                  placeholder="Ej: 12" 
                  disabled={!loyaltyProgramForm.getFieldValue('points_expire')}
                />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item 
            name="is_active" 
            label="Activo" 
            valuePropName="checked"
            initialValue={true}
          >
            <Switch />
          </Form.Item>

          <Form.Item 
            name="is_default" 
            label="Predeterminado" 
            valuePropName="checked"
            initialValue={false}
          >
            <Switch />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" block>
              {editingProgram ? "Actualizar Programa" : "Crear Programa"}
            </Button>
          </Form.Item>
        </Form>
      </Modal>

      {/* Modal para edición/creación de lista de precios */}
      <Modal
        title={editingPriceList ? "Editar Lista de Precios" : "Crear Nueva Lista de Precios"}
        open={priceListModalVisible}
        onCancel={() => setPriceListModalVisible(false)}
        footer={null}
        width={600}
      >
        <Form
          form={priceListForm}
          layout="vertical"
          onFinish={handleSavePriceList}
        >
          <Form.Item 
            name="name" 
            label="Nombre de la lista"
            rules={[{ required: true, message: 'Por favor ingrese el nombre' }]}
          >
            <Input placeholder="Ej: Lista Premium Clientes" />
          </Form.Item>

          <Form.Item name="description" label="Descripción">
            <Input.TextArea rows={3} placeholder="Descripción de la lista de precios" />
          </Form.Item>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item 
                name="currency" 
                label="Moneda"
                initialValue="MXN"
              >
                <Select>
                  <Select.Option value="MXN">Peso Mexicano (MXN)</Select.Option>
                  <Select.Option value="USD">Dólar Americano (USD)</Select.Option>
                  <Select.Option value="EUR">Euro (EUR)</Select.Option>
                  <Select.Option value="COP">Peso Colombiano (COP)</Select.Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item 
                name="validity_period" 
                label="Periodo de validez"
              >
                <RangePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item 
                name="is_active" 
                label="Activa" 
                valuePropName="checked"
                initialValue={true}
              >
                <Switch />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item 
                name="is_default" 
                label="Predeterminada" 
                valuePropName="checked"
                initialValue={false}
              >
                <Switch />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item>
            <Button type="primary" htmlType="submit" block>
              {editingPriceList ? "Actualizar Lista" : "Crear Lista"}
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default SalesConfiguration;